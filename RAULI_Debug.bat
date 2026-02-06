@echo off
title RAULI System DEBUG
color 0E

echo.
echo ========================================
echo 🔍 RAULI SYSTEM - MODO DEBUG
echo ========================================
echo.

cd /d C:\RAULI_CORE

echo 🐍 Versión de Python:
python --version
echo.

echo 📁 Directorio actual:
cd
echo.

echo 📋 Archivos en RAULI_CORE:
dir /b *.py *.bat *.ico
echo.

echo 🔍 Verificando dependencias:
python -c "import tkinter; print('✅ tkinter disponible')" 2>nul || echo "❌ tkinter no disponible"
python -c "import psutil; print('✅ psutil disponible')" 2>nul || echo "❌ psutil no disponible"
python -c "import PIL; print('✅ PIL disponible')" 2>nul || echo "❌ PIL no disponible"
echo.

echo 🧪 Probando import del gestor:
python -c "from rauli_service_manager import RAULIServiceManager; print('✅ Service Manager importable')" 2>nul || echo "❌ Service Manager no importable"
echo.

echo 🚀 Iniciando gestor en modo DEBUG...
echo 💡 Si la ventana se cierra, revisa los errores arriba
echo.

REM Capturar errores
python rauli_service_manager.py 2>&1

echo.
echo ========================================
echo 🔍 DEBUG COMPLETADO
echo ========================================
echo.
echo 📊 Si hay errores, están arriba
echo 🐛 Reporta los mensajes de error
echo.
echo 🎯 Presiona cualquier tecla para salir...
pause >nul
