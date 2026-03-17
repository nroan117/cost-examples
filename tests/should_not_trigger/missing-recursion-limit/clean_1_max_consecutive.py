"""
SHOULD NOT TRIGGER missing-recursion-limit
Clean 1: ConversableAgent with max_consecutive_auto_reply set — pattern-not matches.
"""
from autogen import ConversableAgent

llm_config = {"model": "gpt-4o", "api_key": "placeholder"}

agent = ConversableAgent(
    "support_agent",
    system_message="You are a support agent.",
    llm_config=llm_config,
    max_consecutive_auto_reply=10,
)
