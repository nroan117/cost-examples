import openai
client = openai.OpenAI()
# Good: has max_output_tokens
response = client.responses.create(model="o3", input="Explain AI.", max_output_tokens=500)
print(response.output_text)
