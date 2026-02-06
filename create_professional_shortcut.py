#!/usr/bin/env python3
"""
🚀 RAULI System Desktop Shortcut Creator - Acceso Directo Profesional
"""

import os
import sys
from pathlib import Path

def create_professional_shortcut():
    """Crear acceso directo profesional"""
    print("🔗 Creando acceso directo profesional...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        # Obtener escritorio OneDrive
        desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
        shortcut_path = os.path.join(desktop, "🚀 RAULI System Manager.lnk")
        
        # Rutas
        target_path = os.path.join(os.getcwd(), "RAULI_Manager.bat")
        working_dir = os.getcwd()
        icon_path = target_path
        
        # Verificar que el archivo target existe
        if not os.path.exists(target_path):
            print(f"❌ Archivo target no encontrado: {target_path}")
            return False
        
        # Eliminar acceso directo existente
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        
        # Crear acceso directo profesional
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = working_dir
        shortcut.IconLocation = icon_path
        shortcut.Description = "RAULI System Manager - Gestor Profesional de Servicios"
        shortcut.save()
        
        print(f"✅ Acceso directo profesional creado: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo: {e}")
        return False

def create_simple_shortcut():
    """Crear acceso directo simple"""
    print("🔗 Creando acceso directo simple...")
    
    try:
        # Obtener escritorio OneDrive
        desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
        shortcut_path = os.path.join(desktop, "RAULI Manager.bat")
        
        # Contenido del batch
        batch_content = """@echo off
title RAULI System Manager
color 0A
cd /d C:\\RAULI_CORE
python rauli_service_manager.py
if errorlevel 1 pause
"""
        
        # Crear archivo batch
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ Acceso directo simple creado: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo simple: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 RAULI System - Acceso Directo Profesional")
    print("=" * 50)
    
    # 1. Crear acceso directo profesional
    professional_ok = create_professional_shortcut()
    
    # 2. Crear acceso directo simple
    simple_ok = create_simple_shortcut()
    
    # 3. Resumen
    print("\n" + "=" * 50)
    print("📊 ACCESOS DIRECTOS PROFESIONALES")
    print("=" * 50)
    print(f"🎯 Acceso directo profesional: {'✅' if professional_ok else '❌'}")
    print(f"📝 Acceso directo simple: {'✅' if simple_ok else '❌'}")
    
    print("\n🚀 CARACTERÍSTICAS PROFESIONALES:")
    print("✅ Interfaz gráfica moderna")
    print("✅ Control centralizado de servicios")
    print("✅ Monitoreo en tiempo real")
    print("✅ Logs detallados")
    print("✅ Gestión de PIDs")
    print("✅ Start/Stop individual")
    print("✅ Diagnóstico automático")
    
    print("\n💡 USO PROFESIONAL:")
    print("1. Doble click en '🚀 RAULI System Manager.lnk'")
    print("2. Usa la interfaz gráfica para controlar todo")
    print("3. Monitorea el estado en tiempo real")
    print("4. Revisa los logs para diagnóstico")
    
    print("\n🎯 ¡Sistema profesional listo para producción!")

if __name__ == "__main__":
    main()
