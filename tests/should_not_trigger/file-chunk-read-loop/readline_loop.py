import openai
client = openai.OpenAI()

# Good: reading by line (not f.read(N)), and not calling API in the loop
all_lines = []
with open("data.txt") as f:
    for line in f:
        all_lines.append(line.strip())

client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": "\n".join(all_lines[:100])}], max_tokens=300)
