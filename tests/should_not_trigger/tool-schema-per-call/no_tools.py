import openai
client = openai.OpenAI()

def handle(msg):
    # Good: no tools parameter at all
    client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": msg}], max_tokens=200)
