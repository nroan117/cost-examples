"""Tool handler — tool-schema-per-call vulnerability."""
import openai

client = openai.OpenAI()


def handle_request(user_input: str) -> str:
    """Define tools inline every call — bad pattern."""
    tools = [
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
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        max_tokens=500
    )
    return response.choices[0].message.content
