# Etapa base 
FROM python:3.13-bookworm AS builder

ENV APP_HOME=/usr/src/app
WORKDIR $APP_HOME

# Instala dependencias del sistema y actualiza pip
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip

# Copia primero el archivo de requerimientos para instalar dependencias
COPY requirements.txt requirements.txt

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Etapa final: contenedor más ligero
FROM python:3.13-slim AS runtime

ENV APP_HOME=/app
WORKDIR $APP_HOME

# Copia el código fuente
COPY . .

# Copia toda la instalación de Python (no solo site-packages)
COPY --from=builder /usr/local /usr/local

# Expone el puerto requerido por Cloud Run
EXPOSE 8080

# Comando para iniciar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
