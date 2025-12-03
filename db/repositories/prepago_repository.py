from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.preinscripcion import PrePago


def list_all(session: Session) -> List[PrePago]:
    return session.exec(select(PrePago)).all()


def create(session: Session, entity: PrePago) -> PrePago:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity


def list_by_estado(session: Session, estado: str) -> List[PrePago]:
    return session.exec(select(PrePago).where(PrePago.estado == estado)).all()


def list_by_preinscripcion(session: Session, pre_id: int) -> List[PrePago]:
    return session.exec(select(PrePago).where(PrePago.idInscripcion == pre_id)).all()


def get(session: Session, pago_id: int) -> Optional[PrePago]:
    return session.get(PrePago, pago_id)


def update(session: Session, entity: PrePago) -> PrePago:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity
