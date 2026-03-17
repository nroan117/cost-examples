"""
SHOULD TRIGGER parallel-tool-call-explosion
Variant 2: Different variable names (calls / items) — semgrep metavariables
$TASKS, $ITEM, $ITEMS bind to any names, so the pattern still fires.
"""
import asyncio
from openai import AsyncOpenAI

llm = AsyncOpenAI()


async def bulk_classify(items: list) -> None:
    calls = [
        llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": item["text"]}],
            max_tokens=50,
        )
        for item in items
    ]
    await asyncio.gather(*calls)
