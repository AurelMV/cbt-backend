from pydantic import BaseModel


class DistritoCreate(BaseModel):
    nombreDistrito: str
    provincia_id: int


class DistritoRead(BaseModel):
    id: int
    nombreDistrito: str
    provincia_id: int

    model_config = {"from_attributes": True}
