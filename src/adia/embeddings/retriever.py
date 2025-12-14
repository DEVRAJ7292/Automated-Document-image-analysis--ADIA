from typing import List, Dict

from adia.embeddings.singleton import embedder


class SemanticRetriever:
    """
    Semantic search over embedded documents.
    """

    def query(self, query: str, top_k: int = 5) -> List[Dict]:
        if embedder.index.index is None:
            return []

        query_embedding = embedder.embed([query])

        distances, indices = embedder.index.index.search(
            query_embedding,
            top_k,
        )

        results: List[Dict] = []

        for rank, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(embedder.index.texts):
                continue

            results.append(
                {
                    "text": embedder.index.texts[idx],
                    "metadata": embedder.index.metadatas[idx],
                    "score": float(1 / (1 + distances[0][rank])),
                }
            )

        return results
