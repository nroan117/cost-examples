# Aria triage classifier — INTENTIONAL VULNERABILITY: excessive few-shot
# Uses 12 few-shot examples instead of 2-3, adding thousands of tokens per call.
import openai

client = openai.OpenAI()


def classify_ticket(ticket: str) -> str:
    """Classify support ticket intent using bloated few-shot prompt."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Aria. Classify support tickets."},
            {"role": "user", "content": "My package is late"},
            {"role": "assistant", "content": "shipping"},
            {"role": "user", "content": "I want a refund"},
            {"role": "assistant", "content": "returns"},
            {"role": "user", "content": "How do I reset my password?"},
            {"role": "assistant", "content": "account"},
            {"role": "user", "content": "My card was charged twice"},
            {"role": "assistant", "content": "billing"},
            {"role": "user", "content": "Where is my order?"},
            {"role": "assistant", "content": "shipping"},
            {"role": "user", "content": "I never got a confirmation email"},
            {"role": "assistant", "content": "account"},
            {"role": "user", "content": ticket},
        ],
        max_tokens=20,
    )
    return response.choices[0].message.content.strip()
