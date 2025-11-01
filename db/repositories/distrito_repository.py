from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.location import Distrito


def list_all(session: Session) -> List[Distrito]:
    return session.exec(select(Distrito)).all()


def get(session: Session, dist_id: int) -> Optional[Distrito]:
    return session.get(Distrito, dist_id)


def create(session: Session, dist: Distrito) -> Distrito:
    session.add(dist)
    session.commit()
    session.refresh(dist)
    return dist
