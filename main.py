from fastapi import FastAPI
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

app = FastAPI(title="CBT Backend API", version="1.0.0")


@app.on_event("startup")
def on_startup():
	# Ensure tables exist for newly added models in dev environments
	init_db()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ciclos.router)
app.include_router(grupos.router)
app.include_router(clases.router)
app.include_router(departamentos.router)
app.include_router(provincias.router)
app.include_router(distritos.router)
app.include_router(colegios.router)
app.include_router(programas.router)
app.include_router(preinscripciones.router)
app.include_router(prepagos.router)
app.include_router(alumnos.router)
app.include_router(inscripciones.router)
app.include_router(pagos.router)
