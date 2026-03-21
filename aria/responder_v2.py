# Aria responder v2 — INTENTIONAL VULNERABILITY: hardcoded model, no env routing
# Every call uses gpt-4o regardless of task complexity.
import openai

client = openai.OpenAI()


def classify_intent(message: str) -> str:
    """Classify user intent — simple task using expensive model."""
    response = client.chat.completions.create(
        model="gpt-4o",  # noqa: COST003 — intentional vulnerability
        messages=[
            {"role": "system", "content": "Classify user intent as: billing, shipping, returns, other."},
            {"role": "user", "content": message},
        ],
        max_tokens=20,
    )
    return response.choices[0].message.content.strip()


def generate_response(intent: str, context: str) -> str:
    """Generate support response — complex task also using gpt-4o (same model!)."""
    response = client.chat.completions.create(
        model="gpt-4o",  # noqa: COST003 — same expensive model for all tasks
        messages=[
            {"role": "system", "content": "You are Aria, a helpful customer support agent."},
            {"role": "user", "content": f"Intent: {intent}\nContext: {context}\nProvide a helpful response."},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content
