import base64
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_preinscripcion_pdf(data: dict, voucher_base64: str | None = None) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor("#1a365d")
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#2d3748")
    )
    normal_style = styles["Normal"]
    normal_style.fontSize = 10
    
    elements = []

    # --- Encabezado ---
    # Si tuvieras un logo, lo pondrías aquí:
    # elements.append(Image("path/to/logo.png", width=4*cm, height=2*cm))
    
    elements.append(Paragraph("CONSTANCIA DE PREINSCRIPCIÓN", title_style))
    elements.append(Paragraph(f"Programa: {data.get('programa', '')}", subtitle_style))
    
    elements.append(Paragraph(f"<b>Fecha de registro:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Paragraph(f"<b>Código de referencia:</b> PRE-{data.get('id', '?')}", normal_style))
    elements.append(Spacer(1, 0.5*cm))

    # --- Datos del Estudiante ---
    elements.append(Paragraph("Datos del Estudiante", styles['Heading3']))
    
    student_data = [
        ["Nombre Completo:", f"{data.get('nombre', '')} {data.get('paterno', '')} {data.get('materno', '')}"],
        ["DNI:", data.get('dni', '')],
        ["Email:", data.get('email', '')],
        ["Teléfono:", data.get('telefono', '')],
        ["Colegio:", data.get('colegio', '')],
        ["Ubicación:", f"{data.get('departamento', '')} - {data.get('provincia', '')} - {data.get('distrito', '')}"],
    ]
    
    t_student = Table(student_data, colWidths=[4*cm, 11*cm])
    t_student.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor("#4a5568")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f7fafc")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_student)
    elements.append(Spacer(1, 1*cm))

    # --- Datos del Pago ---
    elements.append(Paragraph("Detalles del Pago", styles['Heading3']))
    
    payment_data = [
        ["Nro. Voucher:", data.get('voucher_code', '')],
        ["Monto:", f"S/ {data.get('monto', '0.00')}"],
        ["Fecha Pago:", data.get('fecha_pago', '')],
        ["Medio de Pago:", data.get('medio_pago', '').upper()],
    ]
    
    t_payment = Table(payment_data, colWidths=[4*cm, 11*cm])
    t_payment.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor("#4a5568")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f7fafc")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_payment)
    elements.append(Spacer(1, 1*cm))

    # --- Imagen del Voucher ---
    if voucher_base64:
        elements.append(Paragraph("Comprobante Adjunto:", styles['Heading3']))
        elements.append(Spacer(1, 0.5*cm))
        
        try:
            # Limpiar cabecera data:image/...;base64, si existe
            if "," in voucher_base64:
                header, encoded = voucher_base64.split(",", 1)
            else:
                encoded = voucher_base64
            
            img_data = base64.b64decode(encoded)
            img_io = io.BytesIO(img_data)
            
            # Crear imagen de ReportLab
            # Ajustar tamaño manteniendo relación de aspecto
            # Ancho máximo disponible: A4 width (21cm) - margins (4cm) = 17cm
            max_width = 16 * cm
            max_height = 12 * cm
            
            img = Image(img_io)
            
            # Calcular escala
            img_width = img.drawWidth
            img_height = img.drawHeight
            
            ratio = min(max_width/img_width, max_height/img_height)
            
            img.drawWidth = img_width * ratio
            img.drawHeight = img_height * ratio
            
            elements.append(img)
            
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar la imagen del voucher: {str(e)}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def generate_pago_pdf(data: dict, voucher_base64: str | None = None) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor("#1a365d")
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#2d3748")
    )
    normal_style = styles["Normal"]
    normal_style.fontSize = 10
    
    elements = []

    elements.append(Paragraph("CONSTANCIA DE PAGO", title_style))
    elements.append(Paragraph(f"Programa: {data.get('programa', '')}", subtitle_style))
    
    elements.append(Paragraph(f"<b>Fecha de emisión:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    elements.append(Paragraph(f"<b>Código de Pago:</b> PAY-{data.get('id', '?')}", normal_style))
    elements.append(Spacer(1, 0.5*cm))

    # --- Datos del Estudiante ---
    elements.append(Paragraph("Datos del Estudiante", styles['Heading3']))
    
    student_data = [
        ["Nombre Completo:", f"{data.get('nombre', '')} {data.get('paterno', '')} {data.get('materno', '')}"],
        ["DNI:", data.get('dni', '')],
        ["Ciclo:", data.get('ciclo', '')],
        ["Código Inscripción:", data.get('codigo_inscripcion', '')],
    ]
    
    t_student = Table(student_data, colWidths=[4*cm, 11*cm])
    t_student.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor("#4a5568")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f7fafc")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_student)
    elements.append(Spacer(1, 1*cm))

    # --- Datos del Pago ---
    elements.append(Paragraph("Detalles del Pago", styles['Heading3']))
    
    payment_data = [
        ["Nro. Voucher:", data.get('voucher_code', '')],
        ["Monto:", f"S/ {data.get('monto', '0.00')}"],
        ["Fecha Pago:", data.get('fecha_pago', '')],
        ["Medio de Pago:", data.get('medio_pago', '').upper()],
        ["Estado:", data.get('estado', '').upper()],
    ]
    
    t_payment = Table(payment_data, colWidths=[4*cm, 11*cm])
    t_payment.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor("#4a5568")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#f7fafc")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_payment)
    elements.append(Spacer(1, 1*cm))

    # --- Imagen del Voucher ---
    if voucher_base64:
        elements.append(Paragraph("Comprobante Adjunto:", styles['Heading3']))
        elements.append(Spacer(1, 0.5*cm))
        
        try:
            if "," in voucher_base64:
                header, encoded = voucher_base64.split(",", 1)
            else:
                encoded = voucher_base64
            
            img_data = base64.b64decode(encoded)
            img_io = io.BytesIO(img_data)
            
            max_width = 16 * cm
            max_height = 12 * cm
            
            img = Image(img_io)
            img_width = img.drawWidth
            img_height = img.drawHeight
            
            ratio = min(max_width/img_width, max_height/img_height)
            
            img.drawWidth = img_width * ratio
            img.drawHeight = img_height * ratio
            
            elements.append(img)
            
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar la imagen del voucher: {str(e)}", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
