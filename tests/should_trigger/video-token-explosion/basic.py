import openai
client = openai.OpenAI()

with open("movie.mp4", "rb") as f:
    video_data = f.read()

client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": [{"type": "text", "text": "Summarize"}, {"type": "video", "data": video_data}]}],
    max_tokens=500
)
