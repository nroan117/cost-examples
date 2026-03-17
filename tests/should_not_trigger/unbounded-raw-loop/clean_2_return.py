"""
SHOULD NOT TRIGGER unbounded-raw-loop
Clean 2: while True loop exits via return — pattern-not suppresses the finding.
"""
from openai import OpenAI

client = OpenAI()


def get_non_empty_response(prompt: str) -> str:
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        content = response.choices[0].message.content
        if content:
            return content
