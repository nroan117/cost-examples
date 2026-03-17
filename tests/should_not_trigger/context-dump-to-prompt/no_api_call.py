import openai
client = openai.OpenAI()

# Good: file read but no messages array sent to API
with open("data.txt") as f:
    content = f.read()

print(content[:100])
