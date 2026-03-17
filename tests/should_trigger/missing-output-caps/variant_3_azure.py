"""
SHOULD TRIGGER missing-output-caps
Variant 3: Azure OpenAI SDK — chat.completions.create without a token cap.
The rule fires on any *.completions.create(...) regardless of which client object
is used.
"""
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://my-resource.openai.azure.com",
    api_version="2024-02-01",
    api_key="azure-key",
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain our SLA policy."},
    ],
)
print(response.choices[0].message.content)
