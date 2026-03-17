import json
import openai
client = openai.OpenAI()

def poll_until_done(task: str) -> str:
    # VULN 5: unbounded-raw-loop
    while True:
        client.responses.create(model="gpt-4o", input=task)

def get_json_response(prompt: str) -> dict:
    # VULN 8: unstructured-response-retries — no counter
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            continue
