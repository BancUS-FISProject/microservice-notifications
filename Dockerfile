FROM python:3.12-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Carpeta de trabajo
WORKDIR /app

# Variables de entorno para Mongo (rellenadas desde docker-compose)
ARG MONGO_CONNECTION_STRING
ARG MONGO_DATABASE_NAME

ENV MONGO_CONNECTION_STRING=$MONGO_CONNECTION_STRING \
    MONGO_DATABASE_NAME=$MONGO_DATABASE_NAME

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src ./src

# Crear usuario no root
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Comando para arrancar la app
CMD ["uvicorn", "src.notifications.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
