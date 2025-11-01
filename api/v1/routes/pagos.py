from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Pago as PagoModel
from db.repositories.inscripcion_repository import get as get_inscripcion
from db.repositories.pago_repository import list_all, create
from schemas.pago import PagoCreate, PagoRead


router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/", response_model=list[PagoRead])
def get_pagos(session: Session = Depends(get_session)):
    return list_all(session)


@router.post("/", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def create_pago(payload: PagoCreate, session: Session = Depends(get_session)):
    # FK validation
    if get_inscripcion(session, payload.idInscripcion) is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    pago = PagoModel(**payload.model_dump())
    return create(session, pago)
