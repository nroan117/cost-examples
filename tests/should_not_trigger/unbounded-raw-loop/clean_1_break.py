"""
SHOULD NOT TRIGGER unbounded-raw-loop
Clean 1: while True loop exits via break — pattern-not suppresses the finding.
"""
from openai import OpenAI

client = OpenAI()


def resolve_with_retry(prompt: str, max_attempts: int = 3) -> str:
    attempt = 0
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        result = response.choices[0].message.content
        if result or attempt >= max_attempts:
            break
        attempt += 1
    return result
