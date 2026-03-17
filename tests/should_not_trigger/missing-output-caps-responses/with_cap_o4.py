import openai
client = openai.OpenAI()
# Good: has max_output_tokens
response = client.responses.create(model="o4-mini", input="Explain AI.", max_output_tokens=1000)
print(response.output_text)
