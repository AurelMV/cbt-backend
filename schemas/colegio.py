from pydantic import BaseModel


class ColegioCreate(BaseModel):
    nombreColegio: str
    distrito_id: int


class ColegioRead(BaseModel):
    id: int
    nombreColegio: str
    distrito_id: int

    model_config = {"from_attributes": True}
