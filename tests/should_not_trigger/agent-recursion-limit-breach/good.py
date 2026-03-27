from langchain.agents import AgentExecutor
from crewai import Agent
import openai

client = openai.OpenAI()
msgs = []
app = None  # placeholder

# OK: LangGraph reasonable limit
result = app.invoke({"messages": []}, {"recursion_limit": 50})
result2 = app.stream({"messages": []}, config={"recursion_limit": 25})
result3 = app.invoke({"messages": []})  # no config = safe default

# OK: AgentExecutor with defaults or safe value
executor = AgentExecutor(agent=None, tools=[])
executor2 = AgentExecutor(agent=None, tools=[], max_iterations=20)

# OK: CrewAI with defaults or safe value
researcher = Agent(role="Researcher", goal="Research", backstory="...")
researcher2 = Agent(role="Researcher", goal="Research", backstory="...", max_iter=30)

# OK: while True with break
while True:
    resp = client.chat.completions.create(model="gpt-4o", messages=msgs)
    if resp.choices[0].finish_reason == "stop":
        break
