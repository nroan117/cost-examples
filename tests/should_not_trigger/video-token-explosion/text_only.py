import openai
client = openai.OpenAI()

# Good: no video data at all
client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": "Summarize this text: ..."}],
    max_tokens=300
)
