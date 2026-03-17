import openai
client = openai.OpenAI()

# Good: text-only, no image_url
client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello, world!"}],
    max_tokens=100
)
