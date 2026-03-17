"""Tool handler — tool-schema-per-call FIXED."""
import openai

client = openai.OpenAI()

# FIX: define tools at module level so they're not re-transmitted every call
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    }
]


def handle_request(user_input: str) -> str:
    """Use module-level tool schema."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}],
        tools=TOOLS,
        max_tokens=500
    )
    return response.choices[0].message.content
