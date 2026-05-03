FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para construir y ejecutar herramientas de desarrollo
RUN apt-get update && apt-get install -y \
    git \
    curl \
    nodejs \
    npm \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Configurar el entorno de Hermes para persistencia y workspace
ENV HERMES_HOME=/app/.hermes
ENV WORKSPACE_DIR=/app/workspace
RUN mkdir -p $HERMES_HOME $WORKSPACE_DIR

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias adicionales para el Dashboard/TUI (Ink/React)
RUN if [ -d "ui-tui" ]; then cd ui-tui && npm install && npm run build; fi

# Exponer el puerto del Dashboard Profesional
EXPOSE 5000

# Comando por defecto: Arrancar el Dashboard en modo escucha global
# Esto permite acceder al Chat, Code Agent y Gateway desde la web
CMD ["python", "-m", "hermes_cli.main", "dashboard", "--host", "0.0.0.0", "--port", "5000"]
