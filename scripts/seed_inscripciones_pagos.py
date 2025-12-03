from __future__ import annotations

from datetime import date, timedelta
from typing import Tuple

from sqlmodel import Session, select

from db.base import engine, init_db
from db.models.location import Departamento, Provincia, Distrito, Colegio
from db.models.programa import ProgramaEstudios
from db.models.academic import Ciclo, Grupo, Clase
from db.models.enrollment import Alumno, Inscripcion, Pago


def get_or_create_departamento(session: Session, nombre: str) -> Departamento:
    dep = session.exec(select(Departamento).where(Departamento.nombreDepartamento == nombre)).first()
    if dep:
        return dep
    dep = Departamento(nombreDepartamento=nombre)
    session.add(dep)
    session.commit()
    session.refresh(dep)
    return dep


def get_or_create_provincia(session: Session, nombre: str, departamento: Departamento) -> Provincia:
    prov = session.exec(
        select(Provincia).where(
            (Provincia.nombreProvincia == nombre) & (Provincia.departamento_id == departamento.id)
        )
    ).first()
    if prov:
        return prov
    prov = Provincia(nombreProvincia=nombre, departamento_id=departamento.id)
    session.add(prov)
    session.commit()
    session.refresh(prov)
    return prov


def get_or_create_distrito(session: Session, nombre: str, provincia: Provincia) -> Distrito:
    dist = session.exec(
        select(Distrito).where((Distrito.nombreDistrito == nombre) & (Distrito.provincia_id == provincia.id))
    ).first()
    if dist:
        return dist
    dist = Distrito(nombreDistrito=nombre, provincia_id=provincia.id)
    session.add(dist)
    session.commit()
    session.refresh(dist)
    return dist


def get_or_create_colegio(session: Session, nombre: str, distrito: Distrito) -> Colegio:
    col = session.exec(
        select(Colegio).where((Colegio.nombreColegio == nombre) & (Colegio.distrito_id == distrito.id))
    ).first()
    if col:
        return col
    col = Colegio(nombreColegio=nombre, distrito_id=distrito.id)
    session.add(col)
    session.commit()
    session.refresh(col)
    return col


def get_or_create_programa(session: Session, nombre: str = "Programa Demo") -> ProgramaEstudios:
    prog = session.exec(select(ProgramaEstudios).where(ProgramaEstudios.nombrePrograma == nombre)).first()
    if prog:
        return prog
    prog = ProgramaEstudios(nombrePrograma=nombre)
    session.add(prog)
    session.commit()
    session.refresh(prog)
    return prog


def get_or_create_ciclo_grupo_clase(session: Session) -> Tuple[Ciclo, Grupo, Clase]:
    today = date.today()
    ciclo_nombre = f"CICLO-DEMO-{today.year}"
    ciclo = session.exec(select(Ciclo).where(Ciclo.nombreCiclo == ciclo_nombre)).first()
    if not ciclo:
        ciclo = Ciclo(
            nombreCiclo=ciclo_nombre,
            fechaInicio=today,
            fechaFin=today + timedelta(days=30),
            estado=True,
        )
        session.add(ciclo)
        session.commit()
        session.refresh(ciclo)

    grupo_nombre = "GRUPO-DEMO-A"
    grupo = session.exec(select(Grupo).where((Grupo.nombreGrupo == grupo_nombre) & (Grupo.ciclo_id == ciclo.id))).first()
    if not grupo:
        grupo = Grupo(nombreGrupo=grupo_nombre, aforo=50, estado=True, ciclo_id=ciclo.id)
        session.add(grupo)
        session.commit()
        session.refresh(grupo)

    clase_codigo = "CLASE-DEMO-1"
    clase = session.exec(select(Clase).where((Clase.codigoClase == clase_codigo) & (Clase.grupo_id == grupo.id))).first()
    if not clase:
        clase = Clase(codigoClase=clase_codigo, grupo_id=grupo.id)
        session.add(clase)
        session.commit()
        session.refresh(clase)

    return ciclo, grupo, clase


def create_demo_alumno(session: Session, idx: int, colegio: Colegio) -> Alumno:
    nombre = f"Alumno{idx:03d}"
    alumno = Alumno(
        nombreAlumno=nombre,
        aMaterno="Perez",
        aPaterno="Gomez",
        sexo="M" if idx % 2 == 0 else "F",
        telefonoEstudiante=f"900000{idx:03d}",
        telefonoApoderado=f"910000{idx:03d}",
        fechaNacimiento=date(2006, 1, 1),
        email=f"{nombre.lower()}@demo.local",
        anoCulminado=2024,
        Direccion=f"Calle Demo {idx}",
        nroDocumento=f"DNI{10000000 + idx}",
        idColegio=colegio.id,
    )
    session.add(alumno)
    session.commit()
    session.refresh(alumno)
    return alumno


def seed_inscripciones_pagos(cantidad: int = 50) -> dict:
    init_db()
    created_ins = 0
    created_pag = 0

    with Session(engine) as session:
        # Datos base de ubicación y colegio
        dep = get_or_create_departamento(session, "DEP-DEMO")
        prov = get_or_create_provincia(session, "PROV-DEMO", dep)
        dist = get_or_create_distrito(session, "DIST-DEMO", prov)
        col = get_or_create_colegio(session, "COLEGIO-DEMO", dist)

        # Programa, Ciclo/Grupo/Clase
        prog = get_or_create_programa(session, "Programa Demo")
        ciclo, _grupo, clase = get_or_create_ciclo_grupo_clase(session)

        for i in range(1, cantidad + 1):
            alumno = create_demo_alumno(session, i, col)

            ins = Inscripcion(
                turno="Mañana" if i % 2 == 0 else "Tarde",
                fecha=date.today(),
                Estado=True,
                idAlumno=alumno.id,
                idPrograma=prog.id,
                idCiclo=ciclo.id,
                idClase=clase.id,
                Codigo=f"INS-DEMO-{i:04d}",
                EstadoPago="pagado",
                TipoPago="transferencia" if i % 2 == 0 else "efectivo",
            )
            session.add(ins)
            session.commit()
            session.refresh(ins)
            created_ins += 1

            pago = Pago(
                nroVoucher=f"VCH-DEMO-{i:04d}",
                medioPago="transferencia" if i % 2 == 0 else "deposito",
                monto=100.0 + i,
                fecha=date.today(),
                idInscripcion=ins.id,
                foto=None,
                Estado=True,
            )
            session.add(pago)
            session.commit()
            created_pag += 1

        # Totales creados con prefijo DEMO
        total_ins_demo = len(
            session.exec(select(Inscripcion).where(Inscripcion.Codigo.like("INS-DEMO-%"))).all()
        )
        total_pago_demo = len(
            session.exec(select(Pago).where(Pago.nroVoucher.like("VCH-DEMO-%"))).all()
        )

    return {
        "inscripciones_creadas": created_ins,
        "pagos_creados": created_pag,
        "inscripciones_demo_totales": total_ins_demo,
        "pagos_demo_totales": total_pago_demo,
    }


if __name__ == "__main__":
    summary = seed_inscripciones_pagos(50)
    print("Seeding completado:", summary)
