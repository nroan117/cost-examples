#!/usr/bin/env python3
"""
run_bad_patterns.py — Generates intentional bad LLM call patterns against the
mock server to exercise behavioral cost detectors.

Patterns exercised
------------------
1. Retry storm  — 20 rapid-fire calls to /v1/messages  (triggers behavioral/retry-storm)
2. Missing caps — 10 calls to /v1/messages without max_tokens
                  (triggers behavioral/missing-output-caps)

Both patterns call the mock server directly via urllib so the anthropic SDK is
not required; if it IS installed the script still uses urllib for predictability.

Environment variables:
  ANTHROPIC_BASE_URL  — base URL of mock server (default: http://localhost:8080)
  MOCK_LLM_URL        — alias for ANTHROPIC_BASE_URL
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

_base = (
    os.environ.get("ANTHROPIC_BASE_URL")
    or os.environ.get("MOCK_LLM_URL")
    or "http://localhost:8080"
).rstrip("/")

MESSAGES_URL = f"{_base}/v1/messages"
RESET_URL = f"{_base}/reset"
HEALTH_URL = f"{_base}/health"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _post(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        # Non-2xx are still fine for our purposes — we just want the call recorded
        body = e.read().decode(errors="replace")
        return {"error": str(e), "body": body}
    except urllib.error.URLError as e:
        print(f"  ⚠  Could not reach mock server at {url}: {e}", file=sys.stderr)
        raise


def _reset() -> None:
    req = urllib.request.Request(RESET_URL, data=b"", method="POST")
    with urllib.request.urlopen(req, timeout=5):
        pass


def _check_health() -> bool:
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Pattern 1 — Retry storm (20 rapid calls in < 2s triggers the detector)
# ---------------------------------------------------------------------------

def run_retry_storm(n: int = 20) -> None:
    print(f"\n[Pattern 1] Retry storm — {n} rapid-fire calls to {MESSAGES_URL}")
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "ping"}],
    }
    start = time.monotonic()
    for i in range(n):
        _post(MESSAGES_URL, payload)
    elapsed = time.monotonic() - start
    print(f"  ✓ {n} calls completed in {elapsed:.2f}s")


# ---------------------------------------------------------------------------
# Pattern 2 — Missing max_tokens (10 calls without the cap)
# ---------------------------------------------------------------------------

def run_missing_max_tokens(n: int = 10) -> None:
    print(f"\n[Pattern 2] Missing max_tokens — {n} calls without output cap")
    payload_no_cap = {
        "model": "claude-3-5-sonnet-20241022",
        # NOTE: intentionally omitting max_tokens to trigger the detector
        "messages": [{"role": "user", "content": "What is 2+2?"}],
    }
    for i in range(n):
        _post(MESSAGES_URL, payload_no_cap)
    print(f"  ✓ {n} uncapped calls sent")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print(f"Mock LLM server: {_base}")

    if not _check_health():
        print(f"ERROR: mock server not reachable at {HEALTH_URL}", file=sys.stderr)
        return 1

    _reset()
    print("  ✓ Call log reset")

    run_retry_storm(n=20)
    run_missing_max_tokens(n=10)

    print("\n✅ Bad-pattern simulation complete. Run behavioral-report.py to analyse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
