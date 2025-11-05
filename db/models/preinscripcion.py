from typing import Optional, List
from datetime import date

from sqlmodel import SQLModel, Field, Relationship


class PreInscripcion(SQLModel, table=True):
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
    estado: str = Field(default="pendiente")

    # Relaciones con tablas existentes
    idColegio: int = Field(foreign_key="colegio.id")
    idCiclo: int = Field(foreign_key="ciclo.id")
    idPrograma: int = Field(foreign_key="programaestudios.id")

    pagos: List["PrePago"] = Relationship(back_populates="preinscripcion")


class PrePago(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nroVoucher: str
    medioPago: str
    monto: float
    fecha: date
    idInscripcion: int = Field(foreign_key="preinscripcion.id")
    foto: str | None = None
    TipoPago: str
    estado: str = Field(default="pendiente")

    preinscripcion: Optional[PreInscripcion] = Relationship(back_populates="pagos")
