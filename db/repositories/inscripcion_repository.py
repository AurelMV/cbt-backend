from typing import List, Optional
from sqlmodel import Session, select

from db.models.enrollment import Inscripcion


def list_all(session: Session) -> List[Inscripcion]:
    return session.exec(select(Inscripcion)).all()


def create(session: Session, inscripcion: Inscripcion) -> Inscripcion:
    session.add(inscripcion)
    session.commit()
    session.refresh(inscripcion)
    return inscripcion


def get(session: Session, inscripcion_id: int) -> Optional[Inscripcion]:
    return session.get(Inscripcion, inscripcion_id)
