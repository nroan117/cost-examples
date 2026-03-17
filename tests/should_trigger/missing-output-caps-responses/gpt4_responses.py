import openai
client = openai.OpenAI()
response = client.responses.create(model="gpt-4o", input="Tell me everything.")
print(response.output_text)
