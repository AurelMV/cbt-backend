from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from db.base import get_session
from db.models.programa import ProgramaEstudios
from db.repositories import programa_repository as repo
from fastapi import HTTPException
from schemas.programa import ProgramaCreate, ProgramaRead, ProgramaUpdate

router = APIRouter(prefix="/programas", tags=["programas"])


@router.get("/", response_model=list[ProgramaRead])
async def list_programas(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=ProgramaRead, status_code=status.HTTP_201_CREATED)
async def create_programa(
    data: ProgramaCreate, session: Session = Depends(get_session)
):
    programa = ProgramaEstudios(**data.model_dump())
    return repo.create(session, programa)


@router.put("/{programa_id}", response_model=ProgramaRead)
async def update_programa(
    programa_id: int,
    data: ProgramaUpdate,
    session: Session = Depends(get_session),
):
    programa = repo.get(session, programa_id)
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    programa.nombrePrograma = data.nombrePrograma
    return repo.update(session, programa)
