"""
Aria structured field extractor.

Extracts structured JSON fields from unstructured support ticket descriptions
using an LLM with retry logic for malformed outputs.
FIX: Bounded for loop (range(MAX_RETRIES)) replaces while True.
"""
import json
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)

MAX_RETRIES = 3

EXTRACTION_PROMPT = """Extract the following fields from the support ticket as valid JSON:
{
  "customer_name": "<name or null>",
  "product": "<product name or null>",
  "issue_type": "<bug|feature_request|billing|other>",
  "urgency": "<low|medium|high>"
}
Return ONLY the JSON object, no explanation."""


def extract_ticket_fields(description: str) -> dict:
    """
    Extract structured fields from a ticket description.

    FIX: for attempt in range(MAX_RETRIES) caps retries at 3, preventing
    an indefinite loop when the model returns bad JSON.
    """
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": description},
            ],
            max_tokens=200,
        )
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as exc:
            logger.warning("Attempt %d/%d: malformed JSON", attempt + 1, MAX_RETRIES)
            last_error = exc

    raise ValueError(f"Could not extract JSON after {MAX_RETRIES} attempts") from last_error
