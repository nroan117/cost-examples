"""
SHOULD TRIGGER a2a-missing-message-budget
Variant 1: GroupChat instantiated without max_round — unbounded message budget.
"""
import autogen

agent1 = autogen.AssistantAgent("assistant")
agent2 = autogen.UserProxyAgent("user")

# Bad: GroupChat without max_round
groupchat = autogen.GroupChat(agents=[agent1, agent2], messages=[])
