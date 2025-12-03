from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from db.base import get_session
from db.models.preinscripcion import PrePago, PreInscripcion
from db.repositories import prepago_repository as repo
from schemas.preinscripcion import PrePagoCreate, PrePagoRead

router = APIRouter(prefix="/prepagos", tags=["prepagos"])


@router.get("/", response_model=list[PrePagoRead])
async def list_prepagos(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=PrePagoRead, status_code=status.HTTP_201_CREATED)
async def create_prepago(data: PrePagoCreate, session: Session = Depends(get_session)):
    if session.get(PreInscripcion, data.idInscripcion) is None:
        raise HTTPException(status_code=400, detail="idInscripcion no existe")

    entity = PrePago(**data.model_dump())
    return repo.create(session, entity)
