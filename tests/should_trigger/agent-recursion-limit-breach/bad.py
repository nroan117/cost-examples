from langchain.agents import AgentExecutor
from crewai import Agent
import openai

client = openai.OpenAI()
msgs = []
app = None  # placeholder

# Pattern 1 — LangGraph high recursion_limit in invoke (> 100)
# ruleid: agent-recursion-limit-breach-high-value
result = app.invoke({"messages": []}, {"recursion_limit": 1000})

# ruleid: agent-recursion-limit-breach-high-value
result2 = app.stream({"messages": []}, config={"recursion_limit": 500})

# Pattern 2 — None disables guard entirely
# ruleid: agent-recursion-limit-breach-disabled
result3 = app.invoke({"messages": []}, {"recursion_limit": None})

# ruleid: agent-recursion-limit-breach-disabled
executor = AgentExecutor(agent=None, tools=[], max_iterations=None)

# ruleid: agent-recursion-limit-breach-disabled
researcher = Agent(role="Researcher", goal="Research topics", backstory="...", max_iter=None)

# Pattern 3 — AgentExecutor > 100
# ruleid: agent-recursion-limit-breach-agent-executor
executor2 = AgentExecutor(agent=None, tools=[], max_iterations=500)

# Pattern 4 — CrewAI > 100
# ruleid: agent-recursion-limit-breach-crewai
researcher2 = Agent(role="Researcher", goal="Research topics", backstory="...", max_iter=500)

# Pattern 5 — while True unbounded
# ruleid: agent-recursion-limit-breach-while-loop
while True:
    resp = client.chat.completions.create(model="gpt-4o", messages=msgs)
    msgs.append({"role": "assistant", "content": resp.choices[0].message.content})
