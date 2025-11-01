from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.location import Provincia


def list_all(session: Session) -> List[Provincia]:
    return session.exec(select(Provincia)).all()


def get(session: Session, prov_id: int) -> Optional[Provincia]:
    return session.get(Provincia, prov_id)


def create(session: Session, prov: Provincia) -> Provincia:
    session.add(prov)
    session.commit()
    session.refresh(prov)
    return prov
