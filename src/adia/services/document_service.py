from pathlib import Path

from adia.ocr.tesseract_runner import TesseractRunner
from adia.embeddings.embedder import Embedder


class DocumentService:
    """
    Handles document ingestion:
    - OCR extraction
    - Embedding generation (in-memory for demo)
    """

    def __init__(self):
        self.ocr_runner = TesseractRunner()
        self.embedder = Embedder()

    def ingest(self, file_path: Path) -> None:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        text = self.ocr_runner.extract(file_path)

        if not text.strip():
            raise ValueError("OCR produced empty text")

        self.embedder.build_index(
            texts=[text],
            metadatas=[{"source": str(file_path)}],
        )
