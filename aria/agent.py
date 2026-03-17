"""
Aria autonomous support queue agent.

Continuously polls the support queue and resolves tickets using LLM.
VULNERABILITY: unbounded-raw-loop — while True with .create() and no break/return/raise.
"""
import time
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)

AGENT_PROMPT = """You are an autonomous support agent. Analyze the ticket below and
provide a complete resolution. Be concise and actionable."""


def process_support_queue(queue) -> None:
    """
    Continuously process tickets from the support queue.

    BUG: This loop runs forever with no exit condition — any failure in queue.get_next_ticket()
    or the LLM call will not stop the loop, potentially generating infinite API calls.
    """
    logger.info("Support queue agent started")

    while True:
        ticket = queue.get_next_ticket()
        if not ticket:
            time.sleep(5)

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
