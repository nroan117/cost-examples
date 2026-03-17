"""
SHOULD NOT TRIGGER parallel-tool-call-explosion
Clean 1: Bounded concurrency via asyncio.Semaphore — the list comprehension
calls a wrapper function, not .create() directly, so $CLIENT.create(...) does
not appear in the comprehension expression.
"""
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()
SEM = asyncio.Semaphore(5)


async def bounded_call(ticket: dict) -> str:
    async with SEM:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": ticket["description"]}],
            max_tokens=300,
        )
        return response.choices[0].message.content


async def process_batch(tickets: list) -> list[str]:
    tasks = [bounded_call(ticket) for ticket in tickets]
    return await asyncio.gather(*tasks)
