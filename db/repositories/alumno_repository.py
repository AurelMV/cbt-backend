from typing import List, Optional
from sqlmodel import Session, select

from db.models.enrollment import Alumno


def list_all(session: Session) -> List[Alumno]:
    return session.exec(select(Alumno)).all()


def create(session: Session, alumno: Alumno) -> Alumno:
    session.add(alumno)
    session.commit()
    session.refresh(alumno)
    return alumno


def get(session: Session, alumno_id: int) -> Optional[Alumno]:
    return session.get(Alumno, alumno_id)
