import re
from typing import Dict, List


class ResumeExtractor:
    """
    Extract structured fields from resume OCR text.
    """

    def extract(self, text: str) -> Dict:
        return {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "skills": self._extract_skills(text),
        }

    def _extract_name(self, text: str) -> str | None:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return lines[0] if lines else None

    def _extract_email(self, text: str) -> str | None:
        match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> str | None:
        match = re.search(r"\+?\d[\d\s\-]{8,}\d", text)
        return match.group(0) if match else None

    def _extract_skills(self, text: str) -> List[str]:
        skills_keywords = [
            "python", "java", "sql", "machine learning", "deep learning",
            "fastapi", "docker", "aws", "tensorflow", "pytorch"
        ]
        found = []
        lower = text.lower()
        for skill in skills_keywords:
            if skill in lower:
                found.append(skill)
        return found
