import openai
client = openai.OpenAI()

def analyze(url):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{"role": "user", "content": [{"type": "text", "text": "What's in this image?"}, {"type": "image_url", "image_url": {"url": url}}]}],
        max_tokens=150
    )
    return response.choices[0].message.content
