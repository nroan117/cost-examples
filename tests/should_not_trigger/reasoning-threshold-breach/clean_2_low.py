"""
SHOULD NOT TRIGGER reasoning-threshold-breach
Clean 2: reasoning_effort="low" — well below the threshold.
"""
from openai import OpenAI

client = OpenAI()


def quick_triage(description: str) -> str:
    response = client.responses.create(
        model="o3-mini",
        input=description,
        reasoning_effort="low",
        max_completion_tokens=500,
    )
    return response.output_text
