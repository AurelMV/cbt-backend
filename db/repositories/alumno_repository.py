from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import or_, func
import math

from db.models.enrollment import Alumno


def list_all(session: Session) -> List[Alumno]:
    return session.exec(select(Alumno)).all()


def list_filtered(
    session: Session,
    q: Optional[str] = None,
    offset: int = 0,
    limit: int = 15,
) -> List[Alumno]:
    stmt = select(Alumno)

    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                Alumno.nombreAlumno.ilike(like),
                Alumno.aPaterno.ilike(like),
                Alumno.aMaterno.ilike(like),
                Alumno.nroDocumento.ilike(like),
                Alumno.email.ilike(like),
            )
        )

    stmt = stmt.offset(max(0, offset)).limit(max(1, limit))
    return session.exec(stmt).all()


def list_filtered_paginated(
    session: Session,
    q: Optional[str] = None,
    offset: int = 0,
    limit: int = 15,
):
    """Return paginated alumnos plus total and pages.

    Applies the same filtering as list_filtered. Pages are computed as
    ceil(total/limit)."""
    like_condition = None
    if q:
        like = f"%{q}%"
        like_condition = or_(
            Alumno.nombreAlumno.ilike(like),
            Alumno.aPaterno.ilike(like),
            Alumno.aMaterno.ilike(like),
            Alumno.nroDocumento.ilike(like),
            Alumno.email.ilike(like),
        )

    base_query = select(Alumno)
    count_query = select(func.count(Alumno.id))
    if like_condition is not None:
        base_query = base_query.where(like_condition)
        count_query = count_query.where(like_condition)

    items = session.exec(base_query.offset(max(0, offset)).limit(max(1, limit))).all()
    total = session.exec(count_query).one()
    pages = math.ceil(total / limit) if total else 0
    return {
        "items": items,
        "total": total,
        "pages": pages,
        "limit": limit,
        "offset": offset,
    }


def create(session: Session, alumno: Alumno) -> Alumno:
    session.add(alumno)
    session.commit()
    session.refresh(alumno)
    return alumno


def get(session: Session, alumno_id: int) -> Optional[Alumno]:
    return session.get(Alumno, alumno_id)


def get_by_dni(session: Session, dni: str) -> Optional[Alumno]:
    """Return the first Alumno matching the given DNI (nroDocumento)."""
    return session.exec(select(Alumno).where(Alumno.nroDocumento == dni)).first()
