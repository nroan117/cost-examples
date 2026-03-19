"""
SHOULD NOT TRIGGER a2a-missing-message-budget
Variant 1: GroupChat with max_round set — message budget is bounded.
"""
import autogen

agent1 = autogen.AssistantAgent("assistant")
agent2 = autogen.UserProxyAgent("user")

# Good: GroupChat with max_round
groupchat = autogen.GroupChat(agents=[agent1, agent2], messages=[], max_round=10)
