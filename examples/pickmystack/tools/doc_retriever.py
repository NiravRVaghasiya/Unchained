"""
Doc Retriever Tool — Searches curated framework documentation.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from unchained import tool, RAG


# Singleton RAG instance
_rag = None


def _get_rag() -> RAG:
    """Lazy-load the knowledge base."""
    global _rag
    if _rag is None:
        _rag = RAG()
        knowledge_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "knowledge"
        )
        if os.path.exists(knowledge_dir):
            for filename in os.listdir(knowledge_dir):
                if filename.endswith((".md", ".txt")):
                    filepath = os.path.join(knowledge_dir, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    _rag.add(content, metadata={"source": filename})
    return _rag


@tool
def retrieve_docs(query: str, top_k: int = 3) -> str:
    """Search the curated framework knowledge base for relevant information.

    Args:
        query: What to search for (e.g., 'best framework for RAG')
        top_k: Number of results to return
    """
    rag = _get_rag()
    results = rag.search(query, top_k=top_k)

    if not results:
        return "No relevant documentation found for this query."

    output = f"## Search Results for: '{query}'\n\n"
    for i, r in enumerate(results, 1):
        source = r["metadata"].get("source", "unknown")
        output += f"### Result {i} (score: {r['score']}) — {source}\n"
        output += f"{r['text'][:500]}...\n\n"

    return output
