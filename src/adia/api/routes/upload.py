from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from adia.services.document_service import DocumentService

router = APIRouter()


@router.post("/upload", summary="Upload and ingest a document")
async def upload_document(file: UploadFile = File(...)):
    upload_dir = Path("data/raw")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        service = DocumentService()
        service.ingest(file_path)

        return {
            "status": "success",
            "filename": file.filename,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
