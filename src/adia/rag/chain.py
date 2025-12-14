from pathlib import Path
from typing import List, Dict

from adia.embeddings.retriever import SemanticRetriever
from adia.rag.llm import LLMClient
from adia.rag.prompt_templates import build_rag_prompt


def compute_confidence(scores: List[float]) -> int:
    if not scores:
        return 0

    top = max(scores)
    confidence = top * 100
    return int(round(max(0, min(confidence, 100))))


class RAGChain:
    def __init__(self, embeddings_path: Path):
        self.retriever = SemanticRetriever(index_path=embeddings_path)
        self.llm = LLMClient()

    def answer(self, question: str, top_k: int = 5) -> Dict:
        results = self.retriever.query(question, top_k=top_k)

        if not results:
            return {
                "answer": "No answer found.",
                "confidence": 0,
                "sources": [],
            }

        context_chunks = [r["text"] for r in results]
        context = "\n\n".join(context_chunks)

        prompt = build_rag_prompt(context=context, question=question)
        answer = self.llm.generate(prompt)

        scores = [r["score"] for r in results]

        sources = [
            {
                "document": r["metadata"].get("source"),
                "similarity": round(r["score"], 3),
                "text_preview": r["text"][:200],
            }
            for r in results
        ]

        return {
            "answer": answer,
            "confidence": compute_confidence(scores),
            "sources": sources,
        }
