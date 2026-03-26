# Usa una imagen base de Python oficial
FROM python:3.11-slim-bookworm

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala Poetry
RUN pip install poetry

# Copia los archivos de configuración de Poetry
COPY pyproject.toml poetry.lock* ./

# Instala las dependencias de producción usando Poetry
RUN poetry install --no-root --no-interaction

# Copia el código de tu aplicación
COPY app.py ./

# Expone el puerto que usará Uvicorn
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
# 'poetry run' asegura que uvicorn se ejecute dentro del entorno virtuala gestionado por Poetry
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
