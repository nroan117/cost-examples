"""
SHOULD NOT TRIGGER missing-recursion-limit
Clean 2: ConversableAgent with max_consecutive_auto_reply as the first kwarg —
argument order does not matter; the pattern-not matches either way.
"""
from autogen import ConversableAgent

llm_config = {"model": "gpt-4o", "api_key": "placeholder"}

agent = ConversableAgent(
    "analyst",
    max_consecutive_auto_reply=5,
    llm_config=llm_config,
    human_input_mode="NEVER",
)
