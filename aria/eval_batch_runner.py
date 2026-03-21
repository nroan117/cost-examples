# Aria batch eval runner — INTENTIONAL VULNERABILITY: no eval cost cap
# For loop over full dataset with LLM calls — no budget check, can burn unbounded tokens.
import openai

client = openai.OpenAI()

# This could grow to millions of rows in production
EVAL_QUESTIONS = [
    "Where is my order?",
    "How do I return an item?",
    "I was charged incorrectly",
    "My account is locked",
    "Package never arrived",
    "How long does shipping take?",
    "Can I change my order?",
    "I need to cancel my subscription",
    "My product is defective",
    "How do I get a refund?",
]


def eval_aria_quality():
    """Evaluate Aria responses — no cost cap, no max samples."""
    results = []
    # noqa: COST011 — intentional: no budget check, no break on cost
    for question in EVAL_QUESTIONS:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Aria, a helpful customer support agent."},
                {"role": "user", "content": question},
            ],
            max_tokens=150,
        )
        results.append({
            "question": question,
            "response": response.choices[0].message.content,
        })
    return results
