# Aria test suite — INTENTIONAL VULNERABILITY: missing test mock
# Tests hitting live LLM API without mocking add cost and flakiness.
import openai
import pytest

client = openai.OpenAI()


def test_aria_greeting_response():
    """Integration test — hits live API without mock."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Aria, a helpful support agent."},
            {"role": "user", "content": "Hello, I need help with my order."},
        ],
        max_tokens=100,
    )
    assert len(response.choices) > 0


def test_aria_refund_flow():
    """Test refund response path — hits live API without mock."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Aria, a helpful support agent."},
            {"role": "user", "content": "I want a refund."},
        ],
        max_tokens=100,
    )
    assert response.choices[0].message.content
