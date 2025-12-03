from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.preinscripcion import PreInscripcion


def list_all(session: Session) -> List[PreInscripcion]:
    return session.exec(select(PreInscripcion)).all()


def create(session: Session, entity: PreInscripcion) -> PreInscripcion:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity


def list_by_estado(session: Session, estado: str) -> List[PreInscripcion]:
    return session.exec(select(PreInscripcion).where(PreInscripcion.estado == estado)).all()


def get(session: Session, pre_id: int) -> Optional[PreInscripcion]:
    return session.get(PreInscripcion, pre_id)


def update(session: Session, entity: PreInscripcion) -> PreInscripcion:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity
