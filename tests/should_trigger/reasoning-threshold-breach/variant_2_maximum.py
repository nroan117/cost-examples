"""
SHOULD TRIGGER reasoning-threshold-breach
Variant 2: reasoning_effort="maximum" — the highest possible setting.
"""
from openai import OpenAI

client = OpenAI()


def deep_analysis(problem: str) -> str:
    response = client.responses.create(
        model="o3",
        input=problem,
        reasoning_effort="maximum",
        max_completion_tokens=5000,
    )
    return response.output_text
