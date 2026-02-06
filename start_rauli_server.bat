@echo off
🚀 RAULI SERVER STARTUP SCRIPT - WINDOWS
echo.
echo 🚀 Iniciando servicios de RAULI Enterprise...
echo.

cd /d C:\RAULI_CORE

# Iniciar Docker Compose
docker-compose up -d

# Verificar servicios
echo 📊 Verificando servicios...
docker-compose ps

# Verificar salud de servicios
echo 🔍 Verificando salud de servicios...
curl -f http://localhost:8502/_stcore/health || echo ⚠️ Dashboard no responde
curl -f http://localhost:5000/mobile/health || echo ⚠️ Mobile no responde

echo.
echo ✅ Servicios iniciados
echo 🌐 Dashboard: http://localhost:8502
echo 📱 Mobile: http://localhost:5000/mobile
echo 📊 Monitoring: http://localhost:3000 (Grafana)
echo.
pause
