# syntax=docker/dockerfile:1.3
FROM python:3.11-slim

# Argumentos de build para configuración
ARG HERMES_HOME=/app/.hermes
ARG WORKSPACE_DIR=/app/workspace
ARG SQLITE_DB_PATH=/app/.hermes/hermes_session.db
ARG HERMES_MODEL=copilot/gpt-4o
ARG HERMES_MAX_ITERATIONS=90
ARG TERMINAL_ENV=local
ARG TERMINAL_TIMEOUT=300
ARG TERMINAL_LIFETIME_SECONDS=600
ARG DASHBOARD_PORT=5000
ARG GIT_SHA=unknown

# Variables de entorno para Hermes
ENV HERMES_HOME=${HERMES_HOME}
ENV WORKSPACE_DIR=${WORKSPACE_DIR}
ENV SQLITE_DB_PATH=${SQLITE_DB_PATH}
ENV HERMES_MODEL=${HERMES_MODEL}
ENV HERMES_MAX_ITERATIONS=${HERMES_MAX_ITERATIONS}
ENV TERMINAL_ENV=${TERMINAL_ENV}
ENV TERMINAL_TIMEOUT=${TERMINAL_TIMEOUT}
ENV TERMINAL_LIFETIME_SECONDS=${TERMINAL_LIFETIME_SECONDS}
ENV DASHBOARD_PORT=${DASHBOARD_PORT}
ENV GIT_SHA=${GIT_SHA}
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    build-essential \
    sqlite3 \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libxext6 \
    libcurl4-gnutls \
    xauth \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js y npm para el TUI
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Actualizar pip primero
RUN pip install --upgrade pip setuptools wheel

# Instalar dependencias de Python con manejo mejorado
# Usar requirements-easypanel.txt si existe (versiones corregidas), sino usar requirements.txt
RUN if [ -f requirements-easypanel.txt ]; then \
    pip install --no-cache-dir -r requirements-easypanel.txt; \
    else \
    pip install --no-cache-dir -r requirements.txt; \
    fi

# Crear directorios necesarios
RUN mkdir -p $HERMES_HOME $WORKSPACE_DIR && \
    chmod -R 755 $HERMES_HOME $WORKSPACE_DIR

# Construir el TUI (React/Ink) si existe
RUN if [ -d "ui-tui" ]; then \
    cd ui-tui && \
    npm ci --prefer-offline && \
    npm run build && \
    cd ..; \
    fi

# Verificar que todo está correctamente instalado
RUN python -c "import hermes_cli; print('Hermes CLI OK')" && \
    python -m hermes_cli.main --version || echo "Hermes ready to initialize"

# Exponer puerto del Dashboard
EXPOSE ${DASHBOARD_PORT}

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import socket; socket.create_connection(('localhost', ${DASHBOARD_PORT}), timeout=5)" || exit 1

# Punto de entrada: iniciar el dashboard
ENTRYPOINT ["python", "-m", "hermes_cli.main"]
CMD ["dashboard", "--host", "0.0.0.0", "--port", "0.0.0.0:${DASHBOARD_PORT}"]
