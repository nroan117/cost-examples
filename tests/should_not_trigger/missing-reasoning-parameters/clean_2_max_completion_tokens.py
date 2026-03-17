"""
SHOULD NOT TRIGGER missing-reasoning-parameters
Clean 2: max_completion_tokens explicitly set — satisfies the other pattern-not clause.
"""
from openai import OpenAI

client = OpenAI()


def bounded_reasoning(prompt: str) -> str:
    response = client.responses.create(
        model="o3",
        input=prompt,
        max_completion_tokens=2000,
    )
    return response.output_text
