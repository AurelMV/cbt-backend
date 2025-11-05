from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
from sqlmodel import Session, select

from db.base import engine, init_db
from db.models.location import Departamento, Provincia, Distrito, Colegio


def _norm(s: str) -> str:
    if s is None:
        return ""
    return " ".join(str(s).strip().upper().split())


def _pick_column(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    cols_norm = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in cols_norm:
            return cols_norm[cand.lower()]
    # fallback: try contains-like search
    for c in df.columns:
        lc = c.lower()
        for cand in candidates:
            if cand.lower() in lc:
                return c
    return None


def _get_or_create_dep(session: Session, nombre: str) -> Departamento:
    nombre = _norm(nombre)
    dep = session.exec(select(Departamento).where(Departamento.nombreDepartamento == nombre)).first()
    if dep:
        return dep
    dep = Departamento(nombreDepartamento=nombre)
    session.add(dep)
    session.commit()
    session.refresh(dep)
    return dep


def _get_or_create_prov(session: Session, nombre: str, dep: Departamento) -> Provincia:
    nombre = _norm(nombre)
    prov = session.exec(
        select(Provincia).where((Provincia.nombreProvincia == nombre) & (Provincia.departamento_id == dep.id))
    ).first()
    if prov:
        return prov
    prov = Provincia(nombreProvincia=nombre, departamento_id=dep.id)
    session.add(prov)
    session.commit()
    session.refresh(prov)
    return prov


def _get_or_create_dist(session: Session, nombre: str, prov: Provincia) -> Distrito:
    nombre = _norm(nombre)
    dist = session.exec(
        select(Distrito).where((Distrito.nombreDistrito == nombre) & (Distrito.provincia_id == prov.id))
    ).first()
    if dist:
        return dist
    dist = Distrito(nombreDistrito=nombre, provincia_id=prov.id)
    session.add(dist)
    session.commit()
    session.refresh(dist)
    return dist


def _get_or_create_colegio(session: Session, nombre: str, dist: Distrito) -> Colegio:
    nombre = _norm(nombre)
    col = session.exec(
        select(Colegio).where((Colegio.nombreColegio == nombre) & (Colegio.distrito_id == dist.id))
    ).first()
    if col:
        return col
    col = Colegio(nombreColegio=nombre, distrito_id=dist.id)
    session.add(col)
    session.commit()
    session.refresh(col)
    return col


def load_iiee_from_xls(xls_path: str | Path) -> dict:
    """
    Carga IIEE (colegios) desde un archivo .xls con columnas de ubicación y nivel.
    - Filtra solo nivel secundario (cualquier gestión pública/privada).
    - Inserta Departamento, Provincia, Distrito y Colegio.

    Devuelve resumen de contadores.
    """
    init_db()

    p = Path(xls_path)
    if not p.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {p}")

    # Leer hoja principal; si el .xls es en realidad HTML exportado, caer a read_html
    df = None
    try:
        df = pd.read_excel(p, engine="xlrd")
    except Exception:
        # Intentar como HTML
        tables = pd.read_html(str(p))
        if not tables:
            raise
        # Elegir la tabla con más columnas
        df = max(tables, key=lambda t: t.shape[1])

    # Detectar columnas probables
    col_dep = _pick_column(df, ["departamento", "depa", "dpto"])
    col_prov = _pick_column(df, ["provincia", "prov"])
    col_dist = _pick_column(df, ["distrito", "dist", "distr"])
    col_nivel = _pick_column(df, ["nivel", "nivel educativo", "niv_edu", "educativo"])
    col_gestion = _pick_column(df, ["gestion", "gestión", "dependencia", "sector"])
    col_nombre = _pick_column(
        df,
        [
            "nombre ie",
            "institucion educativa",
            "institución educativa",
            "colegio",
            "nombre",
            "ie",
        ],
    )

    required = {
        "departamento": col_dep,
        "provincia": col_prov,
        "distrito": col_dist,
        "nivel": col_nivel,
        "gestion": col_gestion,
        "nombre": col_nombre,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise ValueError(f"No se encontraron columnas requeridas en el .xls: {missing}")

    # Normalizar y filtrar
    df_work = df[[col_dep, col_prov, col_dist, col_nivel, col_gestion, col_nombre]].copy()
    df_work.columns = ["dep", "prov", "dist", "nivel", "gestion", "nombre"]

    df_work["nivel_norm"] = df_work["nivel"].astype(str).str.upper()
    df_work["gestion_norm"] = df_work["gestion"].astype(str).str.upper()

    # Filtrar SECUNDARIA
    df_work = df_work[df_work["nivel_norm"].str.contains("SECUND", na=False)]

    # Filtrar gestiones públicas/privadas
    allowed_g = ["PUBLIC", "PÚBLIC", "PRIVAD"]
    mask_g = False
    for g in allowed_g:
        mask_g = mask_g | df_work["gestion_norm"].str.contains(g, na=False)
    df_work = df_work[mask_g]

    counts = {
        "departamentos_inserted": 0,
        "provincias_inserted": 0,
        "distritos_inserted": 0,
        "colegios_inserted": 0,
        "rows_processed": 0,
    }

    with Session(engine) as session:
        # Insertar por filas
        for _, row in df_work.iterrows():
            dep = _get_or_create_dep(session, row["dep"])
            prov = _get_or_create_prov(session, row["prov"], dep)
            dist = _get_or_create_dist(session, row["dist"], prov)
            before = session.exec(select(Colegio).where((Colegio.nombreColegio == _norm(row["nombre"])) & (Colegio.distrito_id == dist.id))).first()
            _get_or_create_colegio(session, row["nombre"], dist)

            # Contabilizar inserciones nuevas
            if session.get(Departamento, dep.id) and session.exec(select(Departamento).where(Departamento.id == dep.id)).first():
                pass
            if session.get(Provincia, prov.id) and session.exec(select(Provincia).where(Provincia.id == prov.id)).first():
                pass
            if session.get(Distrito, dist.id) and session.exec(select(Distrito).where(Distrito.id == dist.id)).first():
                pass
            if before is None:
                counts["colegios_inserted"] += 1

            counts["rows_processed"] += 1

    # Los contadores de dep/prov/dist exactos serían costosos por fila; podemos devolver totales actuales
    with Session(engine) as session:
        counts["departamentos_total"] = len(session.exec(select(Departamento)).all())
        counts["provincias_total"] = len(session.exec(select(Provincia)).all())
        counts["distritos_total"] = len(session.exec(select(Distrito)).all())
        counts["colegios_total"] = len(session.exec(select(Colegio)).all())

    return counts


if __name__ == "__main__":
    xls = Path(__file__).resolve().parents[1] / "listado_iiee.xls"
    summary = load_iiee_from_xls(xls)
    print("Resumen importación IIEE (secundaria público/privado):")
    for k, v in summary.items():
        print(f"- {k}: {v}")
