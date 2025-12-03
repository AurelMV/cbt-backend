from datetime import date
from pydantic import BaseModel


class PagoBase(BaseModel):
    nroVoucher: str
    medioPago: str
    monto: float
    fecha: date
    idInscripcion: int
    foto: str | None = None
    Estado: bool = False


class PagoCreate(PagoBase):
    pass


class PagoRead(PagoBase):
    id: int

    model_config = {"from_attributes": True}


class PagoDetalleRead(PagoRead):
    tipoPago: str | None = None
    nombreAlumno: str
    aPaterno: str | None = None
    aMaterno: str | None = None
    nombreCiclo: str
