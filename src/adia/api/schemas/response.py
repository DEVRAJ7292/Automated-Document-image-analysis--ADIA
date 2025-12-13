from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """
    Response returned after a document is accepted.
    """

    document_id: str = Field(
        ...,
        description="Internal unique identifier for the document"
    )

    status: str = Field(
        ...,
        description="Current processing status"
    )

    received_at: datetime = Field(
        ...,
        description="Timestamp when document was received"
    )

    message: Optional[str] = Field(
        default=None,
        description="Optional human-readable message"
    )
