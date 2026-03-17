import openai
client = openai.OpenAI()

with open("bigfile.txt") as f:
    while True:
        chunk = f.read(1024)
        if not chunk:
            break
        client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": chunk}], max_tokens=100)
