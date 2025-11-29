from typing import List, Optional
import math

from sqlmodel import Session, select
from sqlalchemy import func, or_

from core.pagination import paginate

from db.models.enrollment import Pago, Inscripcion, Alumno
from db.models.academic import Ciclo


def list_all(session: Session) -> List[Pago]:
    return session.exec(select(Pago)).all()


def list_paginated(session: Session, q: Optional[str], offset: int, limit: int):
    return paginate(
        session,
        Pago,
        q=q,
        columns=["nroVoucher", "medioPago"],
        offset=offset,
        limit=limit,
    )


def list_paginated_with_details(
    session: Session,
    q: Optional[str],
    offset: int,
    limit: int,
    id_ciclo: Optional[int] = None,
    estado: Optional[bool] = None,
    tipo_pago: Optional[str] = None,
):
    offset = max(0, offset)
    limit = max(1, limit)

    stmt = (
        select(
            Pago.id.label("id"),
            Pago.nroVoucher.label("nroVoucher"),
            Pago.medioPago.label("medioPago"),
            Pago.monto.label("monto"),
            Pago.fecha.label("fecha"),
            Pago.idInscripcion.label("idInscripcion"),
            Pago.foto.label("foto"),
            Pago.Estado.label("Estado"),
            Inscripcion.TipoPago.label("tipoPago"),
            Alumno.nombreAlumno.label("nombreAlumno"),
            Alumno.aPaterno.label("aPaterno"),
            Alumno.aMaterno.label("aMaterno"),
            Ciclo.nombreCiclo.label("nombreCiclo"),
        )
        .join(Inscripcion, Inscripcion.id == Pago.idInscripcion)
        .join(Alumno, Alumno.id == Inscripcion.idAlumno)
        .join(Ciclo, Ciclo.id == Inscripcion.idCiclo)
    )

    if q:
        like = f"%{q}%"
        filtro = or_(
            Pago.nroVoucher.ilike(like),
            Alumno.nombreAlumno.ilike(like),
            Alumno.aPaterno.ilike(like),
            Alumno.aMaterno.ilike(like),
            Pago.medioPago.ilike(like),
            Inscripcion.TipoPago.ilike(like),
            Ciclo.nombreCiclo.ilike(like),
        )
        stmt = stmt.where(filtro)
    else:
        filtro = None

    if id_ciclo is not None:
        stmt = stmt.where(Inscripcion.idCiclo == id_ciclo)
    if estado is not None:
        stmt = stmt.where(Pago.Estado == estado)
    if tipo_pago:
        stmt = stmt.where(Inscripcion.TipoPago == tipo_pago)

    count_base = (
        select(Pago.id)
        .join(Inscripcion, Inscripcion.id == Pago.idInscripcion)
        .join(Alumno, Alumno.id == Inscripcion.idAlumno)
        .join(Ciclo, Ciclo.id == Inscripcion.idCiclo)
    )
    if filtro is not None:
        count_base = count_base.where(filtro)
    if id_ciclo is not None:
        count_base = count_base.where(Inscripcion.idCiclo == id_ciclo)
    if estado is not None:
        count_base = count_base.where(Pago.Estado == estado)
    if tipo_pago:
        count_base = count_base.where(Inscripcion.TipoPago == tipo_pago)

    total = session.exec(
        select(func.count()).select_from(count_base.subquery())
    ).one()

    rows = session.exec(
        stmt.order_by(Pago.fecha.desc(), Pago.id.desc()).offset(offset).limit(limit)
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


def create(session: Session, pago: Pago) -> Pago:
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return pago


def get(session: Session, pago_id: int) -> Optional[Pago]:
    return session.get(Pago, pago_id)
