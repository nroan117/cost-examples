"""File processor — context-dump-to-prompt FIXED."""
import openai

client = openai.OpenAI()

MAX_CONTENT_CHARS = 4000  # prevent context window explosion


def process_document(filename: str) -> str:
    """Read a file with truncation before sending to LLM."""
    with open(filename) as f:
        content = f.read()[:MAX_CONTENT_CHARS]  # FIX: truncate to cap token usage

    messages = [{"role": "user", "content": content}]
    response = client.chat.completions.create(model="gpt-4o", messages=messages, max_tokens=500)
    return response.choices[0].message.content
