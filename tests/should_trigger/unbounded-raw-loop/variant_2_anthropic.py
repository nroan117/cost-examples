"""
SHOULD TRIGGER unbounded-raw-loop
Variant 2: Anthropic legacy completions.create inside while True with no exit.
Different SDK, same unbounded pattern.
"""
import anthropic

client = anthropic.Anthropic()


def monitor_feedback_stream(stream) -> None:
    while True:
        feedback = stream.next()

        response = client.completions.create(
            model="claude-2",
            prompt=f"\n\nHuman: Classify this feedback: {feedback}\n\nAssistant:",
            max_tokens_to_sample=100,
        )
        stream.emit_classification(response.completion)
