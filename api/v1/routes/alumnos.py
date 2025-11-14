from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Alumno as AlumnoModel
from db.repositories import colegio_repository
from db.repositories.alumno_repository import list_filtered_paginated, create
from schemas.alumno import AlumnoCreate, AlumnoRead
from schemas.pagination import Page


router = APIRouter(prefix="/alumnos", tags=["alumnos"])


@router.get("/", response_model=Page[AlumnoRead])
def get_alumnos(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0, description="Desplazamiento para paginación"),
    limit: int = Query(15, ge=1, le=100, description="Límite de resultados"),
    page: int | None = Query(
        None,
        ge=0,
        description="Número de página (0-based). Si se envía, ignora offset",
    ),
    q: str | None = Query(
        None, description="Búsqueda por nombre, apellidos, DNI o email"
    ),
):
    effective_offset = offset if page is None else page * limit
    return list_filtered_paginated(session, q=q, offset=effective_offset, limit=limit)


@router.post("/", response_model=AlumnoRead, status_code=status.HTTP_201_CREATED)
def create_alumno(payload: AlumnoCreate, session: Session = Depends(get_session)):
    # FK validation
    if colegio_repository.get(session, payload.idColegio) is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

    alumno = AlumnoModel(**payload.model_dump())
    return create(session, alumno)
