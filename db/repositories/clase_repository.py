from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select
from core.pagination import paginate

from db.models.academic import Clase


def list_all(session: Session) -> List[Clase]:
    return session.exec(select(Clase)).all()


def list_paginated(session: Session, q: Optional[str], offset: int, limit: int):
    return paginate(
        session, Clase, q=q, columns=["codigoClase"], offset=offset, limit=limit
    )


def create(session: Session, clase: Clase) -> Clase:
    session.add(clase)
    session.commit()
    session.refresh(clase)
    return clase


def get(session: Session, clase_id: int) -> Optional[Clase]:
    return session.get(Clase, clase_id)


def update(session: Session, clase: Clase) -> Clase:
    session.add(clase)
    session.commit()
    session.refresh(clase)
    return clase
