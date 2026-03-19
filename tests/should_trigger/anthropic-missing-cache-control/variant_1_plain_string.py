"""
SHOULD TRIGGER anthropic-missing-cache-control
Variant 1: system passed as a plain string on a claude model — no cache_control.
"""
import anthropic

client = anthropic.Anthropic()

# Bad: system as plain string on claude model
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful assistant. Always be concise.",
    messages=[{"role": "user", "content": "Hello"}]
)
