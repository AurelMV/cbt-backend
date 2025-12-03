from datetime import date
from pydantic import BaseModel


class InscripcionBase(BaseModel):
    turno: str
    fecha: date
    Estado: bool = True
    idAlumno: int
    idPrograma: int
    idCiclo: int
    idClase: int
    Codigo: str
    EstadoPago: str
    TipoPago: str


class InscripcionCreate(InscripcionBase):
    pass


class InscripcionRead(InscripcionBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class InscripcionLookupRead(BaseModel):
    """DTO para devolver datos mínimos al buscar por DNI + ciclo."""
    idInscripcion: int
    idAlumno: int
    idCiclo: int
    nombreAlumno: str
    aPaterno: str
    aMaterno: str
    Codigo: str | None = None


class InscripcionDetalleRead(InscripcionRead):
    nombreAlumno: str
    aPaterno: str | None = None
    aMaterno: str | None = None
    nombreCiclo: str
    nombreGrupo: str
    codigoClase: str
    pagosCount: int

    model_config = {"from_attributes": True}
