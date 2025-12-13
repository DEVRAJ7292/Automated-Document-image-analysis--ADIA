import re
from typing import Dict, Optional


class ContractExtractor:
    """
    Extract key entities from contract OCR text.
    """

    def extract(self, text: str) -> Dict:
        return {
            "party_a": self._extract_party(text, "party a"),
            "party_b": self._extract_party(text, "party b"),
            "effective_date": self._extract_date(text),
            "termination_clause_present": self._has_termination_clause(text),
        }

    def _extract_party(self, text: str, label: str) -> Optional[str]:
        match = re.search(
            rf"{label}[:\-]?\s*(.+)",
            text,
            re.I,
        )
        return match.group(1).strip() if match else None

    def _extract_date(self, text: str) -> Optional[str]:
        match = re.search(
            r"(effective\s*date|dated)[^\d]*(\d{2}[\/\-]\d{2}[\/\-]\d{4})",
            text,
            re.I,
        )
        return match.group(2) if match else None

    def _has_termination_clause(self, text: str) -> bool:
        keywords = ["termination", "terminate", "termination clause"]
        lower = text.lower()
        return any(k in lower for k in keywords)
