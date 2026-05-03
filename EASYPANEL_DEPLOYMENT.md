# Guía de Deployado de Hermes en Easypanel

## Requisitos Previos

1. Easypanel instalado y corriendo
2. Docker y Docker Buildx disponibles
3. Git instalado
4. Credenciales de API keys (GitHub, OpenAI/Copilot, etc.)

## Opción 1: Deploy Automático desde Git (Recomendado)

### Paso 1: Crear un nuevo proyecto en Easypanel

```bash
# En Easypanel UI:
# 1. Navigate to Projects → Create New Service
# 2. Select "Git Repository"
# 3. Enter: https://github.com/mrm8488/hermes-agent.git
# 4. Select branch: main
```

### Paso 2: Configurar el Dockerfile

Easypanel usará automáticamente el `Dockerfile` en la raíz del repo. Si necesitas custom, reemplázalo:

```bash
# Copiar nuestro Dockerfile optimizado
cp Dockerfile Dockerfile.easypanel
```

### Paso 3: Configurar Variables de Entorno

En Easypanel UI, under "Environment Variables":

```
# API Keys y Credenciales
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
COPILOT_GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Configuración de Hermes
HERMES_HOME=/app/.hermes
WORKSPACE_DIR=/app/workspace
HERMES_MODEL=copilot/gpt-4o
HERMES_MAX_ITERATIONS=90

# Terminal
TERMINAL_ENV=local
TERMINAL_TIMEOUT=300
TERMINAL_LIFETIME_SECONDS=600

# Dashboard
DASHBOARD_PORT=5000
DASHBOARD_PASSWORD=tu_password_segura

# Gateway (si usas)
TELEGRAM_BOT_TOKEN=tu_bot_token
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_BOT_TOKEN=token_discord
WHATSAPP_ENABLED=false

# Ollama (si lo usas localmente)
OLLAMA_URL=http://ollama:11434
```

### Paso 4: Build y Deploy

```bash
# En Easypanel:
# 1. Click "Deploy"
# 2. Espera a que complete el build (~5-10 minutos)
# 3. Una vez listo, accede a: https://tu-dominio.com:5000
```

---

## Opción 2: Deploy Manual (Upload del Repo)

### Paso 1: Preparar el repositorio

```bash
# Clonar/actualizar el repo
git clone https://github.com/mrm8488/hermes-agent.git hermes-deploy
cd hermes-deploy
git pull origin main

# Limpiar archivos innecesarios
rm -rf .git tests docs .github website

# Crear archivo .dockerignore (si no existe)
cat > .dockerignore << 'EOF'
.git
.github
.gitignore
tests
docs
website
node_modules
.venv
venv
__pycache__
*.pyc
.env
.env.local
.DS_Store
.idea
.vscode
*.log
build/
dist/
*.egg-info/
EOF
```

### Paso 2: Empaquetar

```bash
tar -czf hermes-deploy.tar.gz --exclude='venv' --exclude='.git' .
```

### Paso 3: Subir a Easypanel

```bash
# En Easypanel UI:
# 1. Create New Service → Upload Codebase
# 2. Upload hermes-deploy.tar.gz
# 3. Select Dockerfile
# 4. Configure Environment Variables (ver arriba)
# 5. Deploy
```

---

## Opción 3: Docker Compose Local + Easypanel

Crear `docker-compose-easypanel.yml`:

```yaml
version: '3.8'

services:
  hermes:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        HERMES_MODEL: "copilot/gpt-4o"
        HERMES_MAX_ITERATIONS: "90"
        DASHBOARD_PORT: "5000"
    environment:
      HERMES_HOME: /app/.hermes
      WORKSPACE_DIR: /app/workspace
      GITHUB_TOKEN: ${GITHUB_TOKEN}
      COPILOT_GITHUB_TOKEN: ${COPILOT_GITHUB_TOKEN}
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      OLLAMA_URL: http://ollama:11434
    ports:
      - "5000:5000"
    volumes:
      - hermes_home:/app/.hermes
      - workspace:/app/workspace
    restart: unless-stopped
    networks:
      - hermes-network

  ollama:
    image: ollama/ollama:latest
    environment:
      OLLAMA_HOST: 0.0.0.0:11434
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - hermes-network
    restart: unless-stopped

volumes:
  hermes_home:
  workspace:
  ollama_data:

networks:
  hermes-network:
    driver: bridge
```

