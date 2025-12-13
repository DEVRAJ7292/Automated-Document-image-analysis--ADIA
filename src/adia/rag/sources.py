from typing import List, Dict


def format_sources(results: List[Dict]) -> List[Dict]:
    """
    Format retriever results into API-safe source citations.
    """

    sources = []

    for r in results:
        sources.append(
            {
                "document": r["metadata"].get("source"),
                "chunk": r["metadata"].get("chunk_id"),
                "similarity": round(r["score"], 3),
                "text_preview": r["text"][:200].strip(),
            }
        )

    return sources
