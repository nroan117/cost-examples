"""
SHOULD NOT TRIGGER unstructured-response-retries
Clean 3: while True with json.JSONDecodeError but no .create() inside the loop —
the LLM call is made once outside, then we retry only the parse step on
cached content (not a real pattern, but tests the rule boundary).
"""
import json


def parse_cached_output(raw: str) -> dict:
    # No .create() call inside the loop — rule does not fire.
    while True:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Strip common model preambles and retry parsing.
            if raw.startswith("```json"):
                raw = raw[7:]
            elif raw.startswith("```"):
                raw = raw[3:]
            elif raw.endswith("```"):
                raw = raw[:-3]
            else:
                raise
