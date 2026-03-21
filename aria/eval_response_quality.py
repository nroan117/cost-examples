# Aria eval — INTENTIONAL VULNERABILITY: eval hitting production API
# Every evaluation call runs against the live OpenAI API, burning real budget.
import openai

client = openai.OpenAI()  # production API key — no staging/mock

EVAL_QUESTIONS = [
    ("Where is my order #12345?", "It appears your order is still processing..."),
    ("I never received my refund", "I apologize for the delay with your refund..."),
    ("My password doesn't work", "Let me help you reset your password..."),
    ("I was charged twice", "I can see there may have been a duplicate charge..."),
    ("Package arrived damaged", "I'm sorry to hear your package arrived damaged..."),
]


def eval_aria_responses():
    """Evaluate Aria's responses — all hitting production API."""
    results = []
    for question, expected_theme in EVAL_QUESTIONS:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Aria, a helpful support agent."},
                {"role": "user", "content": question},
            ],
            max_tokens=200,
        )
        actual = response.choices[0].message.content
        results.append({"question": question, "response": actual})
    return results
