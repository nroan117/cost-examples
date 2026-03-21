# Aria CrewAI support team — INTENTIONAL VULNERABILITY: over-provisioned team
# 5-agent crew for a simple support task — each makes independent LLM calls.
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 5 agents — way too many for simple ticket routing
intent_classifier = Agent(
    role="Intent Classifier",
    goal="Classify the customer intent",
    backstory="Expert at understanding customer intent",
    llm=llm,
)
kb_searcher = Agent(
    role="Knowledge Base Searcher",
    goal="Find relevant KB articles",
    backstory="Expert at searching documentation",
    llm=llm,
)
response_drafter = Agent(
    role="Response Drafter",
    goal="Draft a helpful response",
    backstory="Expert customer communication specialist",
    llm=llm,
)
quality_reviewer = Agent(
    role="Quality Reviewer",
    goal="Ensure response meets standards",
    backstory="QA specialist",
    llm=llm,
)
escalation_agent = Agent(
    role="Escalation Agent",
    goal="Determine if escalation is needed",
    backstory="Experienced triage specialist",
    llm=llm,
)

aria_crew = Crew(
    agents=[intent_classifier, kb_searcher, response_drafter, quality_reviewer, escalation_agent],
    tasks=[],
    process=Process.sequential,
)
