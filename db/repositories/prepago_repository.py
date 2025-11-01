from __future__ import annotations
from typing import List

from sqlmodel import Session, select

from db.models.preinscripcion import PrePago


def list_all(session: Session) -> List[PrePago]:
    return session.exec(select(PrePago)).all()


def create(session: Session, entity: PrePago) -> PrePago:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity
