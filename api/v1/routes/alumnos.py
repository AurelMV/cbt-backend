from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Alumno as AlumnoModel
from db.repositories import colegio_repository
from db.repositories.alumno_repository import list_filtered_paginated, create
from schemas.alumno import AlumnoCreate, AlumnoRead, AlumnoDetalleRead
from schemas.pagination import Page


router = APIRouter(prefix="/alumnos", tags=["alumnos"])


def _calculate_age(birth_date: date) -> int:
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return max(age, 0)


@router.get("/", response_model=Page[AlumnoDetalleRead])
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
    sexo: str | None = Query(
        None,
        min_length=1,
        max_length=1,
        description="Filtra por sexo (M/F)",
    ),
    id_colegio: int | None = Query(
        None,
        alias="idColegio",
        ge=1,
        description="Filtra por colegio",
    ),
):
    effective_offset = offset if page is None else page * limit
    sexo_filter = sexo.upper() if sexo else None
    result = list_filtered_paginated(
        session,
        q=q,
        offset=effective_offset,
        limit=limit,
        sexo=sexo_filter,
        id_colegio=id_colegio,
    )
    items = []
    for item in result["items"]:
        edad = _calculate_age(item["fecha_nacimiento"])
        items.append(
            AlumnoDetalleRead(
                id=item["id"],
                nombreAlumno=item["nombre"],
                aPaterno=item.get("apellido_paterno", ""),
                aMaterno=item.get("apellido_materno", ""),
                sexo=item["sexo"],
                edad=edad,
                telefonoEstudiante=item.get("telefono_estudiante", ""),
                telefonoApoderado=item.get("telefono_apoderado", ""),
                email=item["email"],
                nroDocumento=item["nro_documento"],
                Direccion=item.get("direccion", ""),
                anoCulminado=item["ano_culminado"],
                fechaNacimiento=item["fecha_nacimiento"],
                idColegio=item.get("id_colegio", 0),
                colegioNombre=item.get("colegio"),
            )
        )

    result["items"] = items
    return result


@router.post("/", response_model=AlumnoRead, status_code=status.HTTP_201_CREATED)
def create_alumno(payload: AlumnoCreate, session: Session = Depends(get_session)):
    # FK validation
    if colegio_repository.get(session, payload.idColegio) is None:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

    alumno = AlumnoModel(**payload.model_dump())
    return create(session, alumno)
