import openai
client = openai.OpenAI()

with open("presentation.mp4", "rb") as f:
    raw_video = f.read()

client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": [{"type": "video", "data": raw_video}]}],
    max_tokens=300
)
