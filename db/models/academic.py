from typing import Optional, List, TYPE_CHECKING
from datetime import date

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from db.models.enrollment import Inscripcion


class Ciclo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombreCiclo: str = Field(index=True)
    fechaInicio: date
    fechaFin: date
    estado: bool = Field(default=True)

    grupos: List["Grupo"] = Relationship(back_populates="ciclo")


class Grupo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombreGrupo: str = Field(index=True)
    aforo: int = Field(default=0)
    estado: bool = Field(default=True)

    ciclo_id: int = Field(foreign_key="ciclo.id")
    ciclo: Optional[Ciclo] = Relationship(back_populates="grupos")

    clases: List["Clase"] = Relationship(back_populates="grupo")


class Clase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigoClase: str = Field(index=True)

    grupo_id: int = Field(foreign_key="grupo.id")
    grupo: Optional[Grupo] = Relationship(back_populates="clases")
    inscripciones: List["Inscripcion"] = Relationship(back_populates="clase")
