#!/bin/sh

# Ejecutar migraciones
echo "Ejecutando migraciones..."
uv run alembic upgrade head

# Crear datos iniciales (opcional, seguro de correr múltiples veces si el script lo controla)
echo "Verificando datos iniciales..."
uv run python scripts/seed_initial_data.py

# Iniciar la aplicación
echo "Iniciando servidor..."
# Usar la variable PORT si existe (Railway la provee), sino 8000
PORT="${PORT:-8000}"
exec uv run fastapi run main.py --port "$PORT" --host 0.0.0.0
