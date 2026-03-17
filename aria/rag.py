"""
Aria RAG-based knowledge base search.

Retrieves relevant support documents using vector similarity search.
FIX: top_k reduced to 10 (well within the recommended maximum).
"""
import chromadb

_chroma_client = chromadb.Client()
collection = _chroma_client.get_collection("support_docs")

TOP_K_MAX = 10  # Controlled constant; update via manifest if needed.


def search_knowledge_base(query: str) -> list[dict]:
    """
    Search the support knowledge base for documents relevant to a query.

    FIX: top_k=TOP_K_MAX (10) fetches a manageable context slice.
    """
    results = collection.query(
        query_texts=[query],
        top_k=TOP_K_MAX,
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
