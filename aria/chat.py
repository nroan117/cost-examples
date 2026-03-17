import openai

# VULN 1: hardcoded-api-key
client = openai.OpenAI(api_key="sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz")

def chat(message: str) -> str:
    # VULN 6: missing-output-caps — no max_tokens variant
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": message}],
    )
    return response.choices[0].message.content
