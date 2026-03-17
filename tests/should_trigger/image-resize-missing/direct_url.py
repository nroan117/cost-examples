import openai
client = openai.OpenAI()

img_url = "https://example.com/photo.jpg"
client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[{"role": "user", "content": [{"type": "text", "text": "Describe"}, {"type": "image_url", "image_url": {"url": img_url}}]}],
    max_tokens=200
)
