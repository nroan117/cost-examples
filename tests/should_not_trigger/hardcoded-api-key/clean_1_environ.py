"""
SHOULD NOT TRIGGER hardcoded-api-key
Clean 1: API key loaded from environment variable — correct pattern.
"""
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=50,
)
