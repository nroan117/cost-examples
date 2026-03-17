import openai
client = openai.OpenAI()

def extract_frames(path, max_frames=10):
    return []  # stub

# Good: frame sampling
frames = extract_frames("video.mp4", max_frames=10)
client.chat.completions.create(
    model="gemini-1.5-pro",
    messages=[{"role": "user", "content": f"Analyze {len(frames)} frames"}],
    max_tokens=300
)
