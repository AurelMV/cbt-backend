# Guía de Despliegue y Seguridad

## 1. Inicialización de Base de Datos

Una vez que los contenedores estén corriendo (`docker-compose up -d`), debes inicializar la base de datos y crear los usuarios por defecto.

Ejecuta los siguientes comandos:

```bash
# 1. Aplicar migraciones (crea tablas y roles 'admin'/'user')
docker-compose exec backend uv run alembic upgrade head

# 2. Poblar datos iniciales (crea usuarios 'admin' y 'user')
docker-compose exec backend uv run python scripts/seed_initial_data.py
```

### Usuarios Creados

- **Admin**: `admin` / `123456`
- **User**: `user` / `123456`

---

## 2. Seguridad en Producción

Cuando despliegues esta aplicación en un entorno real (AWS, DigitalOcean, VPS, etc.), **NUNCA** uses los valores por defecto.

### Pasos Críticos:

1.  **Variables de Entorno (.env)**:

    - No subas el archivo `.env` al repositorio (git).
    - En el servidor, crea un archivo `.env` con valores seguros.

2.  **Generar Secretos Seguros**:

    - `SECRET_KEY`: Genera una cadena aleatoria larga.
      ```bash
      openssl rand -hex 32
      ```
    - `POSTGRES_PASSWORD`: Usa una contraseña fuerte para la base de datos.

3.  **Configuración de Docker Compose (Producción)**:

    - No uses `docker-compose.yml` de desarrollo si expone puertos innecesarios.
    - Asegúrate de que `DB_ECHO=False`.

4.  **HTTPS / SSL**:

    - No expongas el puerto 8000 directamente a internet.
    - Usa un proxy inverso como **Nginx** o **Traefik** para manejar SSL (https) y redirigir al contenedor.

5.  **Base de Datos**:
    - En producción, es preferible usar un servicio gestionado (AWS RDS, Google Cloud SQL) en lugar de un contenedor de BD, para facilitar backups y escalabilidad.
    - Si usas contenedor, asegura que el volumen `postgres_data` tenga backups periódicos.
