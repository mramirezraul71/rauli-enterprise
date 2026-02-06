#!/usr/bin/env python3
"""
🔍 RAULI System Diagnostic Tool - Diagnóstico completo del problema
"""

import os
import sys
import subprocess
import traceback
from pathlib import Path

def diagnose_system():
    """Diagnóstico completo del sistema"""
    print("🔍 RAULI SYSTEM DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # 1. Verificar Python
    print("\n🐍 DIAGNÓSTICO DE PYTHON:")
    try:
        python_version = sys.version
        print(f"✅ Versión Python: {python_version}")
    except Exception as e:
        print(f"❌ Error Python: {e}")
        return False
    
    # 2. Verificar dependencias
    print("\n📦 DIAGNÓSTICO DE DEPENDENCIAS:")
    dependencies = ["tkinter", "psutil", "PIL", "winshell", "win32com"]
    
    for dep in dependencies:
        try:
            if dep == "tkinter":
                import tkinter
                print(f"✅ {dep} - OK")
            elif dep == "psutil":
                import psutil
                print(f"✅ {dep} - OK")
            elif dep == "PIL":
                from PIL import Image
                print(f"✅ {dep} - OK")
            elif dep == "winshell":
                import winshell
                print(f"✅ {dep} - OK")
            elif dep == "win32com":
                import win32com.client
                print(f"✅ {dep} - OK")
        except ImportError as e:
            print(f"❌ {dep} - FALTA: {e}")
        except Exception as e:
            print(f"⚠️ {dep} - ERROR: {e}")
    
    # 3. Verificar archivos RAULI
    print("\n📁 DIAGNÓSTICO DE ARCHIVOS RAULI:")
    rauli_files = [
        "rauli_service_manager.py",
        "RAULI_Manager.bat",
        "rauli_icon.ico",
        "rauli_boot_manager.py"
    ]
    
    for file in rauli_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} - {size} bytes")
        else:
            print(f"❌ {file} - NO ENCONTRADO")
    
    # 4. Verificar acceso directo
    print("\n🔗 DIAGNÓSTICO DE ACCESO DIRECTO:")
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    shortcut_path = os.path.join(desktop, "RAULI System Manager.lnk")
    
    if os.path.exists(shortcut_path):
        print(f"✅ Acceso directo encontrado: {shortcut_path}")
        size = os.path.getsize(shortcut_path)
        print(f"✅ Tamaño: {size} bytes")
    else:
        print(f"❌ Acceso directo NO encontrado: {shortcut_path}")
    
    # 5. Probar ejecución del gestor
    print("\n🚀 DIAGNÓSTICO DE EJECUCIÓN:")
    try:
        print("🧪 Probando import de módulos del gestor...")
        
        # Probar import del gestor
        sys.path.insert(0, os.getcwd())
        
        try:
            import tkinter as tk
            print("✅ tkinter importado correctamente")
        except Exception as e:
            print(f"❌ Error importando tkinter: {e}")
            return False
        
        try:
            import psutil
            print("✅ psutil importado correctamente")
        except Exception as e:
            print(f"❌ Error importando psutil: {e}")
            return False
        
        # Probar creación de ventana simple
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar inmediatamente
            root.destroy()
            print("✅ Ventana tkinter creada correctamente")
        except Exception as e:
            print(f"❌ Error creando ventana tkinter: {e}")
            return False
        
        print("✅ Pruebas básicas superadas")
        
    except Exception as e:
        print(f"❌ Error en diagnóstico de ejecución: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_service_manager():
    """Probar ejecución del service manager"""
    print("\n🧪 PROBANDO SERVICE MANAGER:")
    
    try:
        # Importar el gestor
        from rauli_service_manager import RAULIServiceManager
        
        print("✅ RAULIServiceManager importado correctamente")
        
        # Probar creación sin mostrar
        print("🧪 Creando instancia...")
        
        # Crear instancia sin mostrar la ventana
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana
        
        manager = RAULIServiceManager()
        manager.root.withdraw()  # Ocultar también
        
        print("✅ Instancia creada correctamente")
        
        # Destruir
        manager.root.destroy()
        root.destroy()
        
        print("✅ Prueba completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error probando service manager: {e}")
        traceback.print_exc()
        return False

def create_debug_launcher():
    """Crear lanzador de depuración"""
    print("\n🔧 CREANDO LANZADOR DE DEPURACIÓN:")
    
    debug_content = '''@echo off
title RAULI System DEBUG
color 0E

echo.
echo ========================================
echo 🔍 RAULI SYSTEM - MODO DEBUG
echo ========================================
echo.

cd /d C:\\RAULI_CORE

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
'''
    
    debug_path = "RAULI_Debug.bat"
    with open(debug_path, 'w', encoding='utf-8') as f:
        f.write(debug_content)
    
    print(f"✅ Lanzador DEBUG creado: {debug_path}")
    
    # También crear acceso directo en escritorio
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    desktop_debug = os.path.join(desktop, "RAULI Debug.bat")
    
    with open(desktop_debug, 'w', encoding='utf-8') as f:
        f.write(debug_content.replace("C:\\\\RAULI_CORE", os.getcwd().replace("\\", "\\\\")))
    
    print(f"✅ Acceso directo DEBUG creado: {desktop_debug}")
    return True

def create_simple_launcher():
    """Crear lanzador simple que no se cierra"""
    print("\n🔧 CREANDO LANZADOR SIMPLE:")
    
    simple_content = '''@echo off
title RAULI System Manager - Simple
color 0A

echo.
echo 🚀 RAULI SYSTEM MANAGER
echo ========================================
echo.

cd /d C:\\RAULI_CORE

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
'''
    
    simple_path = "RAULI_Simple.bat"
    with open(simple_path, 'w', encoding='utf-8') as f:
        f.write(simple_content)
    
    print(f"✅ Lanzador simple creado: {simple_path}")
    
    # Acceso directo en escritorio
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    desktop_simple = os.path.join(desktop, "RAULI Simple.bat")
    
    with open(desktop_simple, 'w', encoding='utf-8') as f:
        f.write(simple_content.replace("C:\\\\RAULI_CORE", os.getcwd().replace("\\", "\\\\")))
    
    print(f"✅ Acceso directo simple creado: {desktop_simple}")
    return True

def main():
    """Función principal"""
    print("🔍 RAULI SYSTEM - DIAGNÓSTICO COMPLETO")
    print("=" * 60)
    
    # 1. Diagnóstico completo
    diagnosis_ok = diagnose_system()
    
    # 2. Probar service manager
    if diagnosis_ok:
        test_ok = test_service_manager()
    else:
        test_ok = False
    
    # 3. Crear lanzadores alternativos
    debug_ok = create_debug_launcher()
    simple_ok = create_simple_launcher()
    
    # 4. Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    print(f"🔍 Diagnóstico del sistema: {'✅' if diagnosis_ok else '❌'}")
    print(f"🧪 Prueba del gestor: {'✅' if test_ok else '❌'}")
    print(f"🔧 Lanzador DEBUG: {'✅' if debug_ok else '❌'}")
    print(f"📝 Lanzador simple: {'✅' if simple_ok else '❌'}")
    
    print("\n🎯 SOLUCIONES DISPONIBLES:")
    print("1. 📊 Ejecuta 'RAULI_Debug.bat' para diagnóstico completo")
    print("2. 📝 Ejecuta 'RAULI_Simple.bat' para versión simple")
    print("3. 🔗 Busca los accesos directos en tu escritorio OneDrive")
    
    print("\n💡 PASOS A SEGUIR:")
    print("1. Ejecuta el lanzador DEBUG")
    print("2. Revisa los mensajes de error")
    print("3. Reporta los errores específicos")
    print("4. Si funciona el simple, el problema está en la UI")

if __name__ == "__main__":
    main()
