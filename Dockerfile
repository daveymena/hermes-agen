FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para construir y ejecutar herramientas
RUN apt-get update && apt-get install -y \
    git \
    curl \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Configurar el entorno de Hermes para persistencia
ENV HERMES_HOME=/app/.hermes
RUN mkdir -p $HERMES_HOME

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias del Dashboard/TUI (si existen)
RUN if [ -f "package.json" ]; then npm install; fi

# Exponer puertos del Dashboard y API
EXPOSE 5000 8000

# Por defecto, arrancar el Gateway para WhatsApp
# Pero Easypanel permite sobreescribir esto con "python -m hermes_cli.main --tui"
CMD ["python", "-m", "hermes_cli.main", "gateway", "run"]
