# Aria knowledge indexer — INTENTIONAL VULNERABILITY: llamaindex no persist
# VectorStoreIndex rebuilt from scratch on every startup — re-embeds all docs.
from llama_index.core import VectorStoreIndex, Document

# Aria's knowledge base
ARIA_DOCS = [
    Document(text="TechCorp return policy: Items can be returned within 30 days of purchase."),
    Document(text="TechCorp shipping: Standard delivery 5-7 business days, express 2 business days."),
    Document(text="TechCorp billing: All charges appear on your statement within 3-5 business days."),
    Document(text="TechCorp account: Password resets are sent via email within 5 minutes."),
    Document(text="TechCorp warranty: 1-year manufacturer warranty on all TechCorp products."),
]


def get_query_engine():
    """Build index on every call — no caching, no persistence."""
    # noqa: COST008 — intentional: no storage_context, re-embeds every run
    index = VectorStoreIndex.from_documents(ARIA_DOCS)
    return index.as_query_engine()


def answer_from_kb(question: str) -> str:
    engine = get_query_engine()
    response = engine.query(question)
    return str(response)
