from pathlib import Path

from fastapi import APIRouter, HTTPException

from adia.api.schemas.query import QueryRequest, QueryResponse
from adia.rag.chain import RAGChain
from adia.db.database import SessionLocal
from adia.db.crud import log_query

router = APIRouter()


@router.post(
    "/query",
    summary="Ask questions over uploaded documents",
    response_model=QueryResponse,
)
def query_documents(payload: QueryRequest):
    db = SessionLocal()
    try:
        rag = RAGChain(
            embeddings_path=Path("data/embeddings/index.faiss")
        )

        result = rag.answer(payload.question)

        # 🔑 FIX: store only text, not dict
        answer_text = (
            result["answer"]
            if isinstance(result, dict)
            else result
        )

        log_query(
            db=db,
            question=payload.question,
            answer=answer_text,
        )

        return QueryResponse(answer=answer_text)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
    finally:
        db.close()
