"""
Aria ticket triage agent.

Uses the o3-mini reasoning model to classify incoming support tickets
and determine routing priority.
VULNERABILITY: reasoning-threshold-breach — reasoning_effort="high" hardcoded,
making every routine triage call maximally expensive.
"""
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)

TRIAGE_CATEGORIES = ["billing", "technical", "account", "general", "escalate"]

TRIAGE_PROMPT = f"""Classify the support ticket into one of these categories:
{', '.join(TRIAGE_CATEGORIES)}.

Return a JSON object: {{"category": "<category>", "priority": "low|medium|high", "summary": "<one sentence>"}}"""


def triage_ticket(ticket: dict) -> dict:
    """
    Classify a support ticket using the o3-mini reasoning model.

    BUG: reasoning_effort="high" is hardcoded for all tickets, including trivial ones
    like password resets. This should be "low" or "medium" for triage tasks,
    reserving "high" only for complex escalations.
    """
    response = client.responses.create(
        model="o3-mini",
        input=[
            {"role": "system", "content": TRIAGE_PROMPT},
            {"role": "user", "content": ticket["description"]},
        ],
        reasoning_effort="high",
        max_completion_tokens=2000,
    )

    logger.info("Triaged ticket %s", ticket.get("id"))
    return {
        "ticket_id": ticket.get("id"),
        "raw": response.output_text,
    }
