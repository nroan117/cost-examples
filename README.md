# cost-examples — Aria Demo App

**Aria** is a fictional AI-powered customer support chatbot used to demonstrate the
[cost](https://github.com/nroan117/cost) CI/CD tool.

The `aria/` directory contains **9 intentional LLM cost regression vulnerabilities** — one per
rule — that the `cost` GitHub Action detects on every push to `main`.
The `fixes/` branch contains the same app with all vulnerabilities remediated (0 findings).

---

## Intentional Vulnerabilities

| File | Rule | Description |
|------|------|-------------|
| `aria/chatbot.py` | `missing-output-caps` | `chat.completions.create()` missing `max_tokens` |
| `aria/agent.py` | `unbounded-raw-loop` | `while True:` with `.create()` and no `break`/`return`/`raise` |
| `aria/rag.py` | `top-k-distance-breach` | `top_k=200` — retrieves too many documents |
| `aria/reasoning_agent.py` | `missing-reasoning-parameters` | `responses.create()` missing `reasoning_effort` and `max_completion_tokens` |
| `aria/supervisor.py` | `missing-recursion-limit` | `StateGraph(...)` without `recursion_limit` |
| `aria/triage.py` | `reasoning-threshold-breach` | `reasoning_effort="high"` hardcoded for routine triage |
| `aria/parallel_handler.py` | `parallel-tool-call-explosion` | `asyncio.gather` over unbounded list comprehension of `.create()` calls |
| `aria/json_extractor.py` | `unstructured-response-retries` | `while True` JSON retry with `json.JSONDecodeError` and no retry cap |
| `aria/config.py` | `hardcoded-api-key` | `api_key="sk-..."` literal in source |

---

## New Rules (v0.4.0)

Two new rules added in v0.4.0:

| Rule | Description |
|------|-------------|
| `anthropic-missing-cache-control` | Detects Anthropic `messages.create()` calls where `system` is a plain string instead of a list with `cache_control` — missing prompt caching increases token costs on claude models |
| `a2a-missing-message-budget` | Detects `autogen.GroupChat` instantiated without `max_round` — unbounded agent-to-agent message loops can cause runaway costs |

Fixtures for both rules live in `tests/should_trigger/` and `tests/should_not_trigger/`.

---

## Test Suite

The `tests/` directory contains rule-precision test cases:

```
tests/
  should_trigger/        # each file MUST produce >= 1 finding for its rule
    <rule-name>/
      variant_1.py
      variant_2.py
      variant_3.py
  should_not_trigger/    # each file MUST produce 0 findings for its rule
    <rule-name>/
      clean_1.py
      clean_2.py
      clean_3.py
```

Run the full suite locally:

```bash
pip install semgrep
bash scripts/verify.sh /path/to/cost/backend/policies/default/
```

---

## CI/CD

The `cost` GitHub Action runs on every push and pull request.
On `main` it exits 1 (9 findings). On `fixes/` it exits 0 (0 findings).

```
main   → 9 findings → Action exits 1 ❌
fixes/ → 0 findings → Action exits 0 ✅
```

---

## Branches

| Branch | Purpose |
|--------|---------|
| `main` | Contains all 9 vulnerabilities |
| `fixes` | All vulnerabilities remediated |
