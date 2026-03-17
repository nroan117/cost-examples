import openai
client = openai.OpenAI()

with open("doc.txt") as f:
    content = f.read()

messages = [{"role": "user", "content": content}]
client.chat.completions.create(model="gpt-4o", messages=messages)
