def build_rag_prompt(context: str, question: str) -> str:
    return f"""
You are a precise document analysis assistant.

Use ONLY the information in the context below.
If the answer is not present, say "I do not know".

Context:
{context}

Question:
{question}

Answer:
"""
