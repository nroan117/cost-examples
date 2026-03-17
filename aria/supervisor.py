"""
Aria multi-agent supervisor.

Orchestrates a team of specialised support sub-agents using LangGraph.
VULNERABILITY: missing-recursion-limit — StateGraph instantiated without recursion_limit,
allowing the graph to loop indefinitely if agents keep handing off to each other.
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator


class SupportState(TypedDict):
    ticket: str
    category: str
    resolution: str
    escalated: bool
    messages: Annotated[list, operator.add]


def triage_node(state: SupportState) -> dict:
    """Categorise the incoming ticket."""
    return {"category": "billing", "messages": ["triage complete"]}


def billing_node(state: SupportState) -> dict:
    """Handle billing-related tickets."""
    return {"resolution": "Billing resolved", "messages": ["billing handled"]}


def technical_node(state: SupportState) -> dict:
    """Handle technical support tickets."""
    return {"resolution": "Technical resolved", "messages": ["tech handled"]}


def build_supervisor():
    """
    Build the multi-agent support supervisor graph.

    BUG: StateGraph is created without recursion_limit. If routing logic
    cycles between agents, the graph will loop until the process runs out
    of memory or the user's API budget is exhausted.
    """
    workflow = StateGraph(SupportState)

    workflow.add_node("triage", triage_node)
    workflow.add_node("billing", billing_node)
    workflow.add_node("technical", technical_node)

    workflow.set_entry_point("triage")
    workflow.add_edge("billing", END)
    workflow.add_edge("technical", END)

    return workflow.compile()
