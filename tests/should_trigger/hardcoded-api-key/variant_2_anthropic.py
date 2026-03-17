"""
SHOULD TRIGGER hardcoded-api-key
Variant 2: Anthropic() constructor with api_key= set to a string literal
starting with "sk-" (the rule's regex matches "sk-[^"]*").
"""
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-api03-abc123fakekey-do-not-use")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello"}],
)
