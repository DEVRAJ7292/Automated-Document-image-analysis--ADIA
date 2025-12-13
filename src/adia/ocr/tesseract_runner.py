from pathlib import Path
import subprocess
import tempfile

import pytesseract
from PIL import Image

from adia.core.config import get_settings
from adia.ocr.normalizer import OCRNormalizer


class TesseractRunner:
    """
    OCR runner with deterministic normalization.
    """

    def __init__(self):
        settings = get_settings()
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

    def extract_text_from_image(self, image_path: Path) -> str:
        image = Image.open(image_path)
        raw_text = pytesseract.image_to_string(image)
        return OCRNormalizer.normalize(raw_text).strip()

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        OCR a PDF using pdftoppm.
        """
        try:
            subprocess.run(
                ["pdftoppm", "-h"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except Exception:
            raise RuntimeError(
                "pdftoppm is not installed. "
                "Install Poppler for Windows and add it to PATH."
            )

        pages = []

        with tempfile.TemporaryDirectory() as tmpdir:
            prefix = Path(tmpdir) / "page"

            subprocess.run(
                ["pdftoppm", "-png", str(pdf_path), str(prefix)],
                check=True,
            )

            for img in sorted(Path(tmpdir).glob("page-*.png")):
                image = Image.open(img)
                raw_text = pytesseract.image_to_string(image)
                pages.append(OCRNormalizer.normalize(raw_text).strip())

        return "\n\n".join(pages)

    def extract(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()

        if suffix in {".png", ".jpg", ".jpeg"}:
            return self.extract_text_from_image(file_path)

        if suffix == ".pdf":
            return self.extract_text_from_pdf(file_path)

        raise ValueError(f"Unsupported file type: {suffix}")
