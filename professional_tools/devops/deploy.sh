
#!/bin/bash
# RAULI Deployment Script

echo "🚀 Iniciando despliegue de RAULI Professional Suite..."

# Variables
PROJECT_DIR="/opt/rauli"
BACKUP_DIR="/opt/rauli/backups"
LOG_FILE="/var/log/rauli-deploy.log"

# Crear directorios
mkdir -p $PROJECT_DIR
mkdir -p $BACKUP_DIR
mkdir -p $(dirname $LOG_FILE)

# Backup actual
if [ -d "$PROJECT_DIR" ]; then
    echo "📦 Creando backup..."
    tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).tar.gz" -C "$PROJECT_DIR" .
fi

# Actualizar código
echo "📥 Descargando código..."
git pull origin main

# Construir y levantar servicios
echo "🐳 Levantando servicios con Docker..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando servicios..."
sleep 30

# Verificar estado
echo "🔍 Verificando estado..."
docker-compose ps

# Tests básicos
echo "🧪 Ejecutando tests..."
curl -f http://localhost:8501 || exit 1
curl -f http://localhost:8000/api/status || exit 1

echo "✅ Despliegue completado exitosamente!"
echo "📊 Dashboard: http://localhost:8501"
echo "🔧 API: http://localhost:8000"
echo "📈 Grafana: http://localhost:3000"
echo "🔍 Prometheus: http://localhost:9090"
