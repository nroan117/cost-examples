"""
SHOULD NOT TRIGGER top-k-distance-breach
Clean 2: n_results=200 instead of top_k=200 — the rule pattern is specifically
`top_k=$N`, so a different parameter name does not trigger it.
This is also an edge case: high n_results is bad practice but not caught by rule.
"""
import chromadb

client = chromadb.Client()
collection = client.get_collection("docs")


def search_with_n_results(query: str) -> list:
    # Uses n_results, not top_k — rule does not fire.
    results = collection.query(
        query_texts=[query],
        n_results=200,
    )
    return results["documents"][0]
