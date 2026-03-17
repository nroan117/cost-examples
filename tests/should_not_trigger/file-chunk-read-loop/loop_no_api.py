import openai
client = openai.OpenAI()

# Good: loop but no API call inside
lines = []
with open("data.txt") as f:
    while True:
        chunk = f.read(1024)
        if not chunk:
            break
        lines.append(chunk)

full_content = "".join(lines)
client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": full_content[:4000]}], max_tokens=300)
