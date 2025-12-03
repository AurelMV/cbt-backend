from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from sqlmodel import Session

from db.base import get_session
from db.models.location import Distrito, Provincia
from db.repositories import distrito_repository as repo
from schemas.distrito import DistritoCreate, DistritoRead

router = APIRouter(prefix="/distritos", tags=["distritos"])


@router.get("/", response_model=list[DistritoRead])
async def list_distritos(
    provincia_id: Optional[int] = None, session: Session = Depends(get_session)
):
    return repo.list_all(session, provincia_id=provincia_id)


@router.post("/", response_model=DistritoRead, status_code=status.HTTP_201_CREATED)
async def create_distrito(
    data: DistritoCreate, session: Session = Depends(get_session)
):
    # Validate FK: provincia exists
    if session.get(Provincia, data.provincia_id) is None:
        raise HTTPException(status_code=400, detail="provincia_id no existe")

    dist = Distrito(**data.model_dump())
    return repo.create(session, dist)
