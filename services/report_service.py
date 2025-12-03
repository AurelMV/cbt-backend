from io import BytesIO
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from sqlmodel import Session, select
from db.models.academic import Ciclo, Grupo, Clase
from db.models.enrollment import Inscripcion, Alumno
from db.models.programa import ProgramaEstudios

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_ciclo_data(self, ciclo_id: int) -> Dict[str, Any]:
        ciclo = self.db.get(Ciclo, ciclo_id)
        if not ciclo:
            return None
        
        # Fetch all inscriptions for this cycle
        statement = select(Inscripcion).where(Inscripcion.idCiclo == ciclo_id, Inscripcion.Estado == True)
        inscripciones = self.db.exec(statement).all()
        
        return self._process_inscriptions(inscripciones, f"Reporte del Ciclo: {ciclo.nombreCiclo}")

    def get_grupo_data(self, grupo_id: int) -> Dict[str, Any]:
        grupo = self.db.get(Grupo, grupo_id)
        if not grupo:
            return None
            
        # Fetch inscriptions for classes in this group
        # Join Inscripcion -> Clase -> Grupo
        statement = (
            select(Inscripcion)
            .join(Clase)
            .where(Clase.grupo_id == grupo_id, Inscripcion.Estado == True)
        )
        inscripciones = self.db.exec(statement).all()
        
        return self._process_inscriptions(inscripciones, f"Reporte del Grupo: {grupo.nombreGrupo}")

    def get_clase_data(self, clase_id: int) -> Dict[str, Any]:
        clase = self.db.get(Clase, clase_id)
        if not clase:
            return None
            
        statement = select(Inscripcion).where(Inscripcion.idClase == clase_id, Inscripcion.Estado == True)
        inscripciones = self.db.exec(statement).all()
        
        return self._process_inscriptions(inscripciones, f"Reporte de la Clase: {clase.codigoClase}")

    def _process_inscriptions(self, inscripciones: List[Inscripcion], title: str) -> Dict[str, Any]:
        data = []
        for ins in inscripciones:
            alumno = self.db.get(Alumno, ins.idAlumno)
            programa = self.db.get(ProgramaEstudios, ins.idPrograma)
            clase = self.db.get(Clase, ins.idClase)
            grupo = self.db.get(Grupo, clase.grupo_id) if clase else None
            ciclo = self.db.get(Ciclo, ins.idCiclo)
            
            if alumno:
                data.append({
                    "Codigo": ins.Codigo,
                    "DNI": alumno.nroDocumento,
                    "Alumno": f"{alumno.aPaterno} {alumno.aMaterno}, {alumno.nombreAlumno}",
                    "Programa": programa.nombrePrograma if programa else "Sin Programa",
                    "Clase": clase.codigoClase if clase else "Sin Clase",
                    "Grupo": grupo.nombreGrupo if grupo else "Sin Grupo",
                    "Ciclo": ciclo.nombreCiclo if ciclo else "Sin Ciclo",
                    "Telefono": alumno.telefonoEstudiante,
                    "Email": alumno.email,
                    "Direccion": alumno.Direccion
                })
        
        # Sort by Alumno name
        data.sort(key=lambda x: x["Alumno"])
        return {"title": title, "data": data}

    def generate_pdf(self, report_data: Dict[str, Any], columns: List[str]) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center
        )
        elements.append(Paragraph(report_data["title"], title_style))
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
        elements.append(Spacer(1, 20))
        
        # Table Data
        data = report_data["data"]
        if not data:
            elements.append(Paragraph("No hay datos para mostrar.", styles["Normal"]))
        else:
            # Headers
            table_data = [columns]
            
            # Rows
            for row in data:
                table_data.append([str(row.get(col, "")) for col in columns])
            
            # Column widths (auto-adjust logic simplified)
            col_widths = [None] * len(columns)
            
            t = Table(table_data, colWidths=col_widths)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")), # Blue header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke])
            ]))
            elements.append(t)
            
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_excel(self, report_data: Dict[str, Any], columns: List[str]) -> BytesIO:
        buffer = BytesIO()
        data = report_data["data"]
        
        if not data:
            df = pd.DataFrame(columns=columns)
        else:
            # Filter only selected columns
            filtered_data = [{k: v for k, v in item.items() if k in columns} for item in data]
            # Reorder columns
            df = pd.DataFrame(filtered_data)
            # Ensure all requested columns exist (even if empty)
            for col in columns:
                if col not in df.columns:
                    df[col] = ""
            df = df[columns]
            
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Reporte')
            
            # Auto-adjust column width
            worksheet = writer.sheets['Reporte']
            for idx, col in enumerate(df.columns):
                series = df[col]
                max_len = max((
                    series.astype(str).map(len).max(),
                    len(str(series.name))
                )) + 1
                worksheet.column_dimensions[chr(65 + idx)].width = max_len
                
        buffer.seek(0)
        return buffer
