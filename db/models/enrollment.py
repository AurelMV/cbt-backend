from typing import Optional, List, TYPE_CHECKING
from datetime import date

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from db.models.academic import Clase


class Alumno(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombreAlumno: str
    aMaterno: str
    aPaterno: str
    sexo: str
    telefonoEstudiante: str
    telefonoApoderado: str
    fechaNacimiento: date
    email: str
    anoCulminado: int
    Direccion: str
    nroDocumento: str

    idColegio: int = Field(foreign_key="colegio.id")

    inscripciones: List["Inscripcion"] = Relationship(back_populates="alumno")


class Inscripcion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    turno: str
    fecha: date
    Estado: bool = Field(default=True)

    idAlumno: int = Field(foreign_key="alumno.id")
    idPrograma: int = Field(foreign_key="programaestudios.id")
    idCiclo: int = Field(foreign_key="ciclo.id")
    idClase: int = Field(foreign_key="clase.id")

    Codigo: str
    EstadoPago: str
    TipoPago: str

    alumno: Optional["Alumno"] = Relationship(back_populates="inscripciones")
    clase: Optional["Clase"] = Relationship(back_populates="inscripciones")
    pagos: List["Pago"] = Relationship(back_populates="inscripcion")


class Pago(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nroVoucher: str
    medioPago: str
    monto: float
    fecha: date
    idInscripcion: int = Field(foreign_key="inscripcion.id")
    foto: str | None = None
    Estado: bool = Field(default=False)

    inscripcion: Optional["Inscripcion"] = Relationship(back_populates="pagos")
