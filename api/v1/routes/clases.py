from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from db.base import get_session
from db.models.academic import Clase
from fastapi import HTTPException
from db.models.academic import Grupo
from db.repositories import clase_repository as repo
from schemas.clase import ClaseCreate, ClaseRead, ClaseUpdate

router = APIRouter(prefix="/clases", tags=["clases"])


@router.get("/", response_model=list[ClaseRead])
async def list_clases(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=ClaseRead, status_code=status.HTTP_201_CREATED)
async def create_clase(data: ClaseCreate, session: Session = Depends(get_session)):
    clase = Clase(**data.model_dump())
    return repo.create(session, clase)


@router.put("/{clase_id}", response_model=ClaseRead)
async def update_clase(
    clase_id: int, data: ClaseUpdate, session: Session = Depends(get_session)
):
    clase = repo.get(session, clase_id)
    if not clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    # validar FK
    if session.get(Grupo, data.grupo_id) is None:
        raise HTTPException(status_code=400, detail="grupo_id no existe")

    clase.codigoClase = data.codigoClase
    clase.grupo_id = data.grupo_id
    return repo.update(session, clase)
