"""
SHOULD NOT TRIGGER missing-recursion-limit
Clean 3: Custom agent class — neither StateGraph nor ConversableAgent is used,
so the rule's pattern-either does not match at all.
"""
from openai import OpenAI
from dataclasses import dataclass, field


@dataclass
class SimpleAgent:
    """A minimal agent with a hard-coded step limit."""
    name: str
    max_steps: int = 10
    client: OpenAI = field(default_factory=OpenAI)

    def run(self, task: str) -> str:
        for step in range(self.max_steps):
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": task}],
                max_tokens=500,
            )
            result = response.choices[0].message.content
            if "[DONE]" in result:
                return result
        return "max steps reached"
