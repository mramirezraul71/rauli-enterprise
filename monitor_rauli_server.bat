@echo off
📊 RAULI MONITORING SCRIPT - WINDOWS
echo.
echo 📊 Estado de RAULI Enterprise
echo ============================
echo.

# Verificar contenedores
echo 🐳 Contenedores:
docker-compose ps
echo.

# Verificar uso de recursos
echo 💾 Uso de recursos:
docker stats --no-stream
echo.

# Verificar salud de servicios
echo 🔍 Salud de servicios:
curl -s http://localhost:8502/_stcore/health && echo ✅ Dashboard OK || echo ❌ Dashboard ERROR
curl -s http://localhost:5000/mobile/health && echo ✅ Mobile OK || echo ❌ Mobile ERROR
echo.

# Verificar espacio en disco
echo 💿 Espacio en disco:
dir /s C:\RAULI_CORE
echo.

echo.
pause
