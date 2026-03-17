"""
SHOULD NOT TRIGGER hardcoded-api-key
Clean 2: os.getenv with a default — still a variable reference, not a literal.
The rule's metavariable-regex only matches "sk-[^"]*" string literals.
"""
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=api_key)
