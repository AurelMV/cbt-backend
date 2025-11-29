from datetime import date
from pydantic import BaseModel, EmailStr


class AlumnoBase(BaseModel):
    nombreAlumno: str
    aMaterno: str
    aPaterno: str
    sexo: str
    telefonoEstudiante: str
    telefonoApoderado: str
    fechaNacimiento: date
    email: EmailStr
    anoCulminado: int
    Direccion: str
    nroDocumento: str
    idColegio: int


class AlumnoCreate(AlumnoBase):
    pass


class AlumnoRead(AlumnoBase):
    id: int

    model_config = {"from_attributes": True}


class AlumnoDetalleRead(AlumnoRead):
    edad: int
    colegioNombre: str | None = None
