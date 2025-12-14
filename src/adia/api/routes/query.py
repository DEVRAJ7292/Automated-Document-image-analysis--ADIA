from pathlib import Path
from fastapi import APIRouter, HTTPException

from adia.api.schemas.query import QueryRequest, QueryResponse
from adia.rag.chain import RAGChain

router = APIRouter()


@router.post(
    "/query",
    summary="Ask questions over uploaded documents",
    response_model=QueryResponse,
)
def query_documents(payload: QueryRequest):
    try:
        rag = RAGChain(
            embeddings_path=Path("data/embeddings/index.faiss")
        )

        result = rag.answer(payload.question)

        # ✅ Normalize output for UI
        if isinstance(result, dict):
            answer_text = result.get("answer", "No answer found.")
        else:
            answer_text = result

        return QueryResponse(answer=answer_text)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
