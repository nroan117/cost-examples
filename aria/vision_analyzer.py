"""Vision analyzer — image-resize-missing FIXED."""
import openai
from PIL import Image
import base64
import io

client = openai.OpenAI()

TARGET_SIZE = (512, 512)


def analyze_image(image_path: str) -> str:
    """Resize image before sending to vision API."""
    # FIX: resize to cap token usage for vision
    img = Image.open(image_path)
    img.resize(TARGET_SIZE)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content
