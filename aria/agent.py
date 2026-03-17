from langgraph.graph import StateGraph
from autogen import ConversableAgent

def build_graph():
    # VULN 4a: missing-recursion-limit (StateGraph)
    return StateGraph(dict)

def build_agent():
    # VULN 4b: missing-recursion-limit (ConversableAgent)
    return ConversableAgent(name="aria", system_message="You are Aria.")
