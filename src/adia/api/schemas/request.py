from typing import Optional, Literal
from pydantic import BaseModel, Field


class DocumentUploadRequest(BaseModel):
    """
    Metadata sent along with a document upload.

    The file itself is sent as multipart/form-data,
    this schema captures the semantic intent.
    """

    document_type: Literal["invoice", "resume", "contract"] = Field(
        ...,
        description="Type of document being uploaded"
    )

    source: Optional[str] = Field(
        default=None,
        description="Origin of the document (e.g. email, portal, scan)"
    )

    reference_id: Optional[str] = Field(
        default=None,
        description="External reference ID for traceability"
    )
