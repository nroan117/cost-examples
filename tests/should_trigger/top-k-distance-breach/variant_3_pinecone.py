"""
SHOULD TRIGGER top-k-distance-breach
Variant 3: Pinecone-style index query with top_k set to an absurdly high literal.
"""


def query_index(index, query_vector: list) -> dict:
    # Querying 500 results will flood the LLM context window.
    return index.query(vector=query_vector, top_k=500, include_metadata=True)
