@echo off
title RAULI Dashboard Launcher
color 0A

echo.
echo ========================================
echo RAULI DASHBOARD LAUNCHER
echo ========================================
echo.

cd /d C:\dev\RAULI-VISION\dashboard

REM Verificar build
if not exist "dist" (
    echo 🏗️ Build no encontrado - Construyendo...
    npm run build
)

REM Iniciar servidor simple
echo 🌐 Iniciando servidor dashboard...
python C:\RAULI_CORE\dashboard_server.py

pause
