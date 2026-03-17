"""No trigger: static system prompt, no volatile prefix."""
import openai

client = openai.OpenAI()
SYSTEM_PROMPT = "You are a helpful assistant."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hello"},
    ],
    max_tokens=200,
)
