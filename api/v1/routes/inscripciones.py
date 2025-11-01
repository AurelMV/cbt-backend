from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Inscripcion as InscripcionModel
from db.repositories import (
    ciclo_repository,
    programa_repository,
    clase_repository,
)
from db.repositories.alumno_repository import get as get_alumno
from db.repositories.inscripcion_repository import list_all, create
from schemas.inscripcion import InscripcionCreate, InscripcionRead


router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])


@router.get("/", response_model=list[InscripcionRead])
def get_inscripciones(session: Session = Depends(get_session)):
    return list_all(session)


@router.post("/", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED)
def create_inscripcion(payload: InscripcionCreate, session: Session = Depends(get_session)):
    # FK validations
    if get_alumno(session, payload.idAlumno) is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    if programa_repository.get(session, payload.idPrograma) is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    if ciclo_repository.get(session, payload.idCiclo) is None:
        raise HTTPException(status_code=404, detail="Ciclo no encontrado")
    if clase_repository.get(session, payload.idClase) is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada")

    ins = InscripcionModel(**payload.model_dump())
    return create(session, ins)
