from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select
from core.pagination import paginate

from db.models.academic import Ciclo


def list_all(session: Session) -> List[Ciclo]:
    return session.exec(select(Ciclo)).all()


def list_paginated(session: Session, q: Optional[str], offset: int, limit: int):
    return paginate(
        session, Ciclo, q=q, columns=["nombreCiclo"], offset=offset, limit=limit
    )


def create(session: Session, ciclo: Ciclo) -> Ciclo:
    session.add(ciclo)
    session.commit()
    session.refresh(ciclo)
    return ciclo


def get(session: Session, ciclo_id: int) -> Optional[Ciclo]:
    return session.get(Ciclo, ciclo_id)


def update(session: Session, ciclo: Ciclo) -> Ciclo:
    session.add(ciclo)
    session.commit()
    session.refresh(ciclo)
    return ciclo
