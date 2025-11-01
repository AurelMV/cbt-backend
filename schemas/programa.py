from pydantic import BaseModel


class ProgramaCreate(BaseModel):
    nombrePrograma: str


class ProgramaRead(BaseModel):
    id: int
    nombrePrograma: str

    model_config = {"from_attributes": True}


class ProgramaUpdate(BaseModel):
    # Para PUT usamos el mismo shape que create; si quisieras PATCH, lo haríamos opcional
    nombrePrograma: str
