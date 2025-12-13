from pathlib import Path
from typing import List, Dict

from adia.embeddings.retriever import SemanticRetriever
from adia.rag.llm import LLMClient
from adia.rag.prompt_templates import build_rag_prompt


def compute_confidence(scores: List[float]) -> int:
    """
    Deterministic confidence score (0–100) based on similarity scores.
    """
    if not scores:
        return 0

    top = max(scores)
    avg = sum(scores) / len(scores)

    confidence = top * 100

    if len(scores) == 1:
        confidence *= 0.85

    if avg < 0.5:
        confidence *= 0.7

    return int(round(max(0, min(confidence, 100))))


class RAGChain:
    def __init__(self, embeddings_path: Path):
        self.retriever = SemanticRetriever(index_path=embeddings_path)
        self.llm = LLMClient()

    def answer(self, question: str, top_k: int = 5) -> Dict:
        results = self.retriever.query(question, top_k=top_k)

        if not results:
            return {
                "answer": "No relevant documents found.",
                "confidence": 0,
                "sources": [],
            }

        context_chunks: List[str] = [r["text"] for r in results]
        context = "\n\n".join(context_chunks)

        prompt = build_rag_prompt(context=context, question=question)
        answer = self.llm.generate(prompt)

        scores = [r["score"] for r in results]

        sources = [
            {
                "document": r["metadata"].get("source"),
                "chunk": r["metadata"].get("chunk_id"),
                "similarity": round(r["score"], 3),
                "text_preview": r["text"][:200].strip(),
            }
            for r in results
        ]

        return {
            "answer": answer,
            "confidence": compute_confidence(scores),
            "sources": sources,
        }
