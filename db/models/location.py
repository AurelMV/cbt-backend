from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class Departamento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombreDepartamento: str = Field(index=True)

    provincias: List["Provincia"] = Relationship(back_populates="departamento")


class Provincia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombreProvincia: str = Field(index=True)

    departamento_id: int = Field(foreign_key="departamento.id")
    departamento: Optional[Departamento] = Relationship(back_populates="provincias")

    distritos: List["Distrito"] = Relationship(back_populates="provincia")


class Distrito(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombreDistrito: str = Field(index=True)

    provincia_id: int = Field(foreign_key="provincia.id")
    provincia: Optional[Provincia] = Relationship(back_populates="distritos")

    colegios: List["Colegio"] = Relationship(back_populates="distrito")


class Colegio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombreColegio: str = Field(index=True)

    distrito_id: int = Field(foreign_key="distrito.id")
    distrito: Optional[Distrito] = Relationship(back_populates="colegios")
