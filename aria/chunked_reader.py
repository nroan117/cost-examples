"""Chunked reader — file-chunk-read-loop vulnerability."""
import openai

client = openai.OpenAI()


def process_file_in_chunks(filepath: str) -> list:
    """Read file in tiny chunks and call LLM per chunk — bad pattern."""
    results = []
    with open(filepath) as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": chunk}],
                max_tokens=100
            )
            results.append(response.choices[0].message.content)
    return results
