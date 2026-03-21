# Aria LangChain agent — INTENTIONAL VULNERABILITY: verbose=True in production
# Full chain traces dumped to logs on every invocation — debug mode left in prod.
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Aria, a helpful customer support agent."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_openai_tools_agent(llm, [], prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[],
    verbose=True,  # noqa: COST007 — intentional: debug mode never removed
    max_iterations=10,
    handle_parsing_errors=True,
)


def handle_customer_message(message: str) -> str:
    result = agent_executor.invoke({"input": message, "chat_history": []})
    return result["output"]
