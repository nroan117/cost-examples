"""
SHOULD TRIGGER unstructured-response-retries
Variant 2: Uses return instead of break on success — the loop still retries
indefinitely on JSONDecodeError. The rule has no pattern-not for return.
"""
import json
from openai import OpenAI

client = OpenAI()


def extract_json_fields(text: str) -> dict:
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Return JSON only."},
                {"role": "user", "content": text},
            ],
            max_tokens=300,
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            pass  # retry silently
