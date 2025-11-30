from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlmodel import Session, select

from db.base import get_session
from db.models.preinscripcion import PreInscripcion, PrePago
from db.models.location import Colegio, Distrito, Provincia, Departamento
from db.models.academic import Ciclo
from db.models.programa import ProgramaEstudios
from db.repositories import preinscripcion_repository as repo
from schemas.preinscripcion import PreInscripcionCreate, PreInscripcionRead
from services.pdf_service import generate_preinscripcion_pdf

router = APIRouter(prefix="/preinscripciones", tags=["preinscripciones"])


@router.get("/{id}/comprobante", response_class=Response)
async def get_preinscripcion_comprobante(id: int, session: Session = Depends(get_session)):
    pre = session.get(PreInscripcion, id)
    if not pre:
        raise HTTPException(status_code=404, detail="Preinscripción no encontrada")
    
    # Obtener datos relacionados
    colegio = session.get(Colegio, pre.idColegio)
    programa = session.get(ProgramaEstudios, pre.idPrograma)
    
    distrito = session.get(Distrito, colegio.distrito_id) if colegio else None
    provincia = session.get(Provincia, distrito.provincia_id) if distrito else None
    departamento = session.get(Departamento, provincia.departamento_id) if provincia else None
    
    # Buscar el pago
    statement = select(PrePago).where(PrePago.idInscripcion == id)
    pago = session.exec(statement).first()
    
    # Construir diccionario de datos
    data = {
        "id": pre.id,
        "nombre": pre.nombreAlumno,
        "paterno": pre.aPaterno,
        "materno": pre.aMaterno,
        "dni": pre.nroDocumento,
        "email": pre.email,
        "telefono": pre.telefonoEstudiante,
        "colegio": colegio.nombreColegio if colegio else "Desconocido",
        "programa": programa.nombrePrograma if programa else "Desconocido",
        "departamento": departamento.nombreDepartamento if departamento else "—",
        "provincia": provincia.nombreProvincia if provincia else "—",
        "distrito": distrito.nombreDistrito if distrito else "—",
    }
    
    voucher_img = None
    if pago:
        data["voucher_code"] = pago.nroVoucher
        data["monto"] = f"{pago.monto:.2f}"
        data["fecha_pago"] = str(pago.fecha)
        data["medio_pago"] = pago.medioPago
        voucher_img = pago.foto
        # Debug log
        print(f"[PDF] Pago ID: {pago.id}, Foto presente: {bool(pago.foto)}, Len: {len(pago.foto) if pago.foto else 0}")
    else:
        data["voucher_code"] = "Pendiente"
        data["monto"] = "0.00"
        data["fecha_pago"] = "—"
        data["medio_pago"] = "—"

    try:
        pdf_bytes = generate_preinscripcion_pdf(data, voucher_base64=voucher_img)
    except Exception as e:
        # Log error real en consola del servidor
        print(f"Error generando PDF: {e}")
        raise HTTPException(status_code=500, detail="Error generando el PDF")
    
    return Response(content=pdf_bytes, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=comprobante-pre-{id}.pdf"
    })


@router.get("/", response_model=list[PreInscripcionRead])
async def list_preinscripciones(session: Session = Depends(get_session)):
    return repo.list_all(session)


@router.post("/", response_model=PreInscripcionRead, status_code=status.HTTP_201_CREATED)
async def create_preinscripcion(
    data: PreInscripcionCreate, session: Session = Depends(get_session)
):
    # Validaciones de FK
    if session.get(Colegio, data.idColegio) is None:
        raise HTTPException(status_code=400, detail="idColegio no existe")
    if session.get(Ciclo, data.idCiclo) is None:
        raise HTTPException(status_code=400, detail="idCiclo no existe")
    if session.get(ProgramaEstudios, data.idPrograma) is None:
        raise HTTPException(status_code=400, detail="idPrograma no existe")

    entity = PreInscripcion(**data.model_dump())
    return repo.create(session, entity)
