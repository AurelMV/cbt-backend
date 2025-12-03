from pydantic import BaseModel


class GrupoCreate(BaseModel):
    nombreGrupo: str
    aforo: int
    estado: bool = True
    ciclo_id: int


class GrupoRead(BaseModel):
    id: int
    nombreGrupo: str
    aforo: int
    estado: bool
    ciclo_id: int

    model_config = {"from_attributes": True}


class GrupoUpdate(BaseModel):
    nombreGrupo: str
    aforo: int
    estado: bool
    ciclo_id: int
