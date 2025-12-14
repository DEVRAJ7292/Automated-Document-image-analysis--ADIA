from pathlib import Path
from typing import List, Dict

from sentence_transformers import SentenceTransformer

from adia.embeddings.faiss_index import FaissIndex


class Embedder:
    """
    Canonical embedding service for ADIA.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        index_path: Path = Path("data/embeddings/index.faiss"),
    ):
        self.model = SentenceTransformer(model_name)
        self.index = FaissIndex(index_path=index_path)

    def embed(self, texts: List[str]):
        if not texts:
            raise ValueError("No texts provided for embedding")

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

    def build_index(
        self,
        texts: List[str],
        metadatas: List[Dict],
    ) -> None:
        if len(texts) != len(metadatas):
            raise ValueError("texts and metadatas length mismatch")

        embeddings = self.embed(texts)
        self.index.add(embeddings, texts, metadatas)
