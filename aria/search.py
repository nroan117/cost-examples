def search(retriever, query: str) -> list:
    # VULN 9: top-k-distance-breach
    return retriever.retrieve(query=query, top_k=500)
