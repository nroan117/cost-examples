"""
SHOULD NOT TRIGGER missing-reasoning-parameters
Clean 3: chat.completions.create — the rule only matches *.responses.create,
so the completions API is outside its scope even without any reasoning params.
"""
from openai import OpenAI

client = OpenAI()

# completions.create is covered by missing-output-caps, not missing-reasoning-parameters.
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=100,
)
print(response.choices[0].message.content)
