import openai
client = openai.OpenAI()

# Good: truncated content
with open("doc.txt") as f:
    content = f.read()[:2000]

messages = [{"role": "user", "content": content}]
client.chat.completions.create(model="gpt-4o", messages=messages, max_tokens=500)
