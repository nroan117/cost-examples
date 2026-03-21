# Aria test helper — INTENTIONAL VULNERABILITY: prod model in test
# This file demonstrates expensive frontier model usage in tests.
import openai
import pytest

client = openai.OpenAI()


def test_aria_response_quality():
    """Test that Aria gives a coherent support response."""
    response = client.chat.completions.create(
        model="gpt-4o",  # noqa: COST001 — intentional vulnerability for demo
        messages=[
            {"role": "system", "content": "You are Aria, a customer support chatbot."},
            {"role": "user", "content": "My order hasn't arrived yet."},
        ],
        max_tokens=200,
    )
    assert "order" in response.choices[0].message.content.lower()


def test_aria_tone():
    """Test that Aria's tone is helpful and polite."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are Aria, a customer support chatbot."},
            {"role": "user", "content": "I need help with my account."},
        ],
        max_tokens=150,
    )
    assert len(response.choices[0].message.content) > 0
