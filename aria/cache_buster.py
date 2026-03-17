"""Cache buster — cache-prefix-invalidation FIXED.

Moves volatile timestamp to the user message so the static system prompt
content is always the same prefix — KV cache is reused on every request.
"""
import datetime
import openai

client = openai.OpenAI()

SYSTEM_PROMPT = (
    "You are a senior support agent. Resolve tickets accurately and concisely. "
    "Follow company policy at all times."
)


def handle_ticket(ticket_text: str) -> str:
    """FIX: timestamp moved to user turn — system prompt prefix is now stable."""
    current_time = datetime.now().isoformat()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,  # FIX: pure static content, cache-friendly
            },
            {
                "role": "user",
                "content": f"[{current_time}] {ticket_text}",  # volatile in user turn
            },
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
