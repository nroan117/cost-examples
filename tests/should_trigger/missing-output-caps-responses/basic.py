import openai
client = openai.OpenAI()
response = client.responses.create(model="o3", input="Explain everything about AI.")
print(response.output_text)
