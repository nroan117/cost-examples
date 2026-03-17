"""
SHOULD NOT TRIGGER unstructured-response-retries
Clean 1: Bounded for loop with range — not a while True, so the pattern does
not match regardless of the exception handling inside.
"""
import json
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)
MAX_RETRIES = 3


def extract_json_safe(prompt: str) -> dict:
    for attempt in range(MAX_RETRIES):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.warning("Attempt %d/%d: malformed JSON", attempt + 1, MAX_RETRIES)
    raise ValueError(f"Could not extract JSON after {MAX_RETRIES} attempts")
