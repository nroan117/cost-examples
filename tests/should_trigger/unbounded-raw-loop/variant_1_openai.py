"""
SHOULD TRIGGER unbounded-raw-loop
Variant 1: OpenAI chat.completions.create inside while True with no exit.
Processes a queue indefinitely, no break/return/raise anywhere in the loop.
"""
import time
from openai import OpenAI

client = OpenAI()


def run_queue_agent(queue) -> None:
    while True:
        item = queue.pop()
        if not item:
            time.sleep(1)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": item}],
            max_tokens=500,
        )
        queue.mark_done(item, response.choices[0].message.content)
