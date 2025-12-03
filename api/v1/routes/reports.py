from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from typing import List, Optional

from db.base import get_session
from services.report_service import ReportService

router = APIRouter()

@router.get("/{entity_type}/{entity_id}/export")
async def export_report(
    entity_type: str,
    entity_id: int,
    format: str = Query(..., regex="^(pdf|excel)$"),
    columns: str = Query(..., description="Comma separated list of columns"),
    db: Session = Depends(get_session)
):
    service = ReportService(db)
    
    # Fetch data based on entity type
    if entity_type == "ciclo":
        data = service.get_ciclo_data(entity_id)
    elif entity_type == "grupo":
        data = service.get_grupo_data(entity_id)
    elif entity_type == "clase":
        data = service.get_clase_data(entity_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid entity type")
        
    if not data:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    column_list = [c.strip() for c in columns.split(",")]
    
    if format == "pdf":
        buffer = service.generate_pdf(data, column_list)
        media_type = "application/pdf"
        filename = f"reporte_{entity_type}_{entity_id}.pdf"
    else:
        buffer = service.generate_excel(data, column_list)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"reporte_{entity_type}_{entity_id}.xlsx"
        
    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
