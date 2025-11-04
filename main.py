from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
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
)
from db.base import init_db
from core.config import Config

app = FastAPI(title="CBT Backend API", version="1.0.0")

# CORS configuration
settings = Config()
allowed_origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
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

app.include_router(api_router)
