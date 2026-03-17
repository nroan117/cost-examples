"""
Aria ticket triage agent.

Uses the o3-mini reasoning model to classify incoming support tickets
and determine routing priority.
FIX: reasoning_effort changed from "high" to "medium" — appropriate for routine triage.
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

    FIX: reasoning_effort="medium" is sufficient for triage tasks.
    "high" is reserved for complex escalations only.
    """
    response = client.responses.create(
        model="o3-mini",
        input=[
            {"role": "system", "content": TRIAGE_PROMPT},
            {"role": "user", "content": ticket["description"]},
        ],
        reasoning_effort="medium",
        max_completion_tokens=2000,
    )

    logger.info("Triaged ticket %s", ticket.get("id"))
    return {
        "ticket_id": ticket.get("id"),
        "raw": response.output_text,
    }
