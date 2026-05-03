#!/bin/bash
# Script para preparar Hermes para Easypanel
# Uso: bash prepare-for-easypanel.sh

set -e

echo "🚀 Preparando Hermes para Easypanel..."

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar dependencias
echo -e "${YELLOW}[1/6]${NC} Verificando dependencias..."

if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git no encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git OK${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 no encontrado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 OK${NC}"

# 2. Actualizar repositorio
echo -e "${YELLOW}[2/6]${NC} Actualizando repositorio..."
git fetch origin main
git pull origin main
echo -e "${GREEN}✓ Repositorio actualizado${NC}"

# 3. Validar requirements.txt
echo -e "${YELLOW}[3/6]${NC} Validando requirements.txt..."

# Crear un venv temporal para validación
TEMP_VENV=$(mktemp -d)
python3 -m venv "$TEMP_VENV"
source "$TEMP_VENV/bin/activate"

# Intentar instalar - si falla, es problema de requirements
if ! pip install --dry-run -r requirements.txt &>/dev/null; then
    echo -e "${YELLOW}⚠ Detectados problemas en requirements.txt${NC}"
    
    # Intentar corregir automáticamente
    echo "  Intentando corregir versiones problemáticas..."
    
    # Reemplazar versiones conflictivas
    sed -i 's/primp==1\.1\.2/primp==1.2.3/g' requirements.txt
    sed -i 's/primp==1\.1\.1/primp==1.2.3/g' requirements.txt
    sed -i 's/httpx==0\.27\.2/httpx>=0.28.0/g' requirements.txt
    
    echo -e "${GREEN}✓ requirements.txt actualizado${NC}"
else
    echo -e "${GREEN}✓ requirements.txt válido${NC}"
fi

deactivate
rm -rf "$TEMP_VENV"

# 4. Crear .dockerignore si no existe
echo -e "${YELLOW}[4/6]${NC} Configurando .dockerignore..."

if [ ! -f .dockerignore ]; then
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
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/
EOF
    echo -e "${GREEN}✓ .dockerignore creado${NC}"
else
    echo -e "${GREEN}✓ .dockerignore ya existe${NC}"
fi

# 5. Crear .env.example si no existe
echo -e "${YELLOW}[5/6]${NC} Configurando variables de entorno..."

if [ ! -f .env.example ]; then
    cat > .env.example << 'EOF'
# Hermes Configuration for Easypanel
# Copia este archivo a .env y completa los valores

# API Keys y Credenciales
GITHUB_TOKEN=tu_github_token_aqui
COPILOT_GITHUB_TOKEN=tu_copilot_token_aqui
OPENAI_API_KEY=tu_openai_key_aqui

# Hermes Configuration
HERMES_HOME=/app/.hermes
WORKSPACE_DIR=/app/workspace
HERMES_MODEL=copilot/gpt-4o
HERMES_MAX_ITERATIONS=90

# Terminal Configuration
TERMINAL_ENV=local
TERMINAL_TIMEOUT=300
TERMINAL_LIFETIME_SECONDS=600

# Dashboard
DASHBOARD_PORT=5000
DASHBOARD_PASSWORD=tu_contraseña_segura

# Gateway (Optional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_ALLOWED_USERS=
DISCORD_BOT_TOKEN=
WHATSAPP_ENABLED=false

# Ollama Integration
OLLAMA_URL=http://ollama:11434

# Build Info
GIT_SHA=auto
EOF
    echo -e "${GREEN}✓ .env.example creado${NC}"
else
    echo -e "${GREEN}✓ .env.example ya existe${NC}"
fi

# 6. Crear script de arranque para Easypanel
echo -e "${YELLOW}[6/6]${NC} Creando scripts de inicialización..."

mkdir -p docker/entrypoints

cat > docker/entrypoints/start-hermes.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Iniciando Hermes..."

# Crear directorios si no existen
mkdir -p $HERMES_HOME
mkdir -p $WORKSPACE_DIR

# Inicializar configuración si no existe
if [ ! -f "$HERMES_HOME/config.yaml" ]; then
    echo "ℹ Configuración inicial de Hermes..."
    python -m hermes_cli.main setup --quiet || true
fi

# Logging
echo "📝 Hermes está corriendo en puerto ${DASHBOARD_PORT:-5000}"
echo "🌐 Acceso: http://0.0.0.0:${DASHBOARD_PORT:-5000}"

# Iniciar el dashboard
exec python -m hermes_cli.main dashboard \
    --host 0.0.0.0 \
    --port "${DASHBOARD_PORT:-5000}" \
    "$@"
EOF

chmod +x docker/entrypoints/start-hermes.sh

echo -e "${GREEN}✓ Scripts de inicialización creados${NC}"

# Resumen final
echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Hermes listo para Easypanel${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Próximos pasos:"
echo ""
echo "1. En Easypanel, crea un nuevo servicio:"
echo "   - Selecciona este repositorio"
echo "   - Usa el Dockerfile incluido"
echo ""
echo "2. Configura las Environment Variables:"
cat .env.example | grep -v "^#" | grep "=" | sed 's/^/   /'
echo ""
echo "3. Deploy:"
echo "   - Click 'Deploy' en Easypanel"
echo "   - Espera 5-10 minutos para el build"
echo "   - Accede a: https://tu-dominio.com:5000"
echo ""
echo "📚 Para más info, lee: EASYPANEL_DEPLOYMENT.md"
echo ""
