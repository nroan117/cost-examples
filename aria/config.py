"""
Aria API configuration.

Central client setup for all LLM providers used by Aria.
VULNERABILITY: hardcoded-api-key — OpenAI API key committed directly in source.
"""
from openai import OpenAI

# BUG: API key hardcoded in source — this will be committed to version control,
# exposing credentials to anyone with repo access. Use os.environ["OPENAI_API_KEY"].
client = OpenAI(api_key="sk-proj-abc123examplekeydonotuse")

# Application settings
DEFAULT_MODEL = "gpt-4o"
FALLBACK_MODEL = "gpt-3.5-turbo"
MAX_HISTORY_TURNS = 10
