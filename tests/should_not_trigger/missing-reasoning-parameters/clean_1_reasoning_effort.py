"""
SHOULD NOT TRIGGER missing-reasoning-parameters
Clean 1: reasoning_effort explicitly set — satisfies one of the pattern-not clauses.
"""
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o3-mini",
    input="Classify this support ticket.",
    reasoning_effort="medium",
)
print(response.output_text)
