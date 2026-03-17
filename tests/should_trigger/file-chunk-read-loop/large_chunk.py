import openai
client = openai.OpenAI()

with open("data.log") as f:
    while True:
        chunk = f.read(4096)
        if not chunk:
            break
        client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": chunk}], max_tokens=50)
