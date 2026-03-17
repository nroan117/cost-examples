"""
SHOULD NOT TRIGGER top-k-distance-breach
Clean 3: top_k value comes from a config object — variable reference, not literal.
"""


def rag_retrieve(vectorstore, query_embedding: list, config) -> list:
    # config.top_k_max is a variable reference — metavariable-regex won't match.
    return vectorstore.search(query_embedding, top_k=config.top_k_max)
