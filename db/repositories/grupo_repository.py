from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.academic import Grupo


def list_all(session: Session) -> List[Grupo]:
    return session.exec(select(Grupo)).all()


def create(session: Session, grupo: Grupo) -> Grupo:
    session.add(grupo)
    session.commit()
    session.refresh(grupo)
    return grupo


def get(session: Session, grupo_id: int) -> Optional[Grupo]:
    return session.get(Grupo, grupo_id)


def update(session: Session, grupo: Grupo) -> Grupo:
    session.add(grupo)
    session.commit()
    session.refresh(grupo)
    return grupo
