"""
SHOULD NOT TRIGGER top-k-distance-breach
Clean 1: top_k receives a variable, not a literal integer — the metavariable-regex
^(0|[1-9][0-9]*)$ only matches literal integer tokens.
"""
import chromadb

client = chromadb.Client()
collection = client.get_collection("docs")

MAX_RESULTS = 10  # controlled by configuration


def search(query: str) -> list:
    results = collection.query(
        query_texts=[query],
        top_k=MAX_RESULTS,
    )
    return results["documents"][0]
