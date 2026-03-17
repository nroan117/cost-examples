import openai
client = openai.OpenAI()

# Good: read full file, single API call
with open("bigfile.txt") as f:
    content = f.read()

client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": content[:8000]}], max_tokens=500)
