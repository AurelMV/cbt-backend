from typing import List, Optional
import math

from sqlmodel import Session, select
from sqlalchemy import func, or_

from core.pagination import paginate

from db.models.enrollment import Inscripcion, Pago, Alumno
from db.models.academic import Ciclo, Clase, Grupo


def list_all(session: Session) -> List[Inscripcion]:
    return session.exec(select(Inscripcion)).all()


def list_paginated(session: Session, q: Optional[str], offset: int, limit: int):
    # Search over Codigo, EstadoPago, TipoPago
    return paginate(
        session,
        Inscripcion,
        q=q,
        columns=["Codigo", "EstadoPago", "TipoPago"],
        offset=offset,
        limit=limit,
    )


def list_paginated_with_details(
    session: Session,
    q: Optional[str],
    offset: int,
    limit: int,
    id_ciclo: Optional[int] = None,
    id_programa: Optional[int] = None,
    id_clase: Optional[int] = None,
):
    offset = max(0, offset)
    limit = max(1, limit)

    pagos_count = (
        select(func.count(Pago.id))
        .where(Pago.idInscripcion == Inscripcion.id)
        .correlate(Inscripcion)
        .scalar_subquery()
    )

    stmt = (
        select(
            Inscripcion.id.label("id"),
            Inscripcion.turno.label("turno"),
            Inscripcion.fecha.label("fecha"),
            Inscripcion.Estado.label("Estado"),
            Inscripcion.idAlumno.label("idAlumno"),
            Inscripcion.idPrograma.label("idPrograma"),
            Inscripcion.idCiclo.label("idCiclo"),
            Inscripcion.idClase.label("idClase"),
            Inscripcion.Codigo.label("Codigo"),
            Inscripcion.EstadoPago.label("EstadoPago"),
            Inscripcion.TipoPago.label("TipoPago"),
            Alumno.nombreAlumno.label("nombreAlumno"),
            Alumno.aPaterno.label("aPaterno"),
            Alumno.aMaterno.label("aMaterno"),
            Ciclo.nombreCiclo.label("nombreCiclo"),
            Grupo.nombreGrupo.label("nombreGrupo"),
            Clase.codigoClase.label("codigoClase"),
            pagos_count.label("pagosCount"),
        )
        .join(Alumno, Alumno.id == Inscripcion.idAlumno)
        .join(Ciclo, Ciclo.id == Inscripcion.idCiclo)
        .join(Clase, Clase.id == Inscripcion.idClase)
        .join(Grupo, Grupo.id == Clase.grupo_id)
    )

    if q:
        like = f"%{q}%"
        filtro = or_(
            Inscripcion.Codigo.ilike(like),
            Inscripcion.EstadoPago.ilike(like),
            Inscripcion.TipoPago.ilike(like),
            Alumno.nombreAlumno.ilike(like),
            Alumno.aPaterno.ilike(like),
            Alumno.aMaterno.ilike(like),
            Ciclo.nombreCiclo.ilike(like),
            Grupo.nombreGrupo.ilike(like),
            Clase.codigoClase.ilike(like),
        )
        stmt = stmt.where(filtro)
    else:
        filtro = None

    if id_ciclo is not None:
        stmt = stmt.where(Inscripcion.idCiclo == id_ciclo)
    if id_programa is not None:
        stmt = stmt.where(Inscripcion.idPrograma == id_programa)
    if id_clase is not None:
        stmt = stmt.where(Inscripcion.idClase == id_clase)

    count_base = (
        select(Inscripcion.id)
        .join(Alumno, Alumno.id == Inscripcion.idAlumno)
        .join(Ciclo, Ciclo.id == Inscripcion.idCiclo)
        .join(Clase, Clase.id == Inscripcion.idClase)
        .join(Grupo, Grupo.id == Clase.grupo_id)
    )
    if filtro is not None:
        count_base = count_base.where(filtro)
    if id_ciclo is not None:
        count_base = count_base.where(Inscripcion.idCiclo == id_ciclo)
    if id_programa is not None:
        count_base = count_base.where(Inscripcion.idPrograma == id_programa)
    if id_clase is not None:
        count_base = count_base.where(Inscripcion.idClase == id_clase)

    total = session.exec(
        select(func.count()).select_from(count_base.subquery())
    ).one()

    rows = session.exec(
        stmt.order_by(Inscripcion.id).offset(offset).limit(limit)
    ).all()

    pages = math.ceil(total / limit) if total else 0
    page = offset // limit if limit else 0

    items = [dict(row._mapping) for row in rows]

    return {
        "items": items,
        "total": total,
        "pages": pages,
        "limit": limit,
        "offset": offset,
        "page": page,
    }


def create(session: Session, inscripcion: Inscripcion) -> Inscripcion:
    session.add(inscripcion)
    session.commit()
    session.refresh(inscripcion)
    return inscripcion


def get(session: Session, inscripcion_id: int) -> Optional[Inscripcion]:
    return session.get(Inscripcion, inscripcion_id)


def get_by_alumno_and_ciclo(
    session: Session, alumno_id: int, ciclo_id: int
) -> Optional[Inscripcion]:
    """Return the first Inscripcion for a given alumno and ciclo."""
    stmt = select(Inscripcion).where(
        (Inscripcion.idAlumno == alumno_id) & (Inscripcion.idCiclo == ciclo_id)
    )
    return session.exec(stmt).first()
