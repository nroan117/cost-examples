"""
SHOULD TRIGGER unbounded-raw-loop
Variant 3: The .create() call is nested inside a conditional — semgrep's `...`
matches any intervening statements, so the loop still triggers.
"""
import logging
from openai import OpenAI

client = OpenAI()
logger = logging.getLogger(__name__)


def live_moderation_loop(feed) -> None:
    while True:
        post = feed.get()
        if post is None:
            logger.debug("Empty feed, waiting...")
            feed.wait()

        if post.needs_moderation:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Is this post policy-violating? Reply YES or NO."},
                    {"role": "user", "content": post.content},
                ],
                max_tokens=10,
            )
            feed.set_moderation(post.id, response.choices[0].message.content.strip())
