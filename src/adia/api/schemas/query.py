from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., description="User question")


class QueryResponse(BaseModel):
    answer: str = Field(..., description="Answer grounded in documents")
