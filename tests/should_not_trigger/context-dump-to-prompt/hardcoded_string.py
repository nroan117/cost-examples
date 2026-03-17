import openai
client = openai.OpenAI()

# Good: hardcoded string, not from file read
messages = [{"role": "user", "content": "What is the capital of France?"}]
client.chat.completions.create(model="gpt-4o", messages=messages, max_tokens=100)
