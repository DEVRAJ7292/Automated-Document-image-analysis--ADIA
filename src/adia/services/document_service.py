from pathlib import Path

from adia.ocr.tesseract_runner import TesseractRunner
from adia.embeddings.embedder import Embedder


class DocumentService:
    """
    Handles document ingestion:
    OCR → text → embeddings → FAISS
    """

    def __init__(self):
        self.ocr_runner = TesseractRunner()
        self.embedder = Embedder()

    def ingest(self, file_path: Path) -> None:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # 1. OCR
        text = self.ocr_runner.extract(file_path)
        if not text.strip():
            raise ValueError("OCR produced empty text")

        # 2. Save extracted text
        extracted_dir = Path("/app/data/extracted")
        extracted_dir.mkdir(parents=True, exist_ok=True)

        extracted_file = extracted_dir / f"{file_path.stem}.txt"
        extracted_file.write_text(text, encoding="utf-8")

        # 3. Build FAISS index (BLOCKING)
        self.embedder.build_index(
            texts=[text],
            metadatas=[{"source": str(file_path)}],
        )
