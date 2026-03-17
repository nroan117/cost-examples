"""
SHOULD NOT TRIGGER missing-output-caps
Clean 2: max_completion_tokens used (valid alternative parameter name).
"""
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Summarise this."}],
    max_completion_tokens=1000,
    temperature=0.3,
)
print(response.choices[0].message.content)
