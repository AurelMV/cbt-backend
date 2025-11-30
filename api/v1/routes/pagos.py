from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlmodel import Session

from db.base import get_session
from db.models.enrollment import Pago as PagoModel, Inscripcion, Alumno
from db.models.academic import Ciclo
from db.models.programa import ProgramaEstudios
from db.repositories.inscripcion_repository import get as get_inscripcion
from db.repositories.pago_repository import (
    list_paginated_with_details,
    create,
)
from schemas.pagination import Page
from schemas.pago import PagoCreate, PagoRead, PagoDetalleRead
from services.pdf_service import generate_pago_pdf


router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/{id}/comprobante", response_class=Response)
async def get_pago_comprobante(id: int, session: Session = Depends(get_session)):
    pago = session.get(PagoModel, id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    inscripcion = session.get(Inscripcion, pago.idInscripcion)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción asociada no encontrada")
        
    alumno = session.get(Alumno, inscripcion.idAlumno)
    ciclo = session.get(Ciclo, inscripcion.idCiclo)
    programa = session.get(ProgramaEstudios, inscripcion.idPrograma)
    
    data = {
        "id": pago.id,
        "nombre": alumno.nombreAlumno if alumno else "Desconocido",
        "paterno": alumno.aPaterno if alumno else "",
        "materno": alumno.aMaterno if alumno else "",
        "dni": alumno.nroDocumento if alumno else "—",
        "ciclo": ciclo.nombreCiclo if ciclo else "—",
        "programa": programa.nombrePrograma if programa else "—",
        "codigo_inscripcion": inscripcion.Codigo,
        
        "voucher_code": pago.nroVoucher,
        "monto": f"{pago.monto:.2f}",
        "fecha_pago": str(pago.fecha),
        "medio_pago": pago.medioPago,
        "estado": "Aprobado" if pago.Estado else "Pendiente"
    }
    
    try:
        pdf_bytes = generate_pago_pdf(data, voucher_base64=pago.foto)
    except Exception as e:
        print(f"Error generando PDF de pago: {e}")
        raise HTTPException(status_code=500, detail="Error generando el PDF")
    
    return Response(content=pdf_bytes, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=comprobante-pago-{id}.pdf"
    })


@router.get("/", response_model=Page[PagoDetalleRead])

def get_pagos(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(15, ge=1, le=100),
    page: int | None = Query(None, ge=0, description="Número de página (0-based)"),
    q: str | None = Query(
        None, description="Busca por número de voucher o medio de pago"
    ),
    id_ciclo: int | None = Query(None, alias="idCiclo", ge=1),
    estado: bool | None = Query(
        None, description="Filtra por estado del pago (true=aprobado, false=pendiente)"
    ),
    tipo_pago: str | None = Query(None, alias="tipoPago", description="Filtra por tipo de pago de la inscripción"),
):
    effective_offset = offset if page is None else page * limit
    result = list_paginated_with_details(
        session,
        q=q,
        offset=effective_offset,
        limit=limit,
        id_ciclo=id_ciclo,
        estado=estado,
        tipo_pago=tipo_pago,
    )
    result["items"] = [PagoDetalleRead(**item) for item in result["items"]]
    return result


@router.post("/", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def create_pago(payload: PagoCreate, session: Session = Depends(get_session)):
    # FK validation
    if get_inscripcion(session, payload.idInscripcion) is None:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")

    pago = PagoModel(**payload.model_dump())
    return create(session, pago)
