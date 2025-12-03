from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.location import Provincia


def list_all(
    session: Session, departamento_id: Optional[int] = None
) -> List[Provincia]:
    stmt = select(Provincia)
    if departamento_id is not None:
        stmt = stmt.where(Provincia.departamento_id == departamento_id)
    return session.exec(stmt).all()


def get(session: Session, prov_id: int) -> Optional[Provincia]:
    return session.get(Provincia, prov_id)


def create(session: Session, prov: Provincia) -> Provincia:
    session.add(prov)
    session.commit()
    session.refresh(prov)
    return prov
