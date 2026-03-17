"""
Aria parallel ticket batch processor.

Processes a batch of incoming support tickets concurrently for throughput.
VULNERABILITY: parallel-tool-call-explosion — asyncio.gather over an unbounded
list comprehension of .create() calls with no semaphore to cap concurrency.
"""
import asyncio
import logging
from openai import AsyncOpenAI

client = AsyncOpenAI()
logger = logging.getLogger(__name__)

BATCH_PROMPT = """You are a support agent. Provide a brief resolution for this ticket."""


async def process_ticket_batch(tickets: list) -> list[str]:
    """
    Process a batch of support tickets in parallel.

    BUG: Every ticket spawns an independent LLM call with no concurrency cap.
    A batch of 500 tickets fires 500 simultaneous API requests, blowing through
    rate limits and generating an enormous parallel cost spike.
    """
    tasks = [
        client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": BATCH_PROMPT},
                {"role": "user", "content": ticket["description"]},
            ],
            max_tokens=300,
        )
        for ticket in tickets
    ]
    await asyncio.gather(*tasks)

    logger.info("Processed batch of %d tickets", len(tickets))
    return [t["id"] for t in tickets]
