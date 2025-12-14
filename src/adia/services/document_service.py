from pathlib import Path

from adia.ocr.tesseract_runner import TesseractRunner
from adia.embeddings.singleton import embedder


class DocumentService:
    """
    Handles document ingestion.
    """

    def __init__(self):
        self.ocr_runner = TesseractRunner()

    def ingest(self, file_path: Path) -> None:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        text = self.ocr_runner.extract(file_path)

        if not text.strip():
            raise ValueError("OCR produced empty text")

        # ✅ USE GLOBAL EMBEDDER
        embedder.build_index(
            texts=[text],
            metadatas=[{"source": str(file_path)}],
        )
