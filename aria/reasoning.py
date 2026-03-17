import openai
client = openai.OpenAI()

def reason_about(prompt: str) -> str:
    # VULN 2: missing-reasoning-parameters — no max_completion_tokens or reasoning_effort
    response = client.responses.create(model="o3", input=prompt)
    return response.output_text

def reason_hard(prompt: str) -> str:
    # VULN 3: reasoning-threshold-breach — hardcoded "high"
    response = client.responses.create(
        model="o3", input=prompt, reasoning_effort="high", max_completion_tokens=4096
    )
    return response.output_text
