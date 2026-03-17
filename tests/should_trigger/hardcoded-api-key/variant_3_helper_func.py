"""
SHOULD TRIGGER hardcoded-api-key
Variant 3: The key is passed to a helper / factory function — the rule fires on
ANY function call with api_key="sk-..." not just the SDK constructors.
"""
from openai import OpenAI


def make_client(base_url: str, api_key: str) -> OpenAI:
    return OpenAI(base_url=base_url, api_key=api_key)


# This call triggers the rule: api_key="sk-..." as a keyword argument.
client = make_client(
    base_url="https://api.openai.com/v1",
    api_key="sk-proj-internal-dev-key-do-not-commit",
)
