"""
SHOULD NOT TRIGGER reasoning-threshold-breach
Clean 1: reasoning_effort="medium" — below the "high"/"maximum" threshold,
so neither pattern-either branch matches.
"""
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o3-mini",
    input="Classify this support ticket.",
    reasoning_effort="medium",
    max_completion_tokens=1000,
)
print(response.output_text)
