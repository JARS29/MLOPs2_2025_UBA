# Usa una imagen base de Python oficial
FROM python:3.11-slim-bookworm

# Trae el binario de uv desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de configuracion del proyecto
COPY pyproject.toml uv.lock* ./

# Instala las dependencias (sin instalar el propio proyecto)
RUN uv sync --no-dev --no-install-project

# Copia el codigo de tu aplicacion
COPY app.py ./

# Expone el puerto que usara Uvicorn
EXPOSE 8000

# uv run asegura que uvicorn se ejecute dentro del entorno gestionado por uv
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
