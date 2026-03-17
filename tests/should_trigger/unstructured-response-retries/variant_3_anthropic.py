"""
SHOULD TRIGGER unstructured-response-retries
Variant 3: Anthropic completions — the rule's $CLIENT.create(...) matches
any object's .create() call, not just OpenAI.
"""
import json
import anthropic

client = anthropic.Anthropic()


def parse_ticket_json(description: str) -> dict:
    while True:
        response = client.completions.create(
            model="claude-2",
            prompt=f"\n\nHuman: Extract JSON from: {description}\n\nAssistant:",
            max_tokens_to_sample=200,
        )
        try:
            return json.loads(response.completion)
        except json.JSONDecodeError:
            continue
