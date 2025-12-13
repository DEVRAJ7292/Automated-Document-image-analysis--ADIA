from pathlib import Path
from typing import List, Dict

import numpy as np

from adia.embeddings.embedder import Embedder
from adia.embeddings.faiss_index import FaissIndex


class SemanticRetriever:
    """
    Semantic search over embedded documents using FAISS.
    """

    def __init__(
        self,
        index_path: Path = Path("data/embeddings/index.faiss"),
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.embedder = Embedder(
            model_name=model_name,
            index_path=index_path,
        )
        self.index = FaissIndex(index_path=index_path)

    def query(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index.index is None:
            raise RuntimeError("FAISS index not found. Ingest documents first.")

        query_embedding = self.embedder.embed([query])

        distances, indices = self.index.index.search(
            query_embedding,
            top_k,
        )

        results: List[Dict] = []

        for rank, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.index.texts):
                continue

            # Convert FAISS distance to similarity score (deterministic)
            similarity = float(1 / (1 + distances[0][rank]))

            results.append(
                {
                    "text": self.index.texts[idx],
                    "metadata": self.index.metadatas[idx],
                    "score": similarity,
                }
            )

        return results
