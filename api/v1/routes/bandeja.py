from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from db.base import get_session
from db.models.preinscripcion import PreInscripcion, PrePago
from db.models.enrollment import Alumno, Inscripcion, Pago
from db.models.academic import Clase, Grupo
from db.repositories import preinscripcion_repository as pre_repo
from db.repositories import prepago_repository as prepay_repo
from db.repositories import pago_repository
from db.repositories import alumno_repository
from db.repositories import inscripcion_repository
from schemas.inscripcion import InscripcionRead

router = APIRouter(prefix="/bandeja", tags=["bandeja"])


@router.get("/counts")
def get_counts(session: Session = Depends(get_session)):
    pre_pend = len(session.exec(select(PreInscripcion).where(PreInscripcion.estado == "pendiente")).all())
    pay_pend = len(session.exec(select(Pago).where(Pago.Estado == False)).all())  # noqa: E712
    return {"preinscripcionesPendientes": pre_pend, "pagosPendientes": pay_pend}


@router.get("/preinscripciones")
def list_preinscripciones_pendientes(session: Session = Depends(get_session)):
    # Devolver preinscripciones con sus prepagos asociados (si existen)
    pre_list = pre_repo.list_by_estado(session, "pendiente")
    result = []
    for pre in pre_list:
        pagos = prepay_repo.list_by_preinscripcion(session, pre.id)
        # Serializar solo campos de columna para evitar ciclos (relaciones)
        result.append({
            "preinscripcion": pre.model_dump(),
            "prepagos": [p.model_dump() for p in pagos],
        })
    return result


@router.post("/preinscripciones/{pre_id}/aprobar", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED)
def aprobar_preinscripcion(
    pre_id: int,
    payload: dict,
    session: Session = Depends(get_session)
):
    # payload: {"idGrupo": int, "idClase": int}
    pre = pre_repo.get(session, pre_id)
    if pre is None:
        raise HTTPException(status_code=404, detail="Preinscripción no encontrada")

    id_grupo = int(payload.get("idGrupo"))
    id_clase = int(payload.get("idClase"))

    if session.get(Grupo, id_grupo) is None:
        raise HTTPException(status_code=400, detail="Grupo no existe")
    clase = session.get(Clase, id_clase)
    if clase is None:
        raise HTTPException(status_code=400, detail="Clase no existe")
    if clase.grupo_id != id_grupo:
        raise HTTPException(status_code=400, detail="La clase no pertenece al grupo indicado")

    # Asegurar alumno: por nroDocumento
    alumno = session.exec(select(Alumno).where(Alumno.nroDocumento == pre.nroDocumento)).first()
    if alumno is None:
        alumno = Alumno(
            nombreAlumno=pre.nombreAlumno,
            aMaterno=pre.aMaterno,
            aPaterno=pre.aPaterno,
            sexo=pre.sexo,
            telefonoEstudiante=pre.telefonoEstudiante,
            telefonoApoderado=pre.telefonoApoderado,
            fechaNacimiento=pre.fechaNacimiento,
            email=pre.email,
            anoCulminado=pre.anoCulminado,
            Direccion=pre.Direccion,
            nroDocumento=pre.nroDocumento,
            idColegio=pre.idColegio,
        )
        alumno = alumno_repository.create(session, alumno)

    # Crear Inscripción con estado de pago 'aceptado'
    codigo = f"INS-{pre.id:06d}"
    ins = Inscripcion(
        turno="MAÑANA",
        fecha=pre.fechaNacimiento,  # placeholder: idealmente fecha actual
        Estado=True,
        idAlumno=alumno.id,
        idPrograma=pre.idPrograma,
        idCiclo=pre.idCiclo,
        idClase=id_clase,
        Codigo=codigo,
        EstadoPago="aceptado",
        TipoPago=(prepay_repo.list_by_preinscripcion(session, pre.id)[0].TipoPago if prepay_repo.list_by_preinscripcion(session, pre.id) else "N/A"),
    )
    ins = inscripcion_repository.create(session, ins)

    # Crear Pago (aprobado) desde primer prepago si existe
    prepagos = prepay_repo.list_by_preinscripcion(session, pre.id)
    if prepagos:
        p = prepagos[0]
        pago = Pago(
            nroVoucher=p.nroVoucher,
            medioPago=p.medioPago,
            monto=p.monto,
            fecha=p.fecha,
            idInscripcion=ins.id,
            foto=p.foto,
            Estado=True,  # aprobado
        )
        pago_repository.create(session, pago)
        # Marcar prepagos como aceptados
        for pp in prepagos:
            pp.estado = "aceptado"
            prepay_repo.update(session, pp)

    # Marcar preinscripción aceptada
    pre.estado = "aceptado"
    pre_repo.update(session, pre)

    return ins


@router.post("/preinscripciones/{pre_id}/rechazar")
def rechazar_preinscripcion(pre_id: int, session: Session = Depends(get_session)):
    pre = pre_repo.get(session, pre_id)
    if pre is None:
        raise HTTPException(status_code=404, detail="Preinscripción no encontrada")
    pre.estado = "rechazado"
    pre_repo.update(session, pre)
    for pp in prepay_repo.list_by_preinscripcion(session, pre.id):
        pp.estado = "rechazado"
        prepay_repo.update(session, pp)
    return {"status": "ok"}


@router.get("/pagos")
def list_pagos_pendientes(session: Session = Depends(get_session)):
    # Listar pagos reales en estado pendiente (Estado=False)
    pagos = session.exec(select(Pago).where(Pago.Estado == False)).all()  # noqa: E712
    result = []
    for p in pagos:
        ins = session.get(Inscripcion, p.idInscripcion)
        alumno = session.get(Alumno, ins.idAlumno) if ins else None
        result.append({
            "pago": p,
            "inscripcion": ins,
            "alumno": alumno,
        })
    return result


@router.post("/pagos/{pago_id}/aprobar")
def aprobar_pago(pago_id: int, session: Session = Depends(get_session)):
    pago = session.get(Pago, pago_id)
    if pago is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    pago.Estado = True
    session.add(pago)
    session.commit()
    session.refresh(pago)
    return {"status": "ok"}


@router.post("/pagos/{pago_id}/rechazar")
def rechazar_pago(pago_id: int, session: Session = Depends(get_session)):
    pago = session.get(Pago, pago_id)
    if pago is None:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    # Opción simple: eliminar pago rechazado
    session.delete(pago)
    session.commit()
    return {"status": "ok"}
