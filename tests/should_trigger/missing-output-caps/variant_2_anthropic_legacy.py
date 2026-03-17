"""
SHOULD TRIGGER missing-output-caps
Variant 2: Anthropic legacy completions API — max_tokens_to_sample is NOT
the same as max_tokens and does not satisfy the rule's pattern-not clauses.
"""
import anthropic

client = anthropic.Anthropic()

# max_tokens_to_sample is the legacy Anthropic parameter name and is NOT caught
# by pattern-not: max_tokens=..., max_output_tokens=..., max_completion_tokens=...
response = client.completions.create(
    model="claude-2",
    prompt="\n\nHuman: What is our return window?\n\nAssistant:",
    max_tokens_to_sample=512,
)
print(response.completion)
