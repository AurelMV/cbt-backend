from pydantic import BaseModel


class ClaseCreate(BaseModel):
    codigoClase: str
    grupo_id: int


class ClaseRead(BaseModel):
    id: int
    codigoClase: str
    grupo_id: int

    model_config = {"from_attributes": True}


class ClaseUpdate(BaseModel):
    codigoClase: str
    grupo_id: int
