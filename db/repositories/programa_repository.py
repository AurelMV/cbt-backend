from __future__ import annotations
from typing import List, Optional

from sqlmodel import Session, select

from db.models.programa import ProgramaEstudios


def list_all(session: Session) -> List[ProgramaEstudios]:
    return session.exec(select(ProgramaEstudios)).all()


def create(session: Session, programa: ProgramaEstudios) -> ProgramaEstudios:
    session.add(programa)
    session.commit()
    session.refresh(programa)
    return programa


def get(session: Session, programa_id: int) -> Optional[ProgramaEstudios]:
    return session.get(ProgramaEstudios, programa_id)


def update(session: Session, programa: ProgramaEstudios) -> ProgramaEstudios:
    session.add(programa)
    session.commit()
    session.refresh(programa)
    return programa
