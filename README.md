# API de Backend CBT

Backend en FastAPI + SQLModel con autenticación JWT y control de acceso por roles. Pensado para un centro de estudios (alumnos, docentes, cursos) y preparado para escalar el dominio.

## Stack

- FastAPI (con Swagger UI)
- SQLModel (SQLAlchemy + Pydantic)
- JWT (PyJWT) + hashing Argon2 (pwdlib)
- Alembic para migraciones

## Estructura del proyecto

```
cbt-backend/
	alembic/                  # migraciones (env.py lee DATABASE_URL desde .env)
	api/
		deps.py                 # dependencias de auth y chequeos de rol
		v1/
			routes/
				auth.py             # /auth/register, /auth/login
				users.py            # endpoints /users
	core/
		config.py               # settings con pydantic-settings (.env)
		security.py             # hashing y creación/validación de JWT
	db/
		base.py                 # engine, Session, init_db
		models/
			user.py               # User, Role, UserRole
		repositories/
			role_repository.py
			user_repository.py
	schemas/
		user.py                 # Esquemas Pydantic (UserCreate, UserRead, Token)
	services/
		auth_service.py         # lógica de registro/login usando repositorios
	scripts/
		seed_initial_data.py    # seed opcional de usuarios (requiere roles creados)
	main.py                   # app FastAPI e include_routers
	pyproject.toml            # dependencias
	.env.example              # variables de entorno de ejemplo
```

## Requisitos

- Windows PowerShell (los comandos usan esta shell)
- Python 3.13+

Opcional:

- uv (gestor de paquetes rápido) o usar venv + pip

## Puesta en marcha (Setup)

1. Crear entorno virtual e instalar dependencias

Con uv (recomendado):

```powershell
uv sync
```

Con venv + pip:

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -e .
```

2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example`) con al menos:

```
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./cbt-test.db
```

3. Aplicar migraciones (Incluye creación de tablas y roles base)

Alembic está configurado para leer `DATABASE_URL` desde `.env` a través de `core.config.Config`.

```powershell
alembic upgrade head
```

4. (Opcional) Seed de usuarios iniciales

El script siguiente crea un `admin` y un `user` si no existen (requiere que los roles ya existan):

```powershell
uv run scripts/seed_initial_data.py
```

5. Ejecutar la API

```powershell
fastapi dev main.py
```

Abre Swagger UI en:

```
http://127.0.0.1:8000/docs
```

## Uso de autenticación

- Registro: `POST /auth/register`

  - Body de ejemplo:
    ```json
    {
      "username": "alice",
      "password": "secret123",
      "email": "alice@example.com"
    }
    ```
  - Requiere que exista el rol `user`; si no existe, la API devuelve 500 indicando que primero se deben crear/sembrar los roles.

- Login: `POST /auth/login`

  - Usa OAuth2 password flow (form-data).
  - El campo “username” acepta tu nombre de usuario o tu email, más la contraseña.
  - En éxito devuelve `{ "access_token": "...", "token_type": "bearer" }`.

- Autorizar en Swagger:

  - Clic en “Authorize”, completa “username” con tu username o email, y “password”. Deja el resto en blanco.

- Endpoints protegidos:
  - `GET /users/me` requiere rol `user`.
  - `GET /users/` requiere rol `admin`.
  - Los roles se validan contra la base de datos en cada request (no solo desde el token), así que los cambios de permisos aplican de inmediato.

## Solución de problemas (Troubleshooting)

- ModuleNotFoundError: No module named 'db' al ejecutar un script

  - Ejecuta el script como módulo: `./.venv/Scripts/python.exe -m scripts.seed_initial_data`
  - O asegúrate de que el script ajuste `sys.path` (ya se maneja en `scripts/seed_initial_data.py`).

- 422 en /auth/login usando Swagger

  - Usa el botón “Authorize” (OAuth2 password flow) o envía form-data a `/auth/login`.

- Rol por defecto 'user' no encontrado al registrar

  - Crea/siembra los roles primero (ver “Aplicar migraciones”).

- no such table: ...
  - Ejecuta `alembic upgrade head` para aplicar migraciones.

## Notas de desarrollo

- Capa de repositorios: `db/repositories/*` encapsula acceso a DB.
- Capa de servicios: `services/auth_service.py` centraliza la lógica de registro/login.
- Capa de API: `api/v1/routes/*` son controladores delgados que delegan en servicios.
- Configuración: `core/config.py` (pydantic-settings) lee `.env` y está integrado con Alembic.

## Próximos pasos (sugeridos)

- Añadir paginación (limit/offset) y orden a `/users`.
- Agregar refresh tokens si se necesitan, y flujos de recuperación de contraseña.
- Ampliar dominio: students, teachers, courses, enrollments con sus repos/servicios/rutas.

---

## Datos demo: inscripciones y pagos

Para poblar rápidamente datos de prueba en las tablas `inscripcion` y `pago`, puedes usar el script:

- `scripts/seed_inscripciones_pagos.py`: inserta 50 inscripciones y 50 pagos asociados. El script crea, si faltan, los datos base requeridos: ubicación (DEP/PROV/DIST/Colegio demo), un Programa de Estudios, un Ciclo con su Grupo y Clase, y 50 alumnos.

Ejecución desde PowerShell (Windows):

```powershell
./.venv/Scripts/python.exe -m scripts.seed_inscripciones_pagos
```

El script imprime un resumen como:

```
Seeding completado: {"inscripciones_creadas": 50, "pagos_creados": 50, "inscripciones_demo_totales": 50, "pagos_demo_totales": 50}
```

Notas:
- No borra datos existentes; añade registros con prefijos `INS-DEMO-` y `VCH-DEMO-` para poder identificarlos fácilmente.
- Si necesitas una cantidad distinta, puedes editar la llamada en el `if __name__ == "__main__":` del script y ajustar el número.

¡Feliz desarrollo! Si algo no queda claro en este README, abre un issue o avisa al equipo para mejorarlo.
