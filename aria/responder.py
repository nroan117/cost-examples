"""Responder — missing-output-caps-responses FIXED."""
import openai

client = openai.OpenAI()

MAX_COMPLETION_TOKENS = 1000  # FIX: cap output tokens to prevent runaway generation


def get_response(prompt: str) -> str:
    """Call responses.create with reasoning_effort and output token cap."""
    response = client.responses.create(
        model="o3",
        input=prompt,
        reasoning_effort="medium",             # FIX: added reasoning effort budget
        max_completion_tokens=MAX_COMPLETION_TOKENS  # FIX: added output cap
    )
    return response.output_text
