import openai
client = openai.OpenAI()
# Good: using completions.create, not responses.create (different rule handles this)
response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": "Hello"}], max_tokens=100)
print(response.choices[0].message.content)
