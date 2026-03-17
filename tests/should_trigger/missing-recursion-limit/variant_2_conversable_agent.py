"""
SHOULD TRIGGER missing-recursion-limit
Variant 2: AutoGen ConversableAgent without max_consecutive_auto_reply.
The two agents can exchange messages indefinitely.
"""
from autogen import ConversableAgent

llm_config = {"model": "gpt-4o", "api_key": "placeholder"}

# No max_consecutive_auto_reply — unbounded agent-to-agent conversation.
support_agent = ConversableAgent(
    "support_agent",
    system_message="You are a support agent. Help the customer.",
    llm_config=llm_config,
)

customer_proxy = ConversableAgent(
    "customer",
    llm_config=False,
    human_input_mode="NEVER",
)
