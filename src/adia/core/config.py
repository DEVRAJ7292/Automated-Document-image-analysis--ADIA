from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration for ADIA (Gemini-only, strict).
    """

    # ─────────────────────────────
    # App
    # ─────────────────────────────
    APP_NAME: str = "ADIA"
    DEBUG: bool = True

    # ─────────────────────────────
    # Logging
    # ─────────────────────────────
    LOG_LEVEL: str = "INFO"

    # ─────────────────────────────
    # Paths
    # ─────────────────────────────
    DATA_DIR: Path = Path("data")

    # ─────────────────────────────
    # OCR (Tesseract)
    # ─────────────────────────────
    # Windows default path:
    # C:\\Program Files\\Tesseract-OCR\\tesseract.exe
    TESSERACT_CMD: str = "tesseract"

    # ─────────────────────────────
    # Gemini LLM
    # ─────────────────────────────
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",  # STRICT on purpose
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
