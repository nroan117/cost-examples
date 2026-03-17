"""
SHOULD NOT TRIGGER unbounded-raw-loop
Clean 3: while <condition> (not while True) — the rule's pattern matches only
the literal `while True:` construct.
"""
from openai import OpenAI

client = OpenAI()


def process_queue_bounded(queue, max_items: int = 100) -> list:
    results = []
    processed = 0
    while processed < max_items and not queue.empty():
        item = queue.get()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": item}],
            max_tokens=100,
        )
        results.append(response.choices[0].message.content)
        processed += 1
    return results
