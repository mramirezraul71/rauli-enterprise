#!/usr/bin/env python3
"""
🔗 RAULI Desktop Shortcut Creator - Creación de acceso directo en escritorio
"""

import os
import sys
from pathlib import Path

def create_rauli_desktop_shortcut():
    """Crear acceso directo RAULI System en escritorio"""
    print("🔗 Creando acceso directo RAULI System en escritorio...")
    
    try:
        # Importar módulos necesarios
        import winshell
        from win32com.client import Dispatch
        
        # Obtener escritorio
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "RAULI System.lnk")
        
        # Rutas del sistema
        target_path = os.path.join(os.getcwd(), "rauli_boot.bat")
        working_dir = os.getcwd()
        icon_path = target_path
        
        # Verificar que el archivo target existe
        if not os.path.exists(target_path):
            print(f"❌ Archivo target no encontrado: {target_path}")
            return False
        
        # Crear acceso directo
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = working_dir
        shortcut.IconLocation = icon_path
        shortcut.Description = "RAULI System - Sistema IA Híbrido"
        shortcut.save()
        
        print(f"✅ Acceso directo creado: {shortcut_path}")
        return True
        
    except ImportError as e:
        print(f"❌ Módulos faltantes: {e}")
        print("📦 Instalando dependencias...")
        
        # Instalar dependencias
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "winshell", "pywin32"], 
                          capture_output=True, check=True)
            print("✅ Dependencias instaladas")
            
            # Reintentar creación
            return create_rauli_desktop_shortcut()
            
        except Exception as install_error:
            print(f"❌ Error instalando dependencias: {install_error}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando acceso directo: {e}")
        return False

def create_simple_batch_shortcut():
    """Crear acceso directo usando método simple"""
    print("🔗 Creando acceso directo método simple...")
    
    try:
        # Obtener escritorio
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "RAULI System.bat")
        
        # Contenido del batch
        batch_content = """@echo off
echo.
echo ========================================
echo 🚀 RAULI SYSTEM
echo ========================================
echo.

cd /d C:\\RAULI_CORE
python rauli_boot_manager.py boot

pause
"""
        
        # Crear archivo batch
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ Acceso directo batch creado: {shortcut_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo batch: {e}")
        return False

def verify_desktop_shortcut():
    """Verificar acceso directo en escritorio"""
    print("🔍 Verificando acceso directo en escritorio...")
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Buscar archivos RAULI
    rauli_files = []
    for file in os.listdir(desktop):
        if "rauli" in file.lower() or "system" in file.lower():
            rauli_files.append(file)
    
    print(f"📋 Archivos RAULI encontrados: {rauli_files}")
    
    # Verificar si existe el acceso directo
    shortcut_path = os.path.join(desktop, "RAULI System.lnk")
    batch_path = os.path.join(desktop, "RAULI System.bat")
    
    if os.path.exists(shortcut_path):
        print("✅ Acceso directo .lnk encontrado")
        return True
    elif os.path.exists(batch_path):
        print("✅ Acceso directo .bat encontrado")
        return True
    else:
        print("❌ No se encontró acceso directo RAULI System")
        return False

def main():
    """Función principal"""
    print("🔗 RAULI Desktop Shortcut Creator")
    print("=" * 50)
    
    # 1. Verificar estado actual
    verify_desktop_shortcut()
    
    # 2. Intentar crear acceso directo completo
    success = create_rauli_desktop_shortcut()
    
    # 3. Si falla, crear método simple
    if not success:
        print("🔄 Intentando método simple...")
        success = create_simple_batch_shortcut()
    
    # 4. Verificación final
    print("\n🔍 Verificación final:")
    verify_desktop_shortcut()
    
    if success:
        print("\n✅ Acceso directo RAULI System creado exitosamente")
        print("🎯 Busca 'RAULI System' en tu escritorio")
    else:
        print("\n❌ No se pudo crear el acceso directo")
        print("💡 Puedes ejecutar manualmente:")
        print("   cd C:\\RAULI_CORE")
        print("   python rauli_boot_manager.py boot")

if __name__ == "__main__":
    import subprocess
    main()
