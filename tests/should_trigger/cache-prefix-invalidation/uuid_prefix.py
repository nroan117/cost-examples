"""Trigger: uuid.uuid4() at start of system message."""
import uuid
import openai

client = openai.OpenAI()
LARGE_PROMPT = "Large static system instructions that should be cached."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": f"{uuid.uuid4()} — {LARGE_PROMPT}"}],
    max_tokens=300,
)
