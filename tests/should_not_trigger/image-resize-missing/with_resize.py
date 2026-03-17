import openai
from PIL import Image
import base64, io
client = openai.OpenAI()

img = Image.open("photo.jpg")
img.resize((512, 512))
buf = io.BytesIO()
img.save(buf, format="JPEG")
b64 = base64.b64encode(buf.getvalue()).decode()

client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}],
    max_tokens=200
)
