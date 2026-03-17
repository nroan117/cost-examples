import openai
client = openai.OpenAI()

def process_request(user_input):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search",
                "parameters": {"type": "object", "properties": {"q": {"type": "string"}}}
            }
        }
    ]
    client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        max_tokens=300
    )
