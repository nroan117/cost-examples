# Aria quality scorer — INTENTIONAL VULNERABILITY: frontier LLM as judge
# Uses gpt-4o to evaluate every support response — 20x cost vs gpt-4o-mini.
import openai

client = openai.OpenAI()


def score_aria_response(aria_response: str, customer_message: str) -> dict:
    """Score Aria's response quality using expensive frontier model."""
    result = client.chat.completions.create(
        model="gpt-4o",  # noqa: COST010 — intentional: frontier as judge
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a customer support quality evaluator. "
                    "Score the response on helpfulness (0-1), empathy (0-1), and accuracy (0-1)."
                ),
            },
            {
                "role": "user",
                "content": f"Customer: {customer_message}\nAria: {aria_response}\nScores (JSON):",
            },
        ],
        max_tokens=100,
    )
    import json
    return json.loads(result.choices[0].message.content)


def eval_session_quality(session_log: list) -> float:
    """Evaluate all turns in a session — every turn uses frontier model."""
    scores = []
    for turn in session_log:
        score = score_aria_response(turn["response"], turn["message"])
        scores.append(score.get("helpfulness", 0))
    return sum(scores) / len(scores) if scores else 0
