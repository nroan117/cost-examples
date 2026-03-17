"""Video processor — video-token-explosion vulnerability."""
import openai

client = openai.OpenAI()


def analyze_video(video_path: str) -> str:
    """Pass full video file to multimodal API without frame sampling — bad pattern."""
    with open(video_path, "rb") as f:
        video_data = f.read()

    response = client.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Summarize this video"},
                    {"type": "video", "data": video_data}
                ]
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
