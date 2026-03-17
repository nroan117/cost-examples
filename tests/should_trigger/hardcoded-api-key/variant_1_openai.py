"""
SHOULD TRIGGER hardcoded-api-key
Variant 1: OpenAI() constructor with api_key= set to a string literal.
"""
from openai import OpenAI

client = OpenAI(api_key="sk-proj-supersecretkey1234567890abcdef")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=50,
)
