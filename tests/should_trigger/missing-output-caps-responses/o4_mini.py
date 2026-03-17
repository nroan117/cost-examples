import openai
client = openai.OpenAI()
response = client.responses.create(model="o4-mini", input="Write a complete novel.")
print(response.output_text)
