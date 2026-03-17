"""Trigger: time.time() at start of system message."""
import time
import openai

client = openai.OpenAI()
SYSTEM_PROMPT = "You are a helpful assistant."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": f"{time.time()} {SYSTEM_PROMPT}"}],
    max_tokens=200,
)
