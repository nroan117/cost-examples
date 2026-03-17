"""
SHOULD NOT TRIGGER hardcoded-api-key
Clean 3: API key comes from a config object — it's a variable reference,
not a "sk-..." string literal, so the metavariable-regex does not match.
"""
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class AppConfig:
    openai_api_key: str


def make_client(config: AppConfig) -> OpenAI:
    # api_key= receives a variable, not a literal — rule does not fire.
    return OpenAI(api_key=config.openai_api_key)
