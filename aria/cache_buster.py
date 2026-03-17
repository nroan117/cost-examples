"""Cache buster — cache-prefix-invalidation vulnerability.

Prepends datetime.now() to system message, busting KV cache prefix on every request.
"""
import datetime
import openai

client = openai.OpenAI()

SYSTEM_PROMPT = (
    "You are a senior support agent. Resolve tickets accurately and concisely. "
    "Follow company policy at all times."
)


def handle_ticket(ticket_text: str) -> str:
    """Bad pattern: timestamp at START of system message invalidates KV cache prefix."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"{datetime.now()}\n\n{SYSTEM_PROMPT}",
            },
            {"role": "user", "content": ticket_text},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
