class ADIAException(Exception):
    """
    Base exception for the ADIA platform.
    All custom exceptions must inherit from this.
    """

    def __init__(self, message: str, *, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConfigurationError(ADIAException):
    """Raised when application configuration is invalid."""


class OCRProcessingError(ADIAException):
    """Raised when OCR processing fails."""


class ExtractionError(ADIAException):
    """Raised when structured data extraction fails."""


class EmbeddingError(ADIAException):
    """Raised when embedding generation or indexing fails."""


class DatabaseError(ADIAException):
    """Raised when database operations fail."""
  