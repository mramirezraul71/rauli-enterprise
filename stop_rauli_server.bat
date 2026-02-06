@echo off
🛑 RAULI SERVER STOP SCRIPT - WINDOWS
echo.
echo 🛑 Deteniendo servicios de RAULI Enterprise...
echo.

cd /d C:\RAULI_CORE

# Detener Docker Compose
docker-compose down

# Verificar que todo esté detenido
echo 📊 Verificando que los servicios estén detenidos...
docker-compose ps

echo.
echo ✅ Servicios detenidos
echo.
pause
