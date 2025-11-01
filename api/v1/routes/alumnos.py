from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Alumno as AlumnoModel
from db.repositories import colegio_repository
from db.repositories.alumno_repository import list_all, create
from schemas.alumno import AlumnoCreate, AlumnoRead


router = APIRouter(prefix="/alumnos", tags=["alumnos"])


@router.get("/", response_model=list[AlumnoRead])
def get_alumnos(session: Session = Depends(get_session)):
    return list_all(session)


@router.post("/", response_model=AlumnoRead, status_code=status.HTTP_201_CREATED)
def create_alumno(payload: AlumnoCreate, session: Session = Depends(get_session)):
    # FK validation
    if colegio_repository.get(session, payload.idColegio) is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

    alumno = AlumnoModel(**payload.model_dump())
    return create(session, alumno)
