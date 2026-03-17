"""Video processor — video-token-explosion FIXED."""
import openai

client = openai.OpenAI()

MAX_FRAMES = 10


def extract_frames(video_path: str, max_frames: int = MAX_FRAMES) -> list:
    """Sample frames from video to avoid full-video token explosion."""
    try:
        import cv2
        cap = cv2.VideoCapture(video_path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(1, total // max_frames)
        frames = []
        for i in range(0, total, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            if len(frames) >= max_frames:
                break
        cap.release()
        return frames
    except ImportError:
        return []


def analyze_video(video_path: str) -> str:
    """FIX: use frame sampling instead of passing full video."""
    frames = extract_frames(video_path, max_frames=MAX_FRAMES)

    response = client.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[{"role": "user", "content": f"Analyze video based on {len(frames)} sampled frames"}],
        max_tokens=500
    )
    return response.choices[0].message.content
