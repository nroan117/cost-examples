"""
SHOULD NOT TRIGGER reasoning-threshold-breach
Clean 3: reasoning_effort comes from a variable — the rule only matches the
literal strings "high" and "maximum", not variable references.
"""
import os
from openai import OpenAI

client = OpenAI()

# Effort level controlled by environment or config — not a hardcoded literal.
effort_level = os.getenv("REASONING_EFFORT", "medium")

response = client.responses.create(
    model="o3-mini",
    input="Summarise this ticket.",
    reasoning_effort=effort_level,
    max_completion_tokens=1000,
)
