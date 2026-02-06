@echo off
REM 🚀 RAULI System Manager - Versión Final Corregida
REM Sin errores de encoding ni variables

title RAULI System Manager - Final
color 0A

echo.
echo ========================================
echo 🚀 RAULI SYSTEM MANAGER v1.0 FINAL
echo ========================================
echo.
echo 💻 Iniciando interfaz gráfica profesional...
echo 📊 Gestión completa de servicios RAULI
echo 🎛️ Control centralizado del sistema
echo 🔧 Versión corregida sin errores
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

REM Verificar archivos
echo 📁 Verificando archivos críticos...
if not exist "rauli_service_manager_fixed.py" (
    echo ❌ rauli_service_manager_fixed.py no encontrado
    pause
    exit /b 1
)

echo ✅ Archivos verificados

REM Iniciar gestor gráfico corregido
echo 🚀 Iniciando RAULI Service Manager (versión corregida)...
python rauli_service_manager_fixed.py

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
    echo 🔧 Probando versión corregida...
    python rauli_service_manager_fixed.py
    echo.
    pause
)
