import openai
client = openai.OpenAI()

with open("long_document.md") as f:
    document = f.read()

messages = [{"role": "user", "content": document}]
client.chat.completions.create(model="gpt-4-turbo", messages=messages)
