"""Vision analyzer — image-resize-missing vulnerability."""
import openai

client = openai.OpenAI()


def analyze_image(img_url: str) -> str:
    """Send image URL directly to vision API without resizing — bad pattern."""
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail"},
                    {"type": "image_url", "image_url": {"url": img_url}}
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content
