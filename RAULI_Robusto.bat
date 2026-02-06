@echo off
title RAULI System Manager - Robusto
color 0B

echo.
echo ========================================
echo 🛡️ RAULI SYSTEM MANAGER - MODO ROBUSTO
echo ========================================
echo.

cd /d C:\RAULI_CORE

REM Verificación básica
echo 🐍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Verificar archivos
echo 📁 Verificando archivos...
if not exist "rauli_service_manager.py" (
    echo ❌ rauli_service_manager.py no encontrado
    pause
    exit /b 1
)

if not exist "rauli_icon.ico" (
    echo ⚠️ rauli_icon.ico no encontrado (continuando)
)

echo ✅ Archivos verificados

REM Ejecutar con captura de errores
echo.
echo 🚀 Iniciando Service Manager...
echo 💡 Si la ventana se cierra, revisa los mensajes abajo
echo.

REM Método 1: Ejecución directa con manejo de errores
python rauli_service_manager.py 2>&1
set error_level=%errorlevel%

echo.
echo ========================================
echo 📊 RESULTADO DE LA EJECUCIÓN
echo ========================================
echo.
echo 🔄 Código de salida: %error_level%

if %error_level% equ 0 (
    echo ✅ Ejecución completada normalmente
) else (
    echo ❌ Error detectado (código %error_level%)
    echo.
    echo 🔍 Ejecutando diagnóstico rápido...
    python -c "import tkinter; print('✅ tkinter OK')" 2>nul || echo "❌ tkinter ERROR"
    python -c "import psutil; print('✅ psutil OK')" 2>nul || echo "❌ psutil ERROR"
    python -c "from rauli_service_manager import RAULIServiceManager; print('✅ Service Manager OK')" 2>nul || echo "❌ Service Manager ERROR"
)

echo.
echo 🎯 Presiona cualquier tecla para salir...
pause >nul
