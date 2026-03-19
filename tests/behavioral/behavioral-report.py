#!/usr/bin/env python3
"""
behavioral-report.py — Standalone behavioral cost regression reporter.

Fetches the call log from the mock LLM server, runs behavioral analysis,
prints human-readable findings to stdout, and writes a SARIF file if any
findings exist.

Exit code: 1 if any ERROR-severity findings, 0 otherwise.

Environment variables:
  MOCK_LLM_URL  — base URL of mock server (default: http://localhost:8080)
  SARIF_OUTPUT  — path for SARIF output   (default: behavioral-findings.sarif)
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import List, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MOCK_LLM_URL = os.environ.get("MOCK_LLM_URL", "http://localhost:8080").rstrip("/")
SARIF_OUTPUT = os.environ.get("SARIF_OUTPUT", "behavioral-findings.sarif")

# ---------------------------------------------------------------------------
# Inline analyzer (mirrors mock-server/analyzer.py so this script is self-contained)
# The server stores timestamps as timestamp_ms (milliseconds) and has_max_tokens
# (bool). We normalise on the way in.
# ---------------------------------------------------------------------------


@dataclass
class BehavioralFinding:
    rule_id: str
    severity: str   # "ERROR" | "WARNING" | "INFO"
    message: str
    evidence: dict


def _normalise_calls(raw_calls: list) -> list:
    """Convert server call records into the format expected by detectors.

    Server format:
        timestamp_ms  (int, unix millis)
        has_max_tokens (bool)
        estimated_input_tokens (int)

    Detector format:
        timestamp  (float, unix seconds)
        max_tokens (int | None)  — presence signals cap was set
        estimated_input_tokens (int)
    """
    normalised = []
    for c in raw_calls:
        nc = dict(c)
        # Convert ms → seconds
        if "timestamp_ms" in nc and "timestamp" not in nc:
            nc["timestamp"] = nc["timestamp_ms"] / 1000.0
        # Map has_max_tokens bool → max_tokens presence
        if "has_max_tokens" in nc and "max_tokens" not in nc:
            if nc["has_max_tokens"]:
                nc["max_tokens"] = 1  # sentinel — value doesn't matter, only presence
        normalised.append(nc)
    return normalised


class LoopDetector:
    """Fires when >50 calls made in any 10-second window."""
    WINDOW_SECONDS = 10
    THRESHOLD = 50
    RULE_ID = "behavioral/loop-detected"

    def detect(self, calls: list) -> Optional[BehavioralFinding]:
        if not calls:
            return None
        timestamps = sorted(c["timestamp"] for c in calls)
        worst_count = 0
        for t in timestamps:
            window_end = t + self.WINDOW_SECONDS
            count = sum(1 for ts in timestamps if t <= ts < window_end)
            if count > worst_count:
                worst_count = count
        if worst_count > self.THRESHOLD:
            return BehavioralFinding(
                rule_id=self.RULE_ID,
                severity="ERROR",
                message=(
                    f"Possible infinite or runaway loop detected: {worst_count} LLM calls "
                    f"in {self.WINDOW_SECONDS}s. Check for unbounded agent loops."
                ),
                evidence={
                    "calls_in_window": worst_count,
                    "window_seconds": self.WINDOW_SECONDS,
                    "peak_rate": round(worst_count / self.WINDOW_SECONDS, 2),
                },
            )
        return None


class RetryStormDetector:
    """Fires when >10 calls in any 2-second window."""
    WINDOW_SECONDS = 2
    THRESHOLD = 10
    RULE_ID = "behavioral/retry-storm"

    def detect(self, calls: list) -> Optional[BehavioralFinding]:
        if not calls:
            return None
        timestamps = sorted(c["timestamp"] for c in calls)
        worst_count = 0
        for t in timestamps:
            window_end = t + self.WINDOW_SECONDS
            count = sum(1 for ts in timestamps if t <= ts < window_end)
            if count > worst_count:
                worst_count = count
        if worst_count > self.THRESHOLD:
            return BehavioralFinding(
                rule_id=self.RULE_ID,
                severity="ERROR",
                message=(
                    f"Retry storm detected: {worst_count} calls in {self.WINDOW_SECONDS}s. "
                    f"Likely unguarded retry loop on failed responses."
                ),
                evidence={
                    "calls_in_window": worst_count,
                    "window_seconds": self.WINDOW_SECONDS,
                },
            )
        return None


class ConcurrencyExplosionDetector:
    """Fires when peak concurrent calls (overlapping within 100ms) > 20."""
    OVERLAP_MS = 0.1  # 100ms in seconds
    THRESHOLD = 20
    RULE_ID = "behavioral/concurrency-explosion"

    def detect(self, calls: list) -> Optional[BehavioralFinding]:
        if not calls:
            return None
        timestamps = sorted(c["timestamp"] for c in calls)
        peak = 0
        for t in timestamps:
            concurrent = sum(1 for ts in timestamps if abs(ts - t) <= self.OVERLAP_MS)
            if concurrent > peak:
                peak = concurrent
        if peak > self.THRESHOLD:
            return BehavioralFinding(
                rule_id=self.RULE_ID,
                severity="WARNING",
                message=(
                    f"Concurrency explosion: {peak} simultaneous LLM calls detected. "
                    f"Add concurrency limits to asyncio.gather() or similar patterns."
                ),
                evidence={"peak_concurrent": peak},
            )
        return None


class UnboundedOutputDetector:
    """Fires when >20% of calls are missing max_tokens / max_completion_tokens."""
    THRESHOLD_PCT = 20.0
    RULE_ID = "behavioral/missing-output-caps"

    def detect(self, calls: list) -> Optional[BehavioralFinding]:
        if not calls:
            return None
        total = len(calls)
        missing = sum(
            1 for c in calls
            if not c.get("max_tokens") and not c.get("max_completion_tokens")
        )
        pct = round(missing / total * 100, 1)
        if pct > self.THRESHOLD_PCT:
            return BehavioralFinding(
                rule_id=self.RULE_ID,
                severity="WARNING",
                message=(
                    f"{missing} of {total} calls ({pct}%) missing "
                    f"max_tokens/max_completion_tokens. "
                    f"Uncapped output can cause unbounded spend."
                ),
                evidence={"missing_count": missing, "total_calls": total, "percentage": pct},
            )
        return None


class LargeContextDetector:
    """Fires when average estimated_input_tokens > 50,000."""
    THRESHOLD = 50_000
    RULE_ID = "behavioral/large-context"

    def detect(self, calls: list) -> Optional[BehavioralFinding]:
        if not calls:
            return None
        token_counts = [c.get("estimated_input_tokens", 0) for c in calls]
        avg = round(sum(token_counts) / len(token_counts))
        max_tok = max(token_counts)
        if avg > self.THRESHOLD:
            return BehavioralFinding(
                rule_id=self.RULE_ID,
                severity="WARNING",
                message=(
                    f"Average input context is {avg} estimated tokens. "
                    f"Large contexts dramatically increase per-call cost."
                ),
                evidence={"avg_tokens": avg, "max_tokens": max_tok, "total_calls": len(calls)},
            )
        return None


_DETECTORS = [
    LoopDetector(),
    RetryStormDetector(),
    ConcurrencyExplosionDetector(),
    UnboundedOutputDetector(),
    LargeContextDetector(),
]


def analyze(report: dict) -> List[BehavioralFinding]:
    """Run all detectors against a /report payload. Returns deduplicated findings."""
    calls = _normalise_calls(report.get("calls", []))
    findings: dict = {}
    for detector in _DETECTORS:
        finding = detector.detect(calls)
        if finding and finding.rule_id not in findings:
            findings[finding.rule_id] = finding
    return list(findings.values())


def to_sarif(findings: List[BehavioralFinding], tool_version: str = "0.1.0") -> dict:
    """Convert findings list to SARIF 2.1.0 format."""
    _SEV = {"ERROR": "error", "WARNING": "warning", "INFO": "note"}
    rules = []
    results = []
    seen: set = set()

    for f in findings:
        if f.rule_id not in seen:
            seen.add(f.rule_id)
            rules.append({
                "id": f.rule_id,
                "name": f.rule_id.replace("/", "_").replace("-", "_"),
                "shortDescription": {"text": f.message},
                "defaultConfiguration": {"level": _SEV.get(f.severity, "warning")},
                "properties": {"tags": ["behavioral", "cost"]},
            })
        results.append({
            "ruleId": f.rule_id,
            "level": _SEV.get(f.severity, "warning"),
            "message": {"text": f.message},
            "properties": {"evidence": f.evidence},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": "runtime://llm-calls",
                        "uriBaseId": "%SRCROOT%",
                    }
                }
            }],
        })

    return {
        "$schema": (
            "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/"
            "master/Schemata/sarif-schema-2.1.0.json"
        ),
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "cost-behavioral-analyzer",
                    "version": tool_version,
                    "informationUri": "https://github.com/nroan117/cost",
                    "rules": rules,
                }
            },
            "results": results,
        }],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def fetch_report(url: str) -> dict:
    req = urllib.request.Request(f"{url}/report", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"ERROR: Could not reach mock server at {url}: {e}", file=sys.stderr)
        sys.exit(2)


def print_findings(findings: List[BehavioralFinding]) -> None:
    if not findings:
        print("✅ No behavioral findings. All patterns look healthy.")
        return

    print(f"\n{'='*60}")
    print(f"  Behavioral Cost Findings ({len(findings)} total)")
    print(f"{'='*60}\n")

    for f in findings:
        icon = "🔴" if f.severity == "ERROR" else "🟡" if f.severity == "WARNING" else "🔵"
        print(f"{icon}  [{f.severity}] {f.rule_id}")
        print(f"   {f.message}")
        print(f"   Evidence: {json.dumps(f.evidence, indent=6)}")
        print()


def main() -> int:
    print(f"Fetching call report from {MOCK_LLM_URL}/report …")
    report = fetch_report(MOCK_LLM_URL)
    total = report.get("total_calls", 0)
    print(f"Analysing {total} recorded LLM call(s)…\n")

    findings = analyze(report)
    print_findings(findings)

    if findings:
        sarif = to_sarif(findings)
        with open(SARIF_OUTPUT, "w", encoding="utf-8") as fh:
            json.dump(sarif, fh, indent=2)
        print(f"📄 SARIF written to: {SARIF_OUTPUT}")

    errors = [f for f in findings if f.severity == "ERROR"]
    if errors:
        print(f"\n❌ {len(errors)} ERROR finding(s) detected — exiting with code 1.")
        return 1

    print("✅ No ERROR findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
