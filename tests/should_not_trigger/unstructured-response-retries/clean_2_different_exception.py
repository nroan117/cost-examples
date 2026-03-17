"""
SHOULD NOT TRIGGER unstructured-response-retries
Clean 2: while True with .create() but catching ValueError instead of
json.JSONDecodeError — the rule specifically requires json.JSONDecodeError.
"""
import json
from openai import OpenAI

client = OpenAI()


def parse_with_validation(prompt: str) -> dict:
    attempts = 0
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        try:
            data = json.loads(response.choices[0].message.content)
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")
            return data
        except ValueError:
            attempts += 1
            if attempts >= 3:
                raise
