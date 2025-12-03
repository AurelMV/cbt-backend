from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Inscripcion as InscripcionModel
from db.repositories import (
    ciclo_repository,
    programa_repository,
    clase_repository,
)
from db.repositories.alumno_repository import (
    get as get_alumno,
    get_by_dni as get_alumno_by_dni,
)
from db.repositories.inscripcion_repository import (
    list_paginated_with_details,
    create,
    get_by_alumno_and_ciclo,
)
from schemas.pagination import Page
from schemas.inscripcion import (
    InscripcionCreate,
    InscripcionRead,
    InscripcionLookupRead,
    InscripcionDetalleRead,
)


router = APIRouter(prefix="/inscripciones", tags=["inscripciones"])


@router.get("/", response_model=Page[InscripcionDetalleRead])
def get_inscripciones(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(15, ge=1, le=100),
    page: int | None = Query(None, ge=0, description="Número de página (0-based)"),
    q: str | None = Query(
        None, description="Busca por código, estado pago o tipo pago"
    ),
    id_ciclo: int | None = Query(None, alias="idCiclo", ge=1),
    id_programa: int | None = Query(None, alias="idPrograma", ge=1),
    id_clase: int | None = Query(None, alias="idClase", ge=1),
):
    effective_offset = offset if page is None else page * limit
    result = list_paginated_with_details(
        session,
        q=q,
        offset=effective_offset,
        limit=limit,
        id_ciclo=id_ciclo,
        id_programa=id_programa,
        id_clase=id_clase,
    )
    result["items"] = [InscripcionDetalleRead(**item) for item in result["items"]]
    return result


@router.post("/", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED)
def create_inscripcion(
    payload: InscripcionCreate, session: Session = Depends(get_session)
):
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
    id_ciclo: int = Query(..., description="ID del ciclo", alias="idCiclo"),
    session: Session = Depends(get_session),
):
    """Buscar una inscripción por DNI de alumno y ciclo.

    Devuelve nombres del alumno y el id de la inscripción si existe.
    """
    alumno = get_alumno_by_dni(session, dni)
    if alumno is None:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    ins = get_by_alumno_and_ciclo(session, alumno.id, id_ciclo)
    if ins is None:
        raise HTTPException(
            status_code=404, detail="Inscripción no encontrada para el ciclo indicado"
        )

    return InscripcionLookupRead(
        idInscripcion=ins.id,
        idAlumno=alumno.id,
        idCiclo=ins.idCiclo,
        nombreAlumno=alumno.nombreAlumno,
        aPaterno=alumno.aPaterno,
        aMaterno=alumno.aMaterno,
        Codigo=getattr(ins, "Codigo", None),
    )
