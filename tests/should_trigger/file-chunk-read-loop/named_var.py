import openai
client = openai.OpenAI()

with open("report.txt") as fh:
    while True:
        piece = fh.read(2048)
        if not piece:
            break
        client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": piece}], max_tokens=200)
