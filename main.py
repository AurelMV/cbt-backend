from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.staticfiles import StaticFiles
from api.v1.routes import (
    auth,
    users,
    ciclos,
    grupos,
    clases,
    departamentos,
    provincias,
    distritos,
    colegios,
    programas,
    preinscripciones,
    prepagos,
    alumnos,
    inscripciones,
    pagos,
    bandeja,
    reports,
    dashboard,
    publicity,
)
from db.base import init_db
from core.config import settings

app = FastAPI(title="CBT Backend API", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar ProxyHeadersMiddleware para manejar HTTPS detrás de un proxy (Railway)
# Esto asegura que los redirects (ej. trailing slash) usen el esquema correcto (https)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])

# CORS configuration

# Permitir todos los orígenes por defecto si no se configuró CORS_ORIGINS en .env
_allow_origins = settings.CORS_ORIGINS or ["*"]
# La combinación "*" + credentials=True no es válida según el estándar; si se usa "*", forzamos credentials=False
_allow_credentials = settings.CORS_ALLOW_CREDENTIALS and _allow_origins != ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_credentials=_allow_credentials,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
def on_startup():
    # Ensure tables exist for newly added models in dev environments
    init_db()


api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(ciclos.router)
api_router.include_router(grupos.router)
api_router.include_router(clases.router)
api_router.include_router(departamentos.router)
api_router.include_router(provincias.router)
api_router.include_router(distritos.router)
api_router.include_router(colegios.router)
api_router.include_router(programas.router)
api_router.include_router(preinscripciones.router)
api_router.include_router(prepagos.router)
api_router.include_router(alumnos.router)
api_router.include_router(inscripciones.router)
api_router.include_router(pagos.router)
api_router.include_router(bandeja.router)
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(publicity.router)

app.include_router(api_router)

app.include_router(api_router)
