from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from db.base import get_session
from db.models.academic import Grupo
from fastapi import HTTPException
from db.models.academic import Ciclo
from db.repositories import grupo_repository as repo
from schemas.grupo import GrupoCreate, GrupoRead, GrupoUpdate

router = APIRouter(prefix="/grupos", tags=["grupos"])


@router.get("/", response_model=list[GrupoRead])
async def list_grupos(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=GrupoRead, status_code=status.HTTP_201_CREATED)
async def create_grupo(data: GrupoCreate, session: Session = Depends(get_session)):
    grupo = Grupo(**data.model_dump())
    return repo.create(session, grupo)


@router.put("/{grupo_id}", response_model=GrupoRead)
async def update_grupo(
    grupo_id: int, data: GrupoUpdate, session: Session = Depends(get_session)
):
    grupo = repo.get(session, grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    # validar FK
    if session.get(Ciclo, data.ciclo_id) is None:
        raise HTTPException(status_code=400, detail="ciclo_id no existe")

    grupo.nombreGrupo = data.nombreGrupo
    grupo.aforo = data.aforo
    grupo.estado = data.estado
    grupo.ciclo_id = data.ciclo_id
    return repo.update(session, grupo)
