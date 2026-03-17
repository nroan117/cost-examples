import asyncio
import openai
client = openai.AsyncOpenAI()

async def process_all(items: list) -> list:
    # VULN 7: parallel-tool-call-explosion
    tasks = [
        client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": i}])
        for i in items
    ]
    return await asyncio.gather(*tasks)
