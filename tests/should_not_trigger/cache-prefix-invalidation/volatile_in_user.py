"""No trigger: volatile in user message, not system."""
import datetime
import openai

client = openai.OpenAI()
SYSTEM_PROMPT = "You are a helpful assistant."
query = "What is the weather today?"

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Current time: {datetime.now()} — {query}"},
    ],
    max_tokens=200,
)
