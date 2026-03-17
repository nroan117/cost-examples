"""Chunked reader — file-chunk-read-loop FIXED."""
import openai

client = openai.OpenAI()

MAX_CONTENT_CHARS = 8000


def process_file(filepath: str) -> str:
    """FIX: read full file then make a single API call instead of per-chunk calls."""
    with open(filepath) as f:
        content = f.read()

    # Single API call for the full content (truncated)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content[:MAX_CONTENT_CHARS]}],
        max_tokens=500
    )
    return response.choices[0].message.content
