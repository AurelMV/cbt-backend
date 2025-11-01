from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from db.base import get_session
from db.models.location import Departamento
from db.repositories import departamento_repository as repo
from schemas.departamento import DepartamentoCreate, DepartamentoRead

router = APIRouter(prefix="/departamentos", tags=["departamentos"])


@router.get("/", response_model=list[DepartamentoRead])
async def list_departamentos(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=DepartamentoRead, status_code=status.HTTP_201_CREATED)
async def create_departamento(
    data: DepartamentoCreate, session: Session = Depends(get_session)
):
    dep = Departamento(**data.model_dump())
    return repo.create(session, dep)
