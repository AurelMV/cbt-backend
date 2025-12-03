from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from sqlmodel import Session

from db.base import get_session
from db.models.location import Provincia, Departamento
from db.repositories import provincia_repository as repo
from schemas.provincia import ProvinciaCreate, ProvinciaRead

router = APIRouter(prefix="/provincias", tags=["provincias"])


@router.get("/", response_model=list[ProvinciaRead])
async def list_provincias(
    departamento_id: Optional[int] = None, session: Session = Depends(get_session)
):
    return repo.list_all(session, departamento_id=departamento_id)


@router.post("/", response_model=ProvinciaRead, status_code=status.HTTP_201_CREATED)
async def create_provincia(
    data: ProvinciaCreate, session: Session = Depends(get_session)
):
    # Validate FK: departamento exists
    if session.get(Departamento, data.departamento_id) is None:
        raise HTTPException(status_code=400, detail="departamento_id no existe")

    prov = Provincia(**data.model_dump())
    return repo.create(session, prov)
