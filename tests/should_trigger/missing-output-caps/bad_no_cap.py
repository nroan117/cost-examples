import openai

client = openai.OpenAI()

def get_response(user_message: str) -> str:
    # Missing max_tokens — unbounded output
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content
