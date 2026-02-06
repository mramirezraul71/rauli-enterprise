@echo off
REM 🚀 RAULI System Manager - Versión Profesional con Logo
title RAULI System Manager
color 0A

REM Logo RAULI
echo.
echo     ████████╗ ██████╗ ███████╗██╗  ██╗███████╗██████╗ ██████╗ 
echo     ╚══██╔══╝██╔═══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔═══██╗
echo        ██║   ██║   ██║███████╗███████║█████╗  ██████╔╝██║   ██║
echo        ██║   ██║   ██║╚════██║██╔══██║██╔══╝  ██╔══██╗██║   ██║
echo        ██║   ╚██████╔╝███████║██║  ██║███████╗██║  ██║╚██████╔╝
echo        ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
echo.
echo     ███████╗ ██████╗ ██╗   ██╗███████╗████████╗ ██████╗ ███╗   ███╗
echo     ██╔════╝██╔═══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗████╗ ████║
echo     ███████╗██║   ██║██║   ██║█████╗     ██║   ██║   ██║██╔████╔██║
echo     ╚════██║██║   ██║╚██╗ ██╔╝██╔══╝     ██║   ██║   ██║██║╚██╔╝██║
echo     ███████║╚██████╔╝ ╚████╔╝ ███████╗   ██║   ╚██████╔╝██║ ╚═╝ ██║
echo     ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
echo.
echo ========================================
echo 🚀 RAULI SYSTEM MANAGER v1.0
echo ========================================
echo.
echo 💻 Iniciando interfaz gráfica profesional...
echo 📊 Gestión completa de servicios RAULI
echo 🎛️ Control centralizado del sistema IA
echo.

cd /d C:\RAULI_CORE

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo 💡 Por favor instala Python 3.11+
    pause
    exit /b 1
)

REM Iniciar gestor gráfico
echo 🚀 Iniciando RAULI Service Manager...
python rauli_service_manager.py

REM Si hay error, mostrar diagnóstico
if errorlevel 1 (
    echo.
    echo ❌ Error iniciando el gestor gráfico
    echo 🐛 Ejecutando diagnóstico...
    echo.
    echo 📋 Información del sistema:
    python --version
    echo.
    echo 📁 Archivos en RAULI_CORE:
    dir /b *.py
    echo.
    echo 🔍 Verificando dependencias...
    python -c "import tkinter; print('✅ tkinter disponible')" 2>nul || echo "❌ tkinter no disponible"
    python -c "import psutil; print('✅ psutil disponible')" 2>nul || echo "❌ psutil no disponible"
    echo.
    echo 💡 Si faltan dependencias, ejecuta:
    echo    pip install psutil
    echo.
    pause
)
