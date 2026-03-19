"""
SHOULD NOT TRIGGER anthropic-missing-cache-control
Variant 1: system passed as a list with cache_control — correctly optimised.
"""
import anthropic

client = anthropic.Anthropic()

# Good: system as list with cache_control
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[{"type": "text", "text": "You are a helpful assistant.", "cache_control": {"type": "ephemeral"}}],
    messages=[{"role": "user", "content": "Hello"}]
)
