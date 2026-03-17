import openai
client = openai.OpenAI()

with open("lecture.mkv", "rb") as f:
    video_bytes = f.read()

client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": [{"type": "text", "text": "Transcribe"}, {"type": "video", "data": video_bytes}]}],
    max_tokens=1000
)
