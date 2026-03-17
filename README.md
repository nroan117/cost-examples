# cost-examples

> Example app intentionally seeded with 9 LLM cost vulnerabilities to demonstrate the [cost](https://github.com/nroan117/cost) GitHub Action.

## What is Aria?

Aria is a minimal Python chatbot that uses OpenAI, LangGraph, and AutoGen. It is **deliberately vulnerable** — every file contains at least one pattern that the `cost` action will flag.

## Vulnerabilities

| # | Rule ID | File | Severity |
|---|---------|------|----------|
| 1 | `hardcoded-api-key` | `aria/chat.py` | Critical |
| 2 | `missing-reasoning-parameters` | `aria/reasoning.py` | High |
| 3 | `reasoning-threshold-breach` | `aria/reasoning.py` | High |
| 4 | `missing-recursion-limit` | `aria/agent.py` | High |
| 5 | `unbounded-raw-loop` | `aria/retry.py` | Critical |
| 6 | `missing-output-caps` | `aria/chat.py` | High |
| 7 | `parallel-tool-call-explosion` | `aria/fanout.py` | High |
| 8 | `unstructured-response-retries` | `aria/retry.py` | High |
| 9 | `top-k-distance-breach` | `aria/search.py` | Medium |

## Usage

1. Fork this repo
2. Add `COST_API_KEY` to Settings → Secrets → Actions
3. Open a PR — the `cost` action will surface all 9 findings as inline annotations
