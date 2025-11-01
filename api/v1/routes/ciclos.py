from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from db.base import get_session
from db.models.academic import Ciclo
from fastapi import HTTPException
from db.repositories import ciclo_repository as repo
from schemas.ciclo import CicloCreate, CicloRead, CicloUpdate

router = APIRouter(prefix="/ciclos", tags=["ciclos"])


@router.get("/", response_model=list[CicloRead])
async def list_ciclos(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=CicloRead, status_code=status.HTTP_201_CREATED)
async def create_ciclo(data: CicloCreate, session: Session = Depends(get_session)):
    ciclo = Ciclo(**data.model_dump())
    return repo.create(session, ciclo)


@router.put("/{ciclo_id}", response_model=CicloRead)
async def update_ciclo(
    ciclo_id: int, data: CicloUpdate, session: Session = Depends(get_session)
):
    ciclo = repo.get(session, ciclo_id)
    if not ciclo:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")

    ciclo.nombreCiclo = data.nombreCiclo
    ciclo.fechaInicio = data.fechaInicio
    ciclo.fechaFin = data.fechaFin
    ciclo.estado = data.estado
    return repo.update(session, ciclo)
