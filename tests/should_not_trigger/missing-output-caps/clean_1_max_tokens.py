"""
SHOULD NOT TRIGGER missing-output-caps
Clean 1: max_tokens explicitly set — satisfies pattern-not.
"""
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=500,
)
print(response.choices[0].message.content)
