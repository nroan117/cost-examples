"""
Aria escalation agent for complex support tickets.

Uses OpenAI o3 reasoning model to analyze difficult cases that tier-1 agents
could not resolve.
FIX: reasoning_effort="medium" and max_completion_tokens=4000 added.
"""
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)

ESCALATION_PROMPT = """You are a senior support specialist handling escalated tickets.
Analyze the full ticket history, identify root cause, and provide a detailed resolution
plan including any necessary account adjustments or refunds."""


def escalate_complex_ticket(ticket: dict) -> dict:
    """
    Escalate a complex support ticket to the o3 reasoning model.

    FIX: reasoning_effort="medium" is appropriate for most escalations.
    max_completion_tokens=4000 caps the thinking budget.
    """
    history_text = "\n".join(
        f"[{m['role']}]: {m['content']}" for m in ticket.get("history", [])
    )

    response = client.responses.create(
        model="o3",
        input=[
            {"role": "system", "content": ESCALATION_PROMPT},
            {
                "role": "user",
                "content": f"Ticket #{ticket['id']}\n\nHistory:\n{history_text}\n\nLatest: {ticket['description']}",
            },
        ],
        reasoning_effort="medium",
        max_completion_tokens=4000,
    )

    logger.info("Escalation resolved for ticket %s", ticket["id"])
    return {
        "ticket_id": ticket["id"],
        "resolution": response.output_text,
        "model": "o3",
    }
