from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.academic import Ciclo


def list_all(session: Session) -> List[Ciclo]:
    return session.exec(select(Ciclo)).all()


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
