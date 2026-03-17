"""
Aria parallel ticket batch processor.

Processes a batch of incoming support tickets concurrently for throughput.
FIX: asyncio.Semaphore(5) limits concurrent LLM calls to prevent cost spikes.
"""
import asyncio
import logging
from openai import AsyncOpenAI

client = AsyncOpenAI()
logger = logging.getLogger(__name__)

BATCH_PROMPT = """You are a support agent. Provide a brief resolution for this ticket."""
MAX_CONCURRENCY = 5


async def process_ticket_batch(tickets: list) -> list[str]:
    """
    Process a batch of support tickets in parallel with bounded concurrency.

    FIX: Semaphore(5) ensures at most 5 concurrent API calls, preventing
    rate limit breaches and unexpected cost spikes on large batches.
    """
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

    async def bounded_call(ticket: dict) -> str:
        async with semaphore:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": BATCH_PROMPT},
                    {"role": "user", "content": ticket["description"]},
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content

    tasks = [bounded_call(ticket) for ticket in tickets]
    results = await asyncio.gather(*tasks)

    logger.info("Processed batch of %d tickets", len(tickets))
    return list(results)
