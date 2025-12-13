from pathlib import Path
from typing import List

from PIL import Image
import mimetypes

from adia.core.exceptions import OCRProcessingError


SUPPORTED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}
SUPPORTED_PDF_TYPE = "application/pdf"


def detect_mime_type(file_path: Path) -> str:
    """
    Detect MIME type of a file based on its extension.

    This is used to decide whether:
    - file can be OCRed directly (image)
    - file must be converted (PDF)
    """

    mime_type, _ = mimetypes.guess_type(file_path)

    if not mime_type:
        raise OCRProcessingError(
            f"Unable to detect MIME type for file: {file_path.name}"
        )

    return mime_type


def load_image(file_path: Path) -> Image.Image:
    """
    Load an image file into a PIL Image object.

    Raises a controlled error if the image cannot be opened.
    """

    try:
        image = Image.open(file_path)
        image.load()  # force load to catch corrupt images early
        return image
    except Exception as exc:
        raise OCRProcessingError(
            f"Failed to load image file: {file_path.name}"
        ) from exc


def pdf_to_images(file_path: Path) -> List[Image.Image]:
    """
    Convert a PDF file into a list of PIL Image objects (one per page).

    NOTE:
    - Uses Pillow's built-in PDF support
    - Suitable for text-based and scanned PDFs
    """

    try:
        images: List[Image.Image] = []

        with Image.open(file_path) as pdf:
            for page_index in range(pdf.n_frames):
                pdf.seek(page_index)
                images.append(pdf.convert("RGB"))

        if not images:
            raise OCRProcessingError(
                f"No pages found in PDF: {file_path.name}"
            )

        return images

    except Exception as exc:
        raise OCRProcessingError(
            f"Failed to convert PDF to images: {file_path.name}"
        ) from exc


def prepare_images_for_ocr(file_path: Path) -> List[Image.Image]:
    """
    Entry-point utility to normalize input files for OCR.

    Returns a list of images regardless of input type.
    """

    mime_type = detect_mime_type(file_path)

    if mime_type in SUPPORTED_IMAGE_TYPES:
        return [load_image(file_path)]

    if mime_type == SUPPORTED_PDF_TYPE:
        return pdf_to_images(file_path)

    raise OCRProcessingError(
        f"Unsupported file type for OCR: {mime_type}"
    )
