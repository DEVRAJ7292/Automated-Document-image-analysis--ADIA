from pathlib import Path
from typing import List, Dict

from adia.embeddings.embedder import Embedder
from adia.embeddings.faiss_index import FaissIndex


# ✅ GLOBAL IN-MEMORY FAISS (HF-SAFE)
_FAISS_INDEX = None


class SemanticRetriever:
    """
    Semantic search over embedded documents using FAISS.
    """

    def __init__(
        self,
        index_path: Path = Path("data/embeddings/index.faiss"),
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        global _FAISS_INDEX

        self.embedder = Embedder(
            model_name=model_name,
            index_path=index_path,
        )

        if _FAISS_INDEX is None:
            _FAISS_INDEX = self.embedder.index

        self.index = _FAISS_INDEX

    def query(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index.index is None:
            return []

        query_embedding = self.embedder.embed([query])

        distances, indices = self.index.index.search(
            query_embedding,
            top_k,
        )

        results: List[Dict] = []

        for rank, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.index.texts):
                continue

            results.append(
                {
                    "text": self.index.texts[idx],
                    "metadata": self.index.metadatas[idx],
                    "score": float(1 / (1 + distances[0][rank])),
                }
            )

        return results
