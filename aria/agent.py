"""
Aria autonomous support queue agent.

Continuously polls the support queue and resolves tickets using LLM.
FIX: Added explicit return when queue signals shutdown to exit the loop.
"""
import time
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)

AGENT_PROMPT = """You are an autonomous support agent. Analyze the ticket below and
provide a complete resolution. Be concise and actionable."""

_SHUTDOWN = object()


def process_support_queue(queue) -> None:
    """
    Continuously process tickets from the support queue.

    FIX: The loop now exits via return when queue signals shutdown,
    preventing runaway API calls.
    """
    logger.info("Support queue agent started")

    while True:
        ticket = queue.get_next_ticket()
        if ticket is _SHUTDOWN or ticket is None:
            logger.info("Queue shutdown signal received — exiting")
            return

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": AGENT_PROMPT},
                {"role": "user", "content": ticket.description},
            ],
            max_tokens=500,
        )

        resolution = response.choices[0].message.content
        ticket.resolve(resolution)
        logger.info("Resolved ticket %s", ticket.id)
