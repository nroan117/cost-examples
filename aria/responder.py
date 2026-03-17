"""Responder — missing-output-caps-responses FIXED."""
import openai

client = openai.OpenAI()

MAX_OUTPUT_TOKENS = 1000  # FIX: cap output tokens to prevent runaway generation


def get_response(prompt: str) -> str:
    """Call responses.create with max_output_tokens cap."""
    response = client.responses.create(
        model="o3",
        input=prompt,
        max_output_tokens=MAX_OUTPUT_TOKENS  # FIX: added cap
    )
    return response.output_text
