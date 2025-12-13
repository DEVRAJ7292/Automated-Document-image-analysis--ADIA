from typing import List


def compute_confidence(similarities: List[float]) -> int:
    """
    Compute deterministic confidence score (0–100)
    based purely on FAISS similarity scores.
    """

    if not similarities:
        return 0

    top_score = max(similarities)
    avg_score = sum(similarities) / len(similarities)

    # Base confidence from top similarity
    confidence = top_score * 100

    # Penalize if only one strong chunk exists
    if len(similarities) == 1:
        confidence *= 0.85

    # Penalize weak overall evidence
    if avg_score < 0.5:
        confidence *= 0.7

    # Clamp
    confidence = max(0, min(confidence, 100))

    return int(round(confidence))
