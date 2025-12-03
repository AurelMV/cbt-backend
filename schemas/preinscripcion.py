from datetime import date
from pydantic import BaseModel, EmailStr


class PreInscripcionCreate(BaseModel):
    nombreAlumno: str
    aMaterno: str
    aPaterno: str
    sexo: str
    telefonoEstudiante: str
    telefonoApoderado: str
    fechaNacimiento: date
    email: EmailStr
    anoCulminado: int
    Direccion: str
    nroDocumento: str
    idColegio: int
    idCiclo: int
    idPrograma: int


class PreInscripcionRead(BaseModel):
    id: int
    nombreAlumno: str
    aMaterno: str
    aPaterno: str
    sexo: str
    telefonoEstudiante: str
    telefonoApoderado: str
    fechaNacimiento: date
    email: EmailStr
    anoCulminado: int
    Direccion: str
    nroDocumento: str
    idColegio: int
    idCiclo: int
    idPrograma: int

    model_config = {"from_attributes": True}


class PrePagoCreate(BaseModel):
    nroVoucher: str
    medioPago: str
    monto: float
    fecha: date
    idInscripcion: int
    foto: str | None = None
    TipoPago: str


class PrePagoRead(BaseModel):
    id: int
    nroVoucher: str
    medioPago: str
    monto: float
    fecha: date
    idInscripcion: int
    foto: str | None
    TipoPago: str

    model_config = {"from_attributes": True}
