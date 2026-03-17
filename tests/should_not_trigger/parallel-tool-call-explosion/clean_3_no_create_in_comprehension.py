"""
SHOULD NOT TRIGGER parallel-tool-call-explosion
Clean 3: asyncio.gather over a list comprehension — but the comprehension does
not call .create() directly (calls a pre-built coroutine). The pattern requires
$CLIENT.create(...) to be the expression in the list comprehension.
"""
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()


async def make_request(text: str):
    return await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": text}],
        max_tokens=200,
    )


async def run_all(texts: list) -> list:
    # List comp contains make_request(t), not client.xxx.create(...)
    coros = [make_request(t) for t in texts]
    return await asyncio.gather(*coros)
