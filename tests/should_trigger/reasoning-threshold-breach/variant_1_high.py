"""
SHOULD TRIGGER reasoning-threshold-breach
Variant 1: reasoning_effort="high" passed to responses.create.
"""
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o3-mini",
    input="Categorise this support ticket: password reset request.",
    reasoning_effort="high",
    max_completion_tokens=1000,
)
print(response.output_text)
