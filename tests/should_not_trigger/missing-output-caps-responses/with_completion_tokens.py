import openai
client = openai.OpenAI()
# Good: max_completion_tokens is also a valid cap
response = client.responses.create(model="o3", input="Explain AI.", max_completion_tokens=2000)
print(response.output_text)
