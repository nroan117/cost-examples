#!/usr/bin/env bash
# verify.sh — validate all 9 semgrep rules against should_trigger / should_not_trigger test fixtures.
#
# Usage:
#   bash scripts/verify.sh [RULES_DIR]
#
# RULES_DIR defaults to ./rules/ (the local semgrep-1.x-compatible rule copies in this repo).
# Pass the backend policies dir to test against the originals (requires a semgrep version that
# handles duplicate YAML keys, typically semgrep <1.100).
#
# Exit 0 if all checks pass, 1 if any fail.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RULES_DIR="${1:-$REPO_ROOT/rules}"
TRIGGER_DIR="$REPO_ROOT/tests/should_trigger"
NO_TRIGGER_DIR="$REPO_ROOT/tests/should_not_trigger"

PASS=0
FAIL=0
ERRORS=()

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

RULES=(
  "hardcoded-api-key"
  "missing-output-caps"
  "missing-reasoning-parameters"
  "missing-recursion-limit"
  "parallel-tool-call-explosion"
  "reasoning-threshold-breach"
  "top-k-distance-breach"
  "unbounded-raw-loop"
  "unstructured-response-retries"
)

echo ""
echo "======================================================"
echo "  cost rule verification — $(date '+%Y-%m-%d %H:%M')"
echo "  Rules dir : $RULES_DIR"
echo "  Repo root : $REPO_ROOT"
echo "======================================================"
echo ""

check_rule() {
  local rule="$1"
  local rule_yaml="$RULES_DIR/${rule}.yaml"
  local trigger_path="$TRIGGER_DIR/$rule"
  local no_trigger_path="$NO_TRIGGER_DIR/$rule"

  if [[ ! -f "$rule_yaml" ]]; then
    echo -e "  ${RED}SKIP${NC}  $rule — rule file not found: $rule_yaml"
    ERRORS+=("$rule: rule yaml missing")
    ((FAIL++)) || true
    return
  fi

  # ---- should_trigger ----
  if [[ -d "$trigger_path" ]]; then
    local findings
    findings=$(semgrep --config "$rule_yaml" "$trigger_path" --json 2>/dev/null \
      | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null || echo "0")

    if [[ "$findings" -ge 1 ]]; then
      echo -e "  ${GREEN}PASS${NC}  should_trigger/$rule  ($findings finding(s))"
      ((PASS++)) || true
    else
      echo -e "  ${RED}FAIL${NC}  should_trigger/$rule  — expected >= 1 finding, got 0"
      ERRORS+=("should_trigger/$rule: 0 findings (expected >= 1)")
      ((FAIL++)) || true
    fi
  else
    echo -e "  ${YELLOW}WARN${NC}  should_trigger/$rule — directory not found, skipping"
  fi

  # ---- should_not_trigger ----
  if [[ -d "$no_trigger_path" ]]; then
    local non_findings
    non_findings=$(semgrep --config "$rule_yaml" "$no_trigger_path" --json 2>/dev/null \
      | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null || echo "0")

    if [[ "$non_findings" -eq 0 ]]; then
      echo -e "  ${GREEN}PASS${NC}  should_not_trigger/$rule  (0 findings ✓)"
      ((PASS++)) || true
    else
      # Print which files triggered unexpectedly
      local offenders
      offenders=$(semgrep --config "$rule_yaml" "$no_trigger_path" --json 2>/dev/null \
        | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d.get('results',[]):
    print('       >', r['path'], 'line', r['start']['line'])
" 2>/dev/null || true)
      echo -e "  ${RED}FAIL${NC}  should_not_trigger/$rule  — expected 0 findings, got $non_findings"
      echo "$offenders"
      ERRORS+=("should_not_trigger/$rule: $non_findings unexpected findings")
      ((FAIL++)) || true
    fi
  else
    echo -e "  ${YELLOW}WARN${NC}  should_not_trigger/$rule — directory not found, skipping"
  fi

  echo ""
}

for rule in "${RULES[@]}"; do
  echo "── $rule"
  check_rule "$rule"
done

echo "======================================================"
echo -e "  Results: ${GREEN}${PASS} passed${NC}  /  ${RED}${FAIL} failed${NC}"
echo "======================================================"

if [[ "${#ERRORS[@]}" -gt 0 ]]; then
  echo ""
  echo -e "${RED}Failures:${NC}"
  for e in "${ERRORS[@]}"; do
    echo "  • $e"
  done
  echo ""
  exit 1
fi

echo ""
echo -e "${GREEN}All checks passed!${NC}"
echo ""
exit 0
