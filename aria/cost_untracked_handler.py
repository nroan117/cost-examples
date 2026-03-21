# Aria untracked handler — INTENTIONAL VULNERABILITY: missing cost tracking
# LLM calls with no observability — can't see spend, can't optimize.
import openai

client = openai.OpenAI()

SYSTEM_PROMPT = "You are Aria, a helpful customer support agent for TechCorp."


def handle_support_request(user_message: str, history: list) -> str:
    """Handle a customer message with no cost observability."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    # noqa: COST009 — intentional: no callbacks= or extra_headers=
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
    )
    return response.choices[0].message.content
