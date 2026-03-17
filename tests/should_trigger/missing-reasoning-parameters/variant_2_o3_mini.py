"""
SHOULD TRIGGER missing-reasoning-parameters
Variant 2: responses.create with o3-mini — no reasoning budget set.
"""
from openai import OpenAI

client = OpenAI()


def analyse_ticket(description: str) -> str:
    response = client.responses.create(
        model="o3-mini",
        input=description,
    )
    return response.output_text
