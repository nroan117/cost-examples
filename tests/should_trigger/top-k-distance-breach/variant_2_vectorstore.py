"""
SHOULD TRIGGER top-k-distance-breach
Variant 2: Generic vector store with top_k as a different large literal —
the rule fires on ANY literal integer value for top_k.
"""


def similarity_search(vectorstore, query_embedding: list, top_k: int = 50) -> list:
    # Even top_k=50 triggers the rule — the manifest enforces the actual threshold.
    return vectorstore.search(query_embedding, top_k=50)
