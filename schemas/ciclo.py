from datetime import date
from pydantic import BaseModel


class CicloCreate(BaseModel):
    nombreCiclo: str
    fechaInicio: date
    fechaFin: date
    estado: bool = True


class CicloRead(BaseModel):
    id: int
    nombreCiclo: str
    fechaInicio: date
    fechaFin: date
    estado: bool

    model_config = {"from_attributes": True}


class CicloUpdate(BaseModel):
    nombreCiclo: str
    fechaInicio: date
    fechaFin: date
    estado: bool
