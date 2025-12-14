from pathlib import Path
from typing import List, Dict

from adia.embeddings.embedder import Embedder
from adia.embeddings.faiss_index import FaissIndex


class SemanticRetriever:
    def __init__(
        self,
        index_path: Path = Path("/app/data/embeddings/index.faiss"),
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.embedder = Embedder(
            model_name=model_name,
            index_path=index_path,
        )
        self.index = FaissIndex(index_path=index_path)

    def query(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index.index is None:
            # ✅ DO NOT CRASH — DEMO SAFE
            return []

        query_embedding = self.embedder.embed([query])
        distances, indices = self.index.index.search(query_embedding, top_k)

        results: List[Dict] = []

        for idx in indices[0]:
            if idx < 0 or idx >= len(self.index.texts):
                continue

            results.append(
                {
                    "text": self.index.texts[idx],
                    "metadata": self.index.metadatas[idx],
                }
            )

        return results
