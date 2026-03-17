"""
SHOULD TRIGGER top-k-distance-breach
Variant 1: ChromaDB collection.query with top_k as a large literal integer.
"""
import chromadb

client = chromadb.Client()
collection = client.get_collection("knowledge_base")


def fetch_context(query: str) -> list:
    results = collection.query(
        query_texts=[query],
        top_k=200,
    )
    return results["documents"][0]
