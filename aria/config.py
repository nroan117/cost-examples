"""
Aria API configuration.

Central client setup for all LLM providers used by Aria.
FIX: API key loaded from environment variable instead of hardcoded literal.
"""
import os
from openai import OpenAI

# FIX: Read the API key from the environment — never commit secrets to source.
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Application settings
DEFAULT_MODEL = "gpt-4o"
FALLBACK_MODEL = "gpt-3.5-turbo"
MAX_HISTORY_TURNS = 10
