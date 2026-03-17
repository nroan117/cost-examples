"""
SHOULD NOT TRIGGER parallel-tool-call-explosion
Clean 2: Sequential for-loop instead of parallel gather — no asyncio.gather at all.
"""
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()


async def process_sequentially(tickets: list) -> list[str]:
    results = []
    for ticket in tickets:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": ticket["description"]}],
            max_tokens=300,
        )
        results.append(response.choices[0].message.content)
    return results
