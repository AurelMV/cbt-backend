from pathlib import Path

from sqlmodel import Session, select, delete

from db.base import engine, init_db
from db.models.location import Departamento, Provincia, Distrito, Colegio
from db.models.enrollment import Alumno, Inscripcion, Pago
from db.models.preinscripcion import PreInscripcion, PrePago
from scripts.import_iiee_from_xls import load_iiee_from_xls


def clear_location_tables():
    # Borrar respetando FKs:
    # Pago -> Inscripcion -> Alumno -> (Colegio)
    # PrePago -> PreInscripcion -> (Colegio)
    # Luego: Colegio -> Distrito -> Provincia -> Departamento
    with Session(engine) as session:
        session.exec(delete(Pago))
        session.exec(delete(Inscripcion))
        session.exec(delete(PrePago))
        session.exec(delete(PreInscripcion))
        session.exec(delete(Alumno))
        session.exec(delete(Colegio))
        session.exec(delete(Distrito))
        session.exec(delete(Provincia))
        session.exec(delete(Departamento))
        session.commit()


def test_import_iiee_xls():
    init_db()
    clear_location_tables()

    xls_path = Path(__file__).resolve().parents[1] / "listado_iiee.xls"
    summary = load_iiee_from_xls(xls_path)

    # Validaciones básicas
    assert summary.get("rows_processed", 0) > 0, "No se procesaron filas"
    with Session(engine) as session:
        dep_count = len(session.exec(select(Departamento)).all())
        prov_count = len(session.exec(select(Provincia)).all())
        dist_count = len(session.exec(select(Distrito)).all())
        col_count = len(session.exec(select(Colegio)).all())
        assert dep_count > 0, "No se insertaron departamentos"
        assert prov_count > 0, "No se insertaron provincias"
        assert dist_count > 0, "No se insertaron distritos"
        assert col_count > 0, "No se insertaron colegios (secundaria)"

    print("Importación IIEE desde XLS OK. Totales:", summary)


if __name__ == "__main__":
    test_import_iiee_xls()
    print("Prueba ejecutada correctamente.")
