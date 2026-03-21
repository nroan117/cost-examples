# Aria JSON extractor v2 — INTENTIONAL VULNERABILITY: inline JSON schema in prompt
# Schema injected as prompt text adds 300-800 tokens per call unnecessarily.
import openai

client = openai.OpenAI()


def extract_order_info(customer_message: str) -> dict:
    """Extract structured order info from customer message."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": 'You are Aria. Extract order information. Return JSON: {"type": "object", "properties": {"order_id": {"type": "string"}, "issue_type": {"type": "string"}, "urgency": {"type": "string"}}, "required": ["order_id", "issue_type", "urgency"]}',
            },
            {"role": "user", "content": customer_message},
        ],
        max_tokens=200,
    )
    import json
    return json.loads(response.choices[0].message.content)
