"""
SHOULD TRIGGER missing-recursion-limit
Variant 1: LangGraph StateGraph without recursion_limit.
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    input: str
    output: str


def agent_node(state: AgentState) -> dict:
    return {"output": f"processed: {state['input']}"}


# No recursion_limit — the graph can cycle indefinitely.
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
app = graph.compile()
