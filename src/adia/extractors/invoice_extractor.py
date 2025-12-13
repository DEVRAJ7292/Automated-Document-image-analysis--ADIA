import re
from typing import Dict, Optional


class InvoiceExtractor:
    """
    Extract structured fields from invoice OCR text.
    """

    def extract(self, text: str) -> Dict:
        return {
            "invoice_number": self._extract_invoice_number(text),
            "invoice_date": self._extract_date(text),
            "total_amount": self._extract_total(text),
            "currency": self._extract_currency(text),
        }

    def _extract_invoice_number(self, text: str) -> Optional[str]:
        match = re.search(r"(invoice\s*no\.?|inv[\s\-:]*)\s*([A-Z0-9\-]+)", text, re.I)
        return match.group(2) if match else None

    def _extract_date(self, text: str) -> Optional[str]:
        match = re.search(
            r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})", text
        )
        return match.group(1) if match else None

    def _extract_total(self, text: str) -> Optional[float]:
        match = re.search(
            r"(total|amount\s*due|grand\s*total)[^\d]*(\d+(\.\d+)?)",
            text,
            re.I,
        )
        return float(match.group(2)) if match else None

    def _extract_currency(self, text: str) -> Optional[str]:
        if "₹" in text or "INR" in text:
            return "INR"
        if "$" in text or "USD" in text:
            return "USD"
        if "€" in text or "EUR" in text:
            return "EUR"
        return None
