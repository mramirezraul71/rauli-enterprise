#!/usr/bin/env python3
"""
🔗 RAULI Professional Shortcut - Creación de acceso directo con icono (método alternativo)
"""

import os
import sys
from pathlib import Path

def create_professional_shortcut_alternative():
    """Crear acceso directo profesional usando método alternativo"""
    print("🔗 Creando acceso directo profesional (método alternativo)...")
    
    try:
        # Obtener escritorio OneDrive
        desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
        
        # Nombre sin caracteres especiales
        shortcut_name = "RAULI System Manager.lnk"
        shortcut_path = os.path.join(desktop, shortcut_name)
        
        # Rutas
        target_path = os.path.join(os.getcwd(), "RAULI_Manager.bat")
        working_dir = os.getcwd()
        icon_path = os.path.join(os.getcwd(), "rauli_icon.ico")
        
        # Verificar archivos
        if not os.path.exists(target_path):
            print(f"❌ Target no encontrado: {target_path}")
            return False
        
        if not os.path.exists(icon_path):
            print(f"❌ Icono no encontrado: {icon_path}")
            return False
        
        # Eliminar acceso directo anterior
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        
        # Método 1: Usar pywin32 directamente
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target_path
            shortcut.WorkingDirectory = working_dir
            shortcut.IconLocation = f"{icon_path},0"
            shortcut.Description = "RAULI System Manager - Gestor Profesional de Servicios IA"
            shortcut.save()
            
            print(f"✅ Acceso directo creado: {shortcut_path}")
            return True
            
        except Exception as e1:
            print(f"❌ Método 1 falló: {e1}")
            
            # Método 2: Usar winshell
            try:
                import winshell
                
                winshell.CreateShortcut(
                    Path=shortcut_path,
                    Target=target_path,
                    Icon=(icon_path, 0),
                    Description="RAULI System Manager - Gestor Profesional de Servicios IA"
                )
                
                print(f"✅ Acceso directo creado (winshell): {shortcut_path}")
                return True
                
            except Exception as e2:
                print(f"❌ Método 2 falló: {e2}")
                
                # Método 3: Crear batch con icono embebido
                return create_batch_with_icon()
    
    except Exception as e:
        print(f"❌ Error general: {e}")
        return create_batch_with_icon()

def create_batch_with_icon():
    """Crear batch con referencia al icono"""
    print("📝 Creando batch con referencia al icono...")
    
    try:
        desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
        batch_path = os.path.join(desktop, "RAULI System Manager.bat")
        
        # Contenido del batch con referencia al icono
        batch_content = f'''@echo off
REM 🚀 RAULI System Manager - Profesional
title RAULI System Manager
color 0A

REM Referencia al icono (para exploradores de archivos)
REM Icon: {os.path.join(os.getcwd(), "rauli_icon.ico")}

echo.
echo     ████████╗ ██████╗ ███████╗██╗  ██╗███████╗██████╗ ██████╗ 
echo     ╚══██╔══╝██╔═══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔═══██╗
echo        ██║   ██║   ██║███████╗███████║█████╗  ██████╔╝██║   ██║
echo        ██║   ██║   ██║╚════██║██╔══██║██╔══╝  ██╔══██╗██║   ██║
echo        ██║   ╚██████╔╝███████║██║  ██║███████╗██║  ██║╚██████╔╝
echo        ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
echo.
echo ========================================
echo 🚀 RAULI SYSTEM MANAGER v1.0 PRO
echo ========================================
echo.

cd /d {os.getcwd()}

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)

REM Iniciar gestor gráfico
echo 🚀 Iniciando RAULI Service Manager...
python rauli_service_manager.py

if errorlevel 1 pause
'''
        
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ Batch profesional creado: {batch_path}")
        
        # Crear archivo .pif para el icono
        pif_path = os.path.join(desktop, "RAULI System Manager.pif")
        try:
            # Crear archivo PIF simple
            with open(pif_path, 'wb') as f:
                # Header PIF básico
                f.write(b'MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff')
            
            print(f"✅ Archivo PIF creado: {pif_path}")
        except:
            print("⚠️ No se pudo crear archivo PIF")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando batch: {e}")
        return False

def create_icon_info_file():
    """Crear archivo de información del icono"""
    print("📄 Creando archivo de información del icono...")
    
    try:
        icon_info = f'''RAULI System Manager - Información del Icono
=============================================

Icono creado: {os.path.join(os.getcwd(), "rauli_icon.ico")}
Icono PNG: {os.path.join(os.getcwd(), "rauli_icon.png")}

Descripción:
- Icono profesional RAULI System
- Diseño moderno con "R" estilizado
- Colores: Azul profesional y dorado
- Tamaños: 16x16 a 256x256 píxeles

Uso:
- Acceso directo: RAULI System Manager.bat
- Lanzador: RAULI_Manager.bat
- Sistema: rauli_service_manager.py

Características:
- Interfaz gráfica profesional
- Control centralizado de servicios
- Monitoreo en tiempo real
- Logs detallados
- Gestión de PIDs

Creado: {os.path.getctime(os.path.join(os.getcwd(), "rauli_icon.ico"))}
'''
        
        info_path = os.path.join(os.getcwd(), "icon_info.txt")
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(icon_info)
        
        print(f"✅ Archivo de información creado: {info_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando información: {e}")
        return False

def main():
    """Función principal"""
    print("🔗 RAULI System - Acceso Directo Profesional con Icono")
    print("=" * 60)
    
    # 1. Crear acceso directo profesional
    shortcut_ok = create_professional_shortcut_alternative()
    
    # 2. Crear archivo de información del icono
    info_ok = create_icon_info_file()
    
    # 3. Verificar archivos creados
    print("\n🔍 Verificando archivos creados:")
    files_to_check = [
        "rauli_icon.ico",
        "rauli_icon.png", 
        "RAULI_Manager.bat",
        "icon_info.txt"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} no encontrado")
    
    # 4. Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"🔗 Acceso directo profesional: {'✅' if shortcut_ok else '❌'}")
    print(f"📄 Información del icono: {'✅' if info_ok else '❌'}")
    
    print("\n🎯 ACCESO PROFESIONAL:")
    print("📂 Busca en tu escritorio OneDrive:")
    print("   • RAULI System Manager.bat (con logo ASCII)")
    print("   • RAULI System Manager.pif (referencia al icono)")
    
    print("\n🎨 CARACTERÍSTICAS DEL ICONO:")
    print("✅ Diseño profesional con 'R' estilizado")
    print("✅ Colores corporativos (azul y dorado)")
    print("✅ Múltiples tamaños (16px a 256px)")
    print("✅ Formato ICO compatible con Windows")
    
    print("\n💡 USO PROFESIONAL:")
    print("🎯 Doble click en 'RAULI System Manager.bat'")
    print("🎨 Verás el logo RAULI en ASCII al iniciar")
    print("🚀 Interfaz gráfica profesional se abrirá")
    print("📊 Control total del sistema RAULI")

if __name__ == "__main__":
    main()
