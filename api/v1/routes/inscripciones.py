from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Inscripcion as InscripcionModel
from db.repositories import (
    ciclo_repository,
    programa_repository,
    clase_repository,
)
from db.repositories.alumno_repository import get as get_alumno, get_by_dni as get_alumno_by_dni
from db.repositories.inscripcion_repository import list_all, create, get_by_alumno_and_ciclo
from schemas.inscripcion import InscripcionCreate, InscripcionRead, InscripcionLookupRead


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


@router.get("/buscar", response_model=InscripcionLookupRead)
def buscar_inscripcion(
    dni: str = Query(..., description="DNI del alumno"),
    idCiclo: int = Query(..., description="ID del ciclo"),
    session: Session = Depends(get_session),
):
    """Buscar una inscripción por DNI de alumno y ciclo.

    Devuelve nombres del alumno y el id de la inscripción si existe.
    """
    alumno = get_alumno_by_dni(session, dni)
    if alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    ins = get_by_alumno_and_ciclo(session, alumno.id, idCiclo)
    if ins is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada para el ciclo indicado")

    return InscripcionLookupRead(
        idInscripcion=ins.id,
        idAlumno=alumno.id,
        idCiclo=ins.idCiclo,
        nombreAlumno=alumno.nombreAlumno,
        aPaterno=alumno.aPaterno,
        aMaterno=alumno.aMaterno,
        Codigo=getattr(ins, "Codigo", None),
    )
