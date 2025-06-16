# Etapa base 
FROM python:3.13-bookworm AS builder

# Define el directorio base del proyecto
ENV APP_HOME=/usr/src/app
WORKDIR $APP_HOME

# Instala dependencias del sistema y actualiza pip
RUN apt-get update && apt-get install -y gcc && \
    pip install --upgrade pip

# Copia primero el archivo de requerimientos para instalar dependencias
COPY requirements.txt requirements.txt

# Instala las dependencias del proyecto en una carpeta temporal
RUN pip install --no-cache-dir -r requirements.txt

# Segunda etapa: contenedor final más ligero
FROM python:3.13-slim AS runtime

ENV APP_HOME=/app
WORKDIR $APP_HOME

# Copia los archivos del proyecto
COPY . .

# Copia las dependencias ya instaladas desde la etapa anterior
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Expone el puerto por defecto de FastAPI
EXPOSE 8080

# Shell form para facilitar sobreescritura en producción
# Comando por defecto para correr FastAPI con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