---

## Verificación Post-Deploy

### 1. Verificar que Hermes está corriendo

```bash
curl http://localhost:5000/health
# Debería devolver 200 OK
```

### 2. Acceder al Dashboard

Abre tu navegador:
```
http://tu-dominio-easypanel.com:5000
```

### 3. Verificar logs

En Easypanel UI:
```
Services → Hermes → Logs
```

O vía SSH:
```bash
docker logs hermes-container-id
```

### 4. Verificar que todas las herramientas están disponibles

```bash
# Dentro del contenedor
docker exec hermes-container-id python -m hermes_cli.main --version
docker exec hermes-container-id python -m hermes_cli.main tools list
```

---

## Troubleshooting

### Error: "primp==1.1.2 not found"

**Solución:** Actualiza el repo a la versión más reciente:
```bash
git pull origin main
```

El Dockerfile está optimizado para manejar incompatibilidades automáticamente.

### Error: "Could not read Username for GitHub"

**Solución:** En Easypanel, añade `--network host` al build:

En Easypanel Advanced Build Options:
```
Docker Build Args:
--network=host
```

### Error: Npm build falla en ui-tui

**Solución:** Aumenta memoria disponible:

En Easypanel Service Settings → Resources:
```
Memory Limit: 2GB
CPUs: 2
```

### Node modules gigantes ralentizan el build

**Solución:** Usa caché Docker:

En Easypanel → Advanced:
```
Use Docker Build Cache: YES
```

### No puedo acceder al Dashboard en http://localhost:5000

**Solución:**

1. Verifica que el contenedor está corriendo:
```bash
docker ps | grep hermes
```

2. Verifica los logs:
```bash
docker logs <container-id>
```

3. Prueba conectar al puerto dentro del contenedor:
```bash
docker exec <container-id> curl http://localhost:5000
```

---

## Configuración Avanzada

### Persistencia de Datos

Las siguientes rutas se persisten automáticamente en volumes:

```
HERMES_HOME=/app/.hermes          # Config, keys, sessions
WORKSPACE_DIR=/app/workspace      # Workspace temporal
```

En Easypanel, se usan Docker volumes automáticamente.

### Usar modelo local con Ollama

Asegúrate de que `OLLAMA_URL` esté configurado:

```
OLLAMA_URL=http://ollama:11434
```

Luego en Hermes:
```bash
hermes provider set ollama
hermes model set <model-name>
```

### Integración Gateway (Telegram, Discord, etc.)

Añade los tokens correspondientes en Environment Variables:

```
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjklmNOpqrsTUVwxyz
DISCORD_BOT_TOKEN=token_aqui
WHATSAPP_ENABLED=true
```

### Ejecutar Skills Personalizadas

Monta tu directorio de skills:

```yaml
volumes:
  - /ruta/local/skills:/app/.hermes/skills
```

---

## Performance Tuning

### Para mejor velocidad del Dashboard

```
HERMES_MAX_ITERATIONS=60    # Reducir si es lento
TERMINAL_TIMEOUT=300         # Aumentar si los scripts tardan
```

### Para usar más modelos simultáneamente

En Easypanel:
```
Memory Limit: 4GB
CPUs: 4
```

### Build rápido sin TUI (CLI only)

Modifica el Dockerfile:
```dockerfile
# Comentar esta línea:
# RUN if [ -d "ui-tui" ]; then cd ui-tui && npm ci && npm run build; fi
```

---

## Actualizar Hermes

Cuando haya nuevas versiones:

```bash
# En tu repo local
git pull origin main

# Push a Easypanel (si usas auto-deploy)
git push

# O re-deploy manualmente en Easypanel UI
```

---

## Seguridad

### Cambiar contraseña del Dashboard

```bash
hermes dashboard --password nueva_password_segura
```

O en env variables:
```
DASHBOARD_PASSWORD=nueva_password_segura_minimo_12_caracteres
```

### Proteger API keys

**NUNCA** commits los `.env` con credenciales. En Easypanel:

1. Usa Secrets, no Environment Variables plain text
2. Activa HTTPS/SSL
3. Usa firewall rules para limitar acceso

---

## Soporte

Para issues específicos de Hermes:
- GitHub: https://github.com/anomalyco/opencode
- Docs: https://opencode.ai/docs

Para issues de Easypanel:
- Docs: https://www.easypanel.io/docs
