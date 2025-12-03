# Recomendaciones para Despliegue en Railway

Tu proyecto está listo para Railway. Aquí tienes algunas recomendaciones finales para asegurar un despliegue exitoso y sin problemas.

## 1. Configuración de Puerto (Crítico)

Railway asigna dinámicamente un puerto a tu aplicación a través de la variable de entorno `PORT`.

- **He actualizado tu `entrypoint.sh`** para que use automáticamente este puerto (`$PORT`) si está disponible, o `8000` por defecto.
- No necesitas configurar nada extra en Railway para esto.

## 2. Variables de Entorno en Railway

Cuando crees el proyecto en Railway, ve a la pestaña **Variables** y asegúrate de agregar:

| Variable                      | Valor Recomendado                                                                                    |
| ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| `SECRET_KEY`                  | Una cadena larga y aleatoria (ej. generada con `openssl rand -hex 32`)                               |
| `ALGORITHM`                   | `HS256`                                                                                              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` (24 horas) o lo que prefieras                                                                 |
| `CORS_ORIGINS`                | `["https://tu-frontend.vercel.app", "https://tu-dominio.com"]` (La URL de tu frontend en producción) |
| `CORS_ALLOW_CREDENTIALS`      | `True`                                                                                               |
| `DB_ECHO`                     | `False`                                                                                              |

**Nota sobre la Base de Datos:**
Si agregas un servicio de PostgreSQL dentro de tu proyecto en Railway, la variable `DATABASE_URL` se inyectará automáticamente. No necesitas agregarla manualmente.

## 3. Almacenamiento de Archivos (Fotos/Vouchers)

He notado que el modelo `Pago` tiene un campo `foto`.

- Si estás guardando las fotos como **Base64** (texto) en la base de datos: **Todo funcionará bien**.
- Si planeas guardar archivos en el disco del servidor (`/app/uploads/...`): **Se perderán** cada vez que despliegues una nueva versión, ya que el sistema de archivos de Railway es efímero.
  - **Solución:** Usa un servicio externo como AWS S3, Cloudinary o Firebase Storage para guardar archivos y guarda solo la URL en la base de datos.

## 4. Health Check

Railway intentará verificar si tu app está viva.

- Si te pide una ruta de Health Check, usa: `/docs` o `/api/` (si tienes una ruta raíz).
- Si no tienes ruta raíz, Railway suele detectar el puerto abierto automáticamente.

## 5. Tiempos de Espera (Timeouts)

El plan gratuito/hobby de Railway tiene límites de uso. Si tus reportes PDF son muy pesados o tardan mucho en generarse, podrías tener timeouts.

- Para este proyecto, la generación de PDFs parece ligera, así que no debería ser problema.

## 6. Despliegue

1. Sube todo a GitHub.
2. En Railway: `New Project` -> `Deploy from GitHub repo`.
3. Agrega el servicio de PostgreSQL.
4. Configura las variables.
5. ¡Listo! El `entrypoint.sh` se encargará de las migraciones y el usuario admin.
