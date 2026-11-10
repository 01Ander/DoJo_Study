# ============================================================================
# Quest 04-02 (Misión M1): Dockerfile Multi-Stage para el Worker ETL (FinCorp)
# ============================================================================
# Instrucciones: Completa las directivas del Dockerfile multi-stage siguiendo
# el contrato de Lore 04 (§2.1):
#   1. Etapa 1: `FROM python:3.12-slim AS builder` y `WORKDIR /build`
#   2. Copia `requirements.txt` e instala con `RUN pip install --no-cache-dir --prefix=/install -r requirements.txt`
#   3. Etapa 2: `FROM python:3.12-slim AS runtime` y `WORKDIR /app`
#   4. Define `ENV PYTHONDONTWRITEBYTECODE=1` y `ENV PYTHONUNBUFFERED=1`
#   5. Copia los paquetes desde builder: `COPY --from=builder /install /usr/local`
#   6. Copia el módulo `postgres_loader.py` al contenedor y define `CMD ["python", "postgres_loader.py"]`

# TODO: Escribe aquí tu Dockerfile multi-stage

# ==========================================
# ETAPA 1: Builder (Instalación y compilación)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Evita archivos .pyc y fuerza logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# ETAPA 2: Runtime (Imagen limpia de producción)
# ==========================================
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Copiamos únicamente los paquetes ya instalados desde la etapa builder
COPY --from=builder /install /usr/local

# Copiamos el código fuente del pipeline
COPY postgres_loader.py .

CMD ["python", "postgres_loader.py"]