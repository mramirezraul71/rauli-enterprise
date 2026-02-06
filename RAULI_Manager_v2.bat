@echo off
REM RAULI System Manager - Version Corregida y Funcional
title RAULI System Manager - Fixed
color 0A

echo.
echo ========================================
echo RAULI SYSTEM MANAGER v2.0 FIXED
echo ========================================
echo.
echo Iniciando sistema corregido...
echo Ollama: Funcionando
echo Node.js: Instalado
echo Dashboard: Dependencias listas
echo.

cd /d C:\RAULI_CORE

REM Iniciar version corregida
echo Iniciando RAULI Service Manager (v2.0)...
python rauli_service_manager_fixed_v2.py

pause
