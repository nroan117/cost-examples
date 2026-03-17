"""
SHOULD TRIGGER missing-reasoning-parameters
Variant 1: responses.create with o3 — neither reasoning_effort nor
max_completion_tokens is provided.
"""
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o3",
    input=[
        {"role": "user", "content": "Debug this production outage: database connections timing out."},
    ],
)
print(response.output_text)
