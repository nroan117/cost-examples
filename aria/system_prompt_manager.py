# Aria system prompt manager — INTENTIONAL VULNERABILITY: system prompt not cached
# Long system prompt passed as plain string — re-sent on every API call.
import anthropic

client = anthropic.Anthropic()

ARIA_SYSTEM_PROMPT = """
You are Aria, the intelligent customer support agent for TechCorp. Your role is to help 
customers resolve their issues quickly and efficiently. You have access to order information,
account data, and product documentation.

Guidelines:
- Always greet customers warmly and use their name if available
- Acknowledge the customer's issue before providing solutions
- For order issues: ask for order number and check tracking status
- For billing disputes: explain the charges clearly and offer adjustments when appropriate
- For technical issues: walk through troubleshooting steps patiently
- For returns/refunds: follow the 30-day return policy strictly
- Escalate to human agents for: legal threats, safety concerns, unresolved issues after 3 attempts
- Never promise what you cannot deliver
- End every conversation by asking if there is anything else you can help with

TechCorp values: Innovation, Integrity, Customer First, Continuous Improvement
Support hours: 24/7 for chat, 9-5 PT for phone support
"""


def handle_message(user_message: str, conversation_history: list) -> str:
    """Handle a customer message using Aria's system prompt."""
    messages = conversation_history + [{"role": "user", "content": user_message}]
    response = client.messages.create(
        model="claude-haiku-3-5",
        max_tokens=500,
        system=ARIA_SYSTEM_PROMPT,  # noqa: COST005 — intentional: not cached
        messages=messages,
    )
    return response.content[0].text
