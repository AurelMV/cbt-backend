from typing import List
from pydantic import BaseModel


class StatCard(BaseModel):
    label: str
    value: str | int | float
    description: str | None = None
    trend: float | None = None  # Percentage change, optional


class ChartDataPoint(BaseModel):
    name: str
    value: int | float


class DashboardStats(BaseModel):
    total_alumnos: int
    total_inscripciones: int
    ingresos_totales: float
    pagos_pendientes: int


class DashboardCharts(BaseModel):
    ingresos_por_mes: List[ChartDataPoint]
    inscripciones_por_programa: List[ChartDataPoint]
    inscripciones_por_ciclo: List[ChartDataPoint]
    estado_pagos: List[ChartDataPoint]


class DashboardResponse(BaseModel):
    stats: DashboardStats
    charts: DashboardCharts
