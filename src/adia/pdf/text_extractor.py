from pathlib import Path
from typing import Optional

import pdfplumber


class PDFTextExtractor:
    """
    Native text extraction for PDFs.
    Falls back to OCR if extracted text is empty or invalid.
    """

    @staticmethod
    def extract_text(pdf_path: Path) -> Optional[str]:
        text_chunks = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text.strip())

        full_text = "\n\n".join(text_chunks).strip()
        return full_text if full_text else None
