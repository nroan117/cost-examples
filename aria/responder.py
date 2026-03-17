"""Responder — missing-output-caps-responses vulnerability."""
import openai

client = openai.OpenAI()


def get_response(prompt: str) -> str:
    """Call responses.create without max_output_tokens — bad pattern."""
    response = client.responses.create(
        model="o3",
        input=prompt
    )
    return response.output_text
