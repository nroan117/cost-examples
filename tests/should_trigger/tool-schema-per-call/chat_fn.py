import openai
client = openai.OpenAI()

def chat(question):
    tools = [{"type": "function", "function": {"name": "get_weather", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}}}]
    client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": question}], tools=tools, max_tokens=200)
