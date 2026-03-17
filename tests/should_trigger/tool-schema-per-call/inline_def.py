import openai
client = openai.OpenAI()

def handle(msg):
    tools = [{"type": "function", "function": {"name": "lookup", "parameters": {}}}]
    client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": msg}], tools=tools, max_tokens=200)
