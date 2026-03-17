"""
Aria escalation agent for complex support tickets.

Uses OpenAI o3 reasoning model to analyze difficult cases that tier-1 agents
could not resolve.
VULNERABILITY: missing-reasoning-parameters — responses.create called without
reasoning_effort or max_completion_tokens.
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

    BUG: missing reasoning_effort and max_completion_tokens — the reasoning model
    will use its default (maximum) thinking budget, generating unbounded thinking
    tokens on every escalation even for straightforward cases.
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
    )

    logger.info("Escalation resolved for ticket %s", ticket["id"])
    return {
        "ticket_id": ticket["id"],
        "resolution": response.output_text,
        "model": "o3",
    }
