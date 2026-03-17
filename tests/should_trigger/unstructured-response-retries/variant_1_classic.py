"""
SHOULD TRIGGER unstructured-response-retries
Variant 1: Classic while True JSON-retry loop — breaks on success but retries
forever on JSONDecodeError with no counter.
"""
import json
from openai import OpenAI

client = OpenAI()


def get_structured_output(prompt: str) -> dict:
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        try:
            result = json.loads(response.choices[0].message.content)
            break
        except json.JSONDecodeError:
            continue
    return result
