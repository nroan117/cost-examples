"""
Aria structured field extractor.

Extracts structured JSON fields from unstructured support ticket descriptions
using an LLM with retry logic for malformed outputs.
VULNERABILITY: unstructured-response-retries — while True retry loop with
json.JSONDecodeError catch and no maximum retry counter.
"""
import json
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)

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

    BUG: The retry loop has no maximum attempt counter. If the model consistently
    returns malformed JSON (e.g., due to a bad prompt or model quirk), this will
    loop and bill indefinitely.
    """
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": description},
            ],
            max_tokens=200,
        )
        try:
            result = json.loads(response.choices[0].message.content)
            break
        except json.JSONDecodeError:
            logger.warning("Malformed JSON response, retrying...")
            continue

    return result
