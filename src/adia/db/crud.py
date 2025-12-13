from sqlalchemy.orm import Session

from adia.db import models


def create_document(db: Session, filename: str, source_path: str):
    doc = models.Document(
        filename=filename,
        source_path=source_path,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def log_query(db: Session, question: str, answer: str):
    q = models.QueryLog(
        question=question,
        answer=answer,
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q
