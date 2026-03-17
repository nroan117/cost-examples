"""
SHOULD NOT TRIGGER missing-output-caps
Clean 3: responses.create — the missing-output-caps rule only matches
*.completions.create, not *.responses.create. Completely different rule scope.
"""
from openai import OpenAI

client = OpenAI()

# responses.create is covered by missing-reasoning-parameters, not missing-output-caps.
response = client.responses.create(
    model="o3-mini",
    input="What is 2 + 2?",
    reasoning_effort="low",
    max_completion_tokens=100,
)
print(response.output_text)
