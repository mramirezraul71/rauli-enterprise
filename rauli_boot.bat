@echo off
REM 🚀 RAULI System Boot - Arranque Automático
echo.
echo ========================================
echo 🚀 RAULI SYSTEM BOOT MANAGER
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Instalando...
    goto :install_python
)

REM Iniciar sistema
echo 🚀 Iniciando RAULI System...
cd /d C:\RAULI_CORE
python rauli_boot_manager.py boot

goto :end

:install_python
echo 📦 Descargando Python...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
echo 🔧 Instalando Python...
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
del python_installer.exe
echo ✅ Python instalado. Reiniciando arranque...
timeout /t 5
goto :start

:end
echo.
echo 🎯 ARRANQUE COMPLETADO
echo 📊 Revisa el estado de los servicios
echo 💡 Usa 'python rauli_boot_manager.py status' para verificar
echo.
pause
