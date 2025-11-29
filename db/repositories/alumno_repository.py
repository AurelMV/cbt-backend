from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import or_, func
import math

from db.models.enrollment import Alumno
from db.models.location import Colegio


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
    sexo: Optional[str] = None,
    id_colegio: Optional[int] = None,
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
            Colegio.nombreColegio.ilike(like),
        )

    offset = max(0, offset)
    limit = max(1, limit)

    base_query = (
        select(
            Alumno.id.label("id"),
            Alumno.nombreAlumno.label("nombre"),
            Alumno.aPaterno.label("apellido_paterno"),
            Alumno.aMaterno.label("apellido_materno"),
            Alumno.sexo.label("sexo"),
            Alumno.fechaNacimiento.label("fecha_nacimiento"),
            Alumno.telefonoEstudiante.label("telefono_estudiante"),
            Alumno.telefonoApoderado.label("telefono_apoderado"),
            Alumno.email.label("email"),
            Alumno.nroDocumento.label("nro_documento"),
            Alumno.Direccion.label("direccion"),
            Alumno.anoCulminado.label("ano_culminado"),
            Alumno.idColegio.label("id_colegio"),
            Colegio.nombreColegio.label("colegio"),
        )
        .join(Colegio, Colegio.id == Alumno.idColegio)
    )
    count_query = select(Alumno.id).join(Colegio, Colegio.id == Alumno.idColegio)

    if like_condition is not None:
        base_query = base_query.where(like_condition)
        count_query = count_query.where(like_condition)

    if sexo:
        base_query = base_query.where(Alumno.sexo == sexo)
        count_query = count_query.where(Alumno.sexo == sexo)
    if id_colegio is not None:
        base_query = base_query.where(Colegio.id == id_colegio)
        count_query = count_query.where(Colegio.id == id_colegio)

    rows = session.exec(base_query.offset(offset).limit(limit)).all()
    total = session.exec(
        select(func.count()).select_from(count_query.subquery())
    ).one()
    pages = math.ceil(total / limit) if total else 0
    page = offset // limit if limit > 0 else 0
    items = [dict(row._mapping) for row in rows]
    return {
        "items": items,
        "total": total,
        "pages": pages,
        "limit": limit,
        "offset": offset,
        "page": page,
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
