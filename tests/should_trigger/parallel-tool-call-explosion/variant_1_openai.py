"""
SHOULD TRIGGER parallel-tool-call-explosion
Variant 1: Classic unbounded asyncio.gather over a list comprehension of
chat.completions.create calls — no semaphore.
"""
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()


async def batch_summarise(tickets: list) -> None:
    tasks = [
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": t["description"]}],
            max_tokens=200,
        )
        for t in tickets
    ]
    await asyncio.gather(*tasks)
