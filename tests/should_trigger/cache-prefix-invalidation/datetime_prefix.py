"""Trigger: datetime.now() at start of system message."""
import datetime
import openai

client = openai.OpenAI()
SYSTEM_PROMPT = "You are a helpful assistant with detailed instructions."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": f"{datetime.now()}\n\n{SYSTEM_PROMPT}"}],
    max_tokens=500,
)
