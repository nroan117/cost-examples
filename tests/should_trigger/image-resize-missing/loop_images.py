import openai
client = openai.OpenAI()

urls = ["https://example.com/img1.jpg", "https://example.com/img2.jpg"]
for url in urls:
    client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": url}}]}],
        max_tokens=100
    )
