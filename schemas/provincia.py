from pydantic import BaseModel


class ProvinciaCreate(BaseModel):
    nombreProvincia: str
    departamento_id: int


class ProvinciaRead(BaseModel):
    id: int
    nombreProvincia: str
    departamento_id: int

    model_config = {"from_attributes": True}
