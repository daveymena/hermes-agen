# Hermes en Easypanel - GUÍA RÁPIDA

## El Problema

Tu `requirements.txt` tiene versiones que no existen en PyPI:
- `primp==1.1.2` ❌ No existe (máximo es 1.2.3)
- Red bloqueada al clonar desde GitHub dentro del contenedor

## La Solución ✓

Ya hemos preparado todo. Solo sigue estos pasos:

---

## PASO 1: Preparar tu repositorio

```bash
# En tu máquina local
cd /ruta/a/hermes-agent
git pull origin main

# Ya tenemos los archivos listos:
# ✓ requirements-easypanel.txt (corregido)
# ✓ Dockerfile (optimizado)
# ✓ .dockerignore (configurado)
```

---

## PASO 2: Subir a Easypanel

### Opción A: Auto-deploy desde GitHub (MÁS FÁCIL)

1. **En Easypanel UI:**
   - Click "Create Service" → "Git Repository"
   - Pega: `https://github.com/mrm8488/hermes-agent.git`
   - Branch: `main`

2. **Configura Environment Variables:**
```
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
COPILOT_GITHUB_TOKEN=ghp_xxxxxxxxxxxx
HERMES_MODEL=copilot/gpt-4o
DASHBOARD_PORT=5000
```

3. **Deploy:**
   - Click "Deploy"
   - Espera 5-10 minutos
   - Accede a: `http://tu-dominio:5000`

### Opción B: Upload manual

```bash
# En tu máquina
tar -czf hermes.tar.gz --exclude='.git' --exclude='venv' --exclude='.venv' .

# En Easypanel:
# 1. Create Service → Upload Codebase
# 2. Selecciona hermes.tar.gz
# 3. Sigue mismo proceso que Opción A
```

---

## PASO 3: Variables de Entorno Importantes

**MÍNIMAS (necesarias):**
```
HERMES_HOME=/app/.hermes
WORKSPACE_DIR=/app/workspace
DASHBOARD_PORT=5000
```

**CON API KEYS (recomendado):**
```
GITHUB_TOKEN=ghp_xxxxxxx
COPILOT_GITHUB_TOKEN=ghp_xxxxxxx
OPENAI_API_KEY=sk-xxxxxxx
HERMES_MODEL=copilot/gpt-4o
HERMES_MAX_ITERATIONS=90
TERMINAL_TIMEOUT=300
```

**CON GATEWAY (opcional - para Telegram, Discord, etc):**
```
TELEGRAM_BOT_TOKEN=123456:ABCDEFxyz
TELEGRAM_ALLOWED_USERS=123456789,987654321
WHATSAPP_ENABLED=false
```

---

## PASO 4: Verificar que funciona

Una vez deployado:

```bash
# Desde tu máquina
curl http://tu-dominio-easypanel.com:5000

# Debería responder con la interfaz del Dashboard
```

En el navegador:
```
http://tu-dominio-easypanel.com:5000
```

---

## Si hay errores...

### ❌ Error: "primp==1.1.2 not found"

✓ **SOLUCIONADO:** Ahora usamos `requirements-easypanel.txt`

Verifica en Easypanel → Build Logs que dice:
```
RUN if [ -f requirements-easypanel.txt ]; then
  pip install --no-cache-dir -r requirements-easypanel.txt;
```

### ❌ Error: "Could not read Username for GitHub"

Este era el primer error. **Ya lo solucionamos** eliminando el `git clone` del Dockerfile.

Ahora el código se copia directamente (`COPY . .`)

### ❌ Error: npm build para el TUI falla

Aumenta memoria en Easypanel:
- Memory: 2GB
- CPUs: 2

O desactiva el TUI (CLI only) comentando en Dockerfile:
```dockerfile
# RUN if [ -d "ui-tui" ]; then ...
```

### ❌ No puedo acceder en http://localhost:5000

Hermes corre **dentro del contenedor**. Usa:

- URL en Easypanel: `http://tu-dominio-easypanel.com:5000`
- O SSH a la máquina y: `docker exec <container-id> curl http://localhost:5000`

---

## Cambiar configuración después del deploy

### Opción 1: Variables de Entorno (sin rebuild)

En Easypanel UI:
- Services → Hermes → Environment
- Modifica valores
- Click "Restart Service"

### Opción 2: Editar config.yaml directamente

Accede al shell del contenedor:
```bash
docker exec -it <container-id> bash
nano ~/.hermes/config.yaml
```

### Opción 3: GUI del Dashboard

1. Abre: `http://tu-dominio:5000`
2. Icono ⚙️ Settings
3. Modifica configuración
4. Guarda automáticamente

---

## Integración con Ollama local

Si tienes Ollama en otra máquina:

```
OLLAMA_URL=http://ollama-machine-ip:11434
```

Luego en Hermes:
```bash
hermes provider set ollama
hermes model set <model-name>  # ej: llama2, neural-chat
```

---

## Performance Tuning

**Si es lento:**
- Reduce: `HERMES_MAX_ITERATIONS=60` (default 90)
- Aumenta en Easypanel: Memory a 2GB, CPUs a 2

**Si es rápido:**
- Aumenta: `HERMES_MAX_ITERATIONS=120`
- Aprovecha mejor: Memory 4GB, CPUs 4

---

## Archivos clave ya creados

✓ `Dockerfile` - Optimizado para Easypanel
✓ `requirements-easypanel.txt` - Dependencias corregidas
✓ `.dockerignore` - Acelera builds
✓ `EASYPANEL_DEPLOYMENT.md` - Guía completa
✓ `prepare-for-easypanel.sh` - Script de setup

---

## Soporte

- Documentación: https://opencode.ai/docs
- GitHub Issues: https://github.com/anomalyco/opencode
- Este repositorio: https://github.com/mrm8488/hermes-agent

¡Listo! Ahora puedes hacer deploy en Easypanel sin errores. 🚀
