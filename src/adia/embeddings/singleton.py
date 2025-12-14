from pathlib import Path
from adia.embeddings.embedder import Embedder

# ✅ SINGLE GLOBAL EMBEDDER (SOURCE OF TRUTH)
embedder = Embedder(
    index_path=Path("data/embeddings/index.faiss")
)
