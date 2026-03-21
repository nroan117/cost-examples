# Aria AutoGen support team — INTENTIONAL VULNERABILITY: no max_consecutive_auto_reply
# Agents can loop indefinitely, burning unlimited tokens until timeout.
from autogen import AssistantAgent, UserProxyAgent

llm_config = {
    "model": "gpt-4o-mini",
    "temperature": 0,
}

# No max_consecutive_auto_reply — runaway risk
aria = AssistantAgent(
    name="aria",
    llm_config=llm_config,
    system_message=(
        "You are Aria, an expert customer support agent. "
        "Help customers resolve their issues completely."
    ),
)

# No max_consecutive_auto_reply
customer = UserProxyAgent(
    name="customer",
    human_input_mode="NEVER",
    code_execution_config=False,
)


def handle_support_session(issue: str) -> str:
    """Run a multi-turn support session — no reply limit!"""
    customer.initiate_chat(aria, message=issue)
    return aria.last_message()["content"]
