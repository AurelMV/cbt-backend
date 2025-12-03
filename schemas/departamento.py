from pydantic import BaseModel


class DepartamentoCreate(BaseModel):
    nombreDepartamento: str


class DepartamentoRead(BaseModel):
    id: int
    nombreDepartamento: str

    model_config = {"from_attributes": True}
