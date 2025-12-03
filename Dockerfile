FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (if needed for psycopg2 or others)
# libpq-dev is often needed for building psycopg2, but psycopg2-binary usually avoids this.
# We'll keep it simple for now.

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . .

# Install the project itself
RUN uv sync --frozen

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["./entrypoint.sh"]
