"""
Aria RAG-based knowledge base search.

Retrieves relevant support documents using vector similarity search.
VULNERABILITY: top-k-distance-breach — top_k=200 far exceeds recommended maximum.
"""
import chromadb

_chroma_client = chromadb.Client()
collection = _chroma_client.get_collection("support_docs")


def search_knowledge_base(query: str) -> list[dict]:
    """
    Search the support knowledge base for documents relevant to a query.

    BUG: top_k=200 retrieves an enormous context window worth of documents.
    This inflates the number of tokens sent to the LLM and increases cost
    proportionally. Recommended maximum is 20.
    """
    results = collection.query(
        query_texts=[query],
        top_k=200,
    )

    documents = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        documents.append({"content": doc, "metadata": meta, "distance": dist})

    return documents


def index_document(doc_id: str, content: str, metadata: dict) -> None:
    """Index a support document into the knowledge base."""
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[doc_id],
    )
