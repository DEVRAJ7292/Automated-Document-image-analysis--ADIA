import re
from datetime import datetime


class OCRNormalizer:
    """
    Deterministic OCR normalization.
    No ML. No guessing. Safe corrections only.
    """

    CURRENT_YEAR = datetime.utcnow().year

    @staticmethod
    def normalize_dates(text: str) -> str:
        """
        Normalize dates like:
        12/12/2625 -> 12/12/2025
        12-12-2625 -> 12/12/2025
        """

        def fix(match):
            day, month, year = match.groups()
            year_int = int(year)

            # If OCR year is far in the future, snap to current century
            if year_int > OCRNormalizer.CURRENT_YEAR + 1:
                year_int = int(f"{OCRNormalizer.CURRENT_YEAR // 100}{year[-2:]}")

            return f"{day}/{month}/{year_int}"

        pattern = re.compile(r"\b(\d{2})[/-](\d{2})[/-](\d{4})\b")
        return pattern.sub(fix, text)

    @staticmethod
    def normalize_amounts(text: str) -> str:
        """
        Fix common OCR digit confusions.
        """
        replacements = {
            "O": "0",
            "o": "0",
            "l": "1",
            "I": "1",
            "S": "5",
        }

        for k, v in replacements.items():
            text = text.replace(k, v)

        return text

    @staticmethod
    def normalize(text: str) -> str:
        """
        Apply all normalization steps.
        """
        text = OCRNormalizer.normalize_dates(text)
        text = OCRNormalizer.normalize_amounts(text)
        return text
