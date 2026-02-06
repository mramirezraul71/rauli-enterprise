@echo off
title RAULI System Manager - Simple
color 0A

echo.
echo 🚀 RAULI SYSTEM MANAGER
echo ========================================
echo.

cd /d C:\RAULI_CORE

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)

REM Iniciar con manejo de errores
echo 🚀 Iniciando gestor...
python rauli_service_manager.py

REM Siempre hacer pause al final
echo.
echo 📊 Sistema finalizado
echo 🎯 Presiona cualquier tecla para salir...
pause >nul
