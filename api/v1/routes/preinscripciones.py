from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from db.base import get_session
from db.models.preinscripcion import PreInscripcion
from db.models.location import Colegio
from db.models.academic import Ciclo
from db.models.programa import ProgramaEstudios
from db.repositories import preinscripcion_repository as repo
from schemas.preinscripcion import PreInscripcionCreate, PreInscripcionRead

router = APIRouter(prefix="/preinscripciones", tags=["preinscripciones"])


@router.get("/", response_model=list[PreInscripcionRead])
async def list_preinscripciones(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=PreInscripcionRead, status_code=status.HTTP_201_CREATED)
async def create_preinscripcion(
    data: PreInscripcionCreate, session: Session = Depends(get_session)
):
    # Validaciones de FK
    if session.get(Colegio, data.idColegio) is None:
        raise HTTPException(status_code=400, detail="idColegio no existe")
    if session.get(Ciclo, data.idCiclo) is None:
        raise HTTPException(status_code=400, detail="idCiclo no existe")
    if session.get(ProgramaEstudios, data.idPrograma) is None:
        raise HTTPException(status_code=400, detail="idPrograma no existe")

    entity = PreInscripcion(**data.model_dump())
    return repo.create(session, entity)
