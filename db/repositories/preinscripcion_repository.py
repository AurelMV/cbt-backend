from __future__ import annotations
from typing import List

from sqlmodel import Session, select

from db.models.preinscripcion import PreInscripcion


def list_all(session: Session) -> List[PreInscripcion]:
    return session.exec(select(PreInscripcion)).all()


def create(session: Session, entity: PreInscripcion) -> PreInscripcion:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity
