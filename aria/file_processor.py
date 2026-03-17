"""File processor — context-dump-to-prompt vulnerability."""
import openai

client = openai.OpenAI()


def process_document(filename: str) -> str:
    """Read a file and send its full contents to the LLM — bad pattern."""
    with open(filename) as f:
        content = f.read()

    messages = [{"role": "user", "content": content}]
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    return response.choices[0].message.content
