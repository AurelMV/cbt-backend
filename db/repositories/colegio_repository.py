from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.location import Colegio


def list_all(session: Session) -> List[Colegio]:
    return session.exec(select(Colegio)).all()


def get(session: Session, col_id: int) -> Optional[Colegio]:
    return session.get(Colegio, col_id)


def create(session: Session, col: Colegio) -> Colegio:
    session.add(col)
    session.commit()
    session.refresh(col)
    return col
