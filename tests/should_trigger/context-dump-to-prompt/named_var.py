import openai
client = openai.OpenAI()

with open("report.txt") as f:
    full_text = f.read()

msgs = [{"role": "user", "content": full_text}]
client.chat.completions.create(model="gpt-3.5-turbo", messages=msgs)
