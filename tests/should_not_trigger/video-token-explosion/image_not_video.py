import openai
client = openai.OpenAI()

# Good: image type, not video
with open("photo.jpg", "rb") as f:
    img_data = f.read()

client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": [{"type": "image", "data": img_data}]}],
    max_tokens=300
)
