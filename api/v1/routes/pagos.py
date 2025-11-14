from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Pago as PagoModel
from db.repositories.inscripcion_repository import get as get_inscripcion
from db.repositories.pago_repository import list_paginated, create
from schemas.pagination import Page
from schemas.pago import PagoCreate, PagoRead


router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/", response_model=Page[PagoRead])
def get_pagos(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(15, ge=1, le=100),
    page: int | None = Query(None, ge=0, description="Número de página (0-based)"),
    q: str | None = Query(
        None, description="Busca por número de voucher o medio de pago"
    ),
):
    effective_offset = offset if page is None else page * limit
    return list_paginated(session, q=q, offset=effective_offset, limit=limit)


@router.post("/", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def create_pago(payload: PagoCreate, session: Session = Depends(get_session)):
    # FK validation
    if get_inscripcion(session, payload.idInscripcion) is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    pago = PagoModel(**payload.model_dump())
    return create(session, pago)
