"""
SHOULD TRIGGER missing-output-caps
Variant 1: OpenAI SDK — chat.completions.create without any token cap.
"""
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Summarise our refund policy."}],
    temperature=0.5,
)
print(response.choices[0].message.content)
