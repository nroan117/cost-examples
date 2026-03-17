import openai
client = openai.OpenAI()

# Good: defined at module level
TOOLS = [{"type": "function", "function": {"name": "lookup", "parameters": {}}}]

def handle(msg):
    client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": msg}], tools=TOOLS, max_tokens=200)
