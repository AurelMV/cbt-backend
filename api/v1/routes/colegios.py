from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from sqlmodel import Session

from db.base import get_session
from db.models.location import Colegio, Distrito
from db.repositories import colegio_repository as repo
from schemas.colegio import ColegioCreate, ColegioRead

router = APIRouter(prefix="/colegios", tags=["colegios"])


@router.get("/", response_model=list[ColegioRead])
async def list_colegios(
    distrito_id: Optional[int] = None, session: Session = Depends(get_session)
):
    return repo.list_all(session, distrito_id=distrito_id)


@router.post("/", response_model=ColegioRead, status_code=status.HTTP_201_CREATED)
async def create_colegio(data: ColegioCreate, session: Session = Depends(get_session)):
    # Validate FK: distrito exists
    if session.get(Distrito, data.distrito_id) is None:
        raise HTTPException(status_code=400, detail="distrito_id no existe")

    col = Colegio(**data.model_dump())
    return repo.create(session, col)
