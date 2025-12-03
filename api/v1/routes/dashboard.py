from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from db.base import get_session
from db.models.enrollment import Alumno, Inscripcion, Pago
from db.models.programa import ProgramaEstudios
from db.models.academic import Ciclo
from schemas.dashboard import (
    DashboardResponse,
    DashboardStats,
    DashboardCharts,
    ChartDataPoint,
)

router = APIRouter()


@router.get("/", response_model=DashboardResponse)
def get_dashboard_data(db: Session = Depends(get_session)):
    """
    Get aggregated data for the dashboard.
    """

    # --- Stats ---
    total_alumnos = db.exec(select(func.count(Alumno.id))).one() or 0
    total_inscripciones = db.exec(select(func.count(Inscripcion.id))).one() or 0
    ingresos_totales = db.exec(select(func.sum(Pago.monto))).one() or 0.0

    # Assuming 'Pagado' is the status for completed payments.
    # Adjust logic if 'EstadoPago' uses different values (e.g., boolean or different strings).
    # If EstadoPago is not 'Pagado', we consider it pending.
    pagos_pendientes = (
        db.exec(select(func.count(Pago.id)).where(Pago.Estado == False)).one() or 0
    )

    stats = DashboardStats(
        total_alumnos=total_alumnos,
        total_inscripciones=total_inscripciones,
        ingresos_totales=ingresos_totales,
        pagos_pendientes=pagos_pendientes,
    )

    # --- Charts ---

    # 1. Ingresos por Mes
    # Determine date formatting function based on dialect
    # Check engine dialect directly or via session bind
    dialect_name = db.bind.dialect.name if db.bind else "sqlite"

    if dialect_name == "postgresql" or dialect_name == "postgres":
        date_format_func = func.to_char(Pago.fecha, "YYYY-MM")
    else:
        # Fallback to SQLite
        date_format_func = func.strftime("%Y-%m", Pago.fecha)

    ingresos_query = (
        select(
            date_format_func.label("mes"),
            func.sum(Pago.monto).label("total"),
        )
        .group_by(date_format_func)
        .order_by("mes")
    )
    ingresos_results = db.exec(ingresos_query).all()

    ingresos_chart = [
        ChartDataPoint(name=row.mes, value=row.total)
        for row in ingresos_results
        if row.mes is not None
    ]

    # 2. Inscripciones por Programa
    prog_query = (
        select(ProgramaEstudios.nombrePrograma, func.count(Inscripcion.id))
        .join(ProgramaEstudios, Inscripcion.idPrograma == ProgramaEstudios.id)
        .group_by(ProgramaEstudios.nombrePrograma)
    )
    prog_results = db.exec(prog_query).all()

    prog_chart = [
        ChartDataPoint(name=row[0], value=row[1]) for i, row in enumerate(prog_results)
    ]

    # 3. Inscripciones por Ciclo
    ciclo_query = (
        select(Ciclo.nombreCiclo, func.count(Inscripcion.id))
        .join(Ciclo, Inscripcion.idCiclo == Ciclo.id)
        .group_by(Ciclo.nombreCiclo)
    )
    ciclo_results = db.exec(ciclo_query).all()

    ciclo_chart = [ChartDataPoint(name=row[0], value=row[1]) for row in ciclo_results]

    # 4. Estado de Pagos
    estado_query = select(Pago.Estado, func.count(Pago.id)).group_by(Pago.Estado)
    estado_results = db.exec(estado_query).all()

    estado_chart = [
        ChartDataPoint(
            name="Pagado" if row[0] else "Pendiente",
            value=row[1],
        )
        for i, row in enumerate(estado_results)
    ]

    charts = DashboardCharts(
        ingresos_por_mes=ingresos_chart,
        inscripciones_por_programa=prog_chart,
        inscripciones_por_ciclo=ciclo_chart,
        estado_pagos=estado_chart,
    )

    return DashboardResponse(stats=stats, charts=charts)
