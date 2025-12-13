from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np
import pickle


class FaissIndex:
    """
    FAISS index wrapper with metadata persistence.
    """

    def __init__(self, index_path: Path):
        self.index_path = index_path
        self.meta_path = index_path.with_suffix(".pkl")

        self.index = None
        self.texts: List[str] = []
        self.metadatas: List[Dict] = []

        if self.index_path.exists():
            self._load()

    def _load(self):
        self.index = faiss.read_index(str(self.index_path))
        with open(self.meta_path, "rb") as f:
            data = pickle.load(f)
            self.texts = data["texts"]
            self.metadatas = data["metadatas"]

    def add(
        self,
        embeddings: np.ndarray,
        texts: List[str],
        metadatas: List[Dict],
    ):
        if self.index is None:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)

        self.index.add(embeddings)
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def save(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))

        with open(self.meta_path, "wb") as f:
            pickle.dump(
                {
                    "texts": self.texts,
                    "metadatas": self.metadatas,
                },
                f,
            )
