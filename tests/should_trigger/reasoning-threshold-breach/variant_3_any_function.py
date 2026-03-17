"""
SHOULD TRIGGER reasoning-threshold-breach
Variant 3: reasoning_effort="high" inside a non-SDK helper function —
the rule matches ANY call with reasoning_effort="high" as a kwarg, not
just responses.create.
"""


def configure_model_settings(model: str, reasoning_effort: str = "medium", **kwargs):
    return {"model": model, "reasoning_effort": reasoning_effort, **kwargs}


# Passes reasoning_effort="high" as a keyword argument — rule fires.
settings = configure_model_settings(
    model="o3-mini",
    reasoning_effort="high",
)
