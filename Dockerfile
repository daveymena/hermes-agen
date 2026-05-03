FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Crear carpeta para la base de datos de Hermes
RUN mkdir -p /root/.hermes

# Exponer el puerto por si usamos el Dashboard (opcional)
EXPOSE 8000

# Comando para arrancar el bot de WhatsApp por defecto
# Se recomienda usar variables de entorno en Easypanel para el TOKEN
CMD ["python", "-m", "hermes_cli.main", "whatsapp"]
