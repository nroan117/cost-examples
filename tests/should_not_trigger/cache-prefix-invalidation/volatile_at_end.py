"""No trigger: volatile appended at END of system prompt (cache prefix preserved)."""
import datetime
import openai

client = openai.OpenAI()
SYSTEM_PROMPT = "You are a helpful assistant with detailed instructions."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": f"{SYSTEM_PROMPT}\n\nContext refreshed at {datetime.now()}",
        },
        {"role": "user", "content": "Hello"},
    ],
    max_tokens=200,
)
