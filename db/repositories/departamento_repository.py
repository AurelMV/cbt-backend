from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.location import Departamento


def list_all(session: Session) -> List[Departamento]:
    return session.exec(select(Departamento)).all()


def get(session: Session, dep_id: int) -> Optional[Departamento]:
    return session.get(Departamento, dep_id)


def create(session: Session, dep: Departamento) -> Departamento:
    session.add(dep)
    session.commit()
    session.refresh(dep)
    return dep
