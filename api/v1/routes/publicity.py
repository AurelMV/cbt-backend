from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
import shutil
import os
from pathlib import Path

router = APIRouter(prefix="/publicity", tags=["publicity"])

UPLOAD_DIR = Path("static/publicity")
BANNER_FILENAME = "banner.jpg"
BANNER_PATH = UPLOAD_DIR / BANNER_FILENAME

@router.get("/")
async def get_publicity():
    """
    Retorna la URL de la imagen publicitaria si existe, o null si no hay.
    """
    if BANNER_PATH.exists():
        # Retornamos la ruta relativa para que el frontend la construya con la BASE_URL
        # Ojo: FastAPI StaticFiles se monta usualmente en /static
        return {"imageUrl": f"/static/publicity/{BANNER_FILENAME}?t={os.path.getmtime(BANNER_PATH)}"}
    return {"imageUrl": None}

@router.post("/")
async def upload_publicity(file: UploadFile = File(...)):
    """
    Sube una nueva imagen publicitaria, reemplazando la anterior.
    """
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(BANNER_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"message": "Publicidad actualizada correctamente", "imageUrl": f"/static/publicity/{BANNER_FILENAME}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

@router.delete("/")
async def delete_publicity():
    """
    Elimina la imagen publicitaria actual.
    """
    if BANNER_PATH.exists():
        os.remove(BANNER_PATH)
        return {"message": "Publicidad eliminada"}
    return {"message": "No hay publicidad para eliminar"}
