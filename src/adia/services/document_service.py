from pathlib import Path

import pdfplumber

from adia.ocr.tesseract_runner import TesseractRunner
from adia.embeddings.embedder import Embedder


class DocumentService:
    """
    Handles document ingestion:
    - Save uploaded file
    - Native PDF text extraction (if possible)
    - OCR fallback
    - Embedding generation
    """

    def __init__(self):
        self.ocr_runner = TesseractRunner()
        self.embedder = Embedder()

    def _extract_text_from_pdf(self, file_path: Path) -> str | None:
        """
        Attempt native text extraction from PDF.
        Returns text if successful, else None.
        """
        try:
            text_chunks = []

            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_chunks.append(page_text.strip())

            text = "\n\n".join(text_chunks).strip()
            return text if text else None

        except Exception:
            # Silent fail → fallback to OCR
            return None

    def ingest(self, file_path: Path) -> None:
        """
        Ingest a document into the system.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            text: str | None = None

            # 1️⃣ Native PDF extraction first
            if file_path.suffix.lower() == ".pdf":
                text = self._extract_text_from_pdf(file_path)

            # 2️⃣ OCR fallback (PDF with no text OR images)
            if not text:
                text = self.ocr_runner.extract(file_path)

            if not text.strip():
                raise ValueError("Text extraction produced empty content")

            # 3️⃣ Save extracted text
            extracted_dir = Path("data/extracted")
            extracted_dir.mkdir(parents=True, exist_ok=True)

            extracted_file = extracted_dir / f"{file_path.stem}.txt"
            extracted_file.write_text(text, encoding="utf-8")

            # 4️⃣ Generate embeddings
            self.embedder.build_index(
                texts=[text],
                metadatas=[{"source": str(file_path)}],
            )

        except Exception as exc:
            # 🔥 DO NOT HIDE THE REAL ERROR
            raise RuntimeError(f"Ingestion failed: {exc}") from exc
