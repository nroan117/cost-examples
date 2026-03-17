"""
Aria customer support chatbot.

Handles incoming support queries with conversational context.
VULNERABILITY: missing-output-caps — completions.create called without max_tokens.
"""
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are Aria, a friendly and knowledgeable customer support assistant
for Acme Corp. Help customers resolve their issues efficiently and professionally."""


def handle_support_query(user_message: str, conversation_history: list) -> str:
    """Handle a customer support query, maintaining conversation history."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history,
        {"role": "user", "content": user_message},
    ]

    # BUG: missing max_tokens — the model can generate an arbitrarily long response,
    # causing unbounded token costs on every support interaction.
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content


def start_session(customer_id: str) -> dict:
    """Start a new support session for a customer."""
    return {
        "customer_id": customer_id,
        "history": [],
    }
