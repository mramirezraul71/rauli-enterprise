#!/usr/bin/env python3
"""
🔗 RAULI Desktop Shortcut Fix - Solución definitiva para acceso directo
"""

import os
import sys
from pathlib import Path

def create_simple_working_shortcut():
    """Crear acceso directo simple que funcione"""
    print("🔗 Creando acceso directo simple y funcional...")
    
    # Obtener escritorio OneDrive
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    
    # Crear batch simple sin caracteres especiales
    batch_content = f'''@echo off
title RAULI System Manager
color 0A

echo.
echo ========================================
echo RAULI SYSTEM MANAGER
echo ========================================
echo.

cd /d {os.getcwd()}

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no encontrado
    pause
    exit /b 1
)

REM Iniciar gestor
echo Iniciando RAULI Service Manager...
python rauli_service_manager_fixed.py

REM Siempre hacer pause
echo.
echo Sistema finalizado
pause
'''
    
    # Guardar en escritorio
    shortcut_path = os.path.join(desktop, "RAULI System.bat")
    with open(shortcut_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Acceso directo simple creado: {shortcut_path}")
    return True

def create_python_launcher():
    """Crear launcher Python para el escritorio"""
    print("🐍 Creando launcher Python...")
    
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    launcher_path = os.path.join(desktop, "RAULI_Launcher.py")
    
    launcher_content = f'''#!/usr/bin/env python3
"""
RAULI System Launcher - Versión simple
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("RAULI System Launcher")
    print("=" * 30)
    
    # Cambiar al directorio correcto
    os.chdir("{os.getcwd()}")
    
    # Verificar Python
    print(f"Python version: {{sys.version}}")
    
    # Verificar archivo
    if not os.path.exists("rauli_service_manager_fixed.py"):
        print("ERROR: rauli_service_manager_fixed.py not found")
        input("Press Enter to exit...")
        return
    
    # Iniciar el gestor
    try:
        print("Starting RAULI Service Manager...")
        subprocess.run([sys.executable, "rauli_service_manager_fixed.py"])
    except Exception as e:
        print(f"Error: {{e}}")
        input("Press Enter to exit...")
    
    print("Launcher finished")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
    
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"✅ Launcher Python creado: {launcher_path}")
    
    # Crear batch para ejecutar el launcher
    batch_path = os.path.join(desktop, "RAULI_Python.bat")
    batch_content = f'''@echo off
title RAULI Python Launcher
cd /d {os.getcwd()}
python "{launcher_path}"
'''
    
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Batch para launcher creado: {batch_path}")
    return True

def create_direct_exe_launcher():
    """Crear launcher que ejecuta directamente el Python"""
    print("🚀 Creando launcher directo...")
    
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    
    # Contenido del batch directo
    batch_content = f'''@echo off
cd /d {os.getcwd()}
"{sys.executable}" rauli_service_manager_fixed.py
pause
'''
    
    launcher_path = os.path.join(desktop, "RAULI_Direct.bat")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Launcher directo creado: {launcher_path}")
    return True

def clean_old_shortcuts():
    """Limpiar accesos directos antiguos"""
    print("🧹 Limpiando accesos directos antiguos...")
    
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    
    # Archivos a eliminar
    old_files = [
        "RAULI System Manager.lnk",
        "RAULI Manager.bat",
        "RAULI_Debug.bat",
        "RAULI_Simple.bat",
        "RAULI Robusto.bat",
        "RAULI Python Test.bat"
    ]
    
    removed_count = 0
    for file in old_files:
        file_path = os.path.join(desktop, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Eliminado: {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error eliminando {file}: {e}")
    
    print(f"✅ {removed_count} accesos antiguos eliminados")
    return removed_count

def test_shortcuts():
    """Probar los accesos directos creados"""
    print("🧪 Probando accesos directos...")
    
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    
    shortcuts_to_test = [
        "RAULI System.bat",
        "RAULI_Python.bat", 
        "RAULI_Direct.bat"
    ]
    
    results = {}
    for shortcut in shortcuts_to_test:
        shortcut_path = os.path.join(desktop, shortcut)
        if os.path.exists(shortcut_path):
            size = os.path.getsize(shortcut_path)
            results[shortcut] = f"✅ Existe ({size} bytes)"
        else:
            results[shortcut] = "❌ No existe"
    
    return results

def main():
    """Función principal"""
    print("🔗 RAULI DESKTOP SHORTCUT FIX")
    print("=" * 50)
    
    # 1. Limpiar accesos antiguos
    removed = clean_old_shortcuts()
    
    # 2. Crear nuevos accesos
    simple_ok = create_simple_working_shortcut()
    python_ok = create_python_launcher()
    direct_ok = create_direct_exe_launcher()
    
    # 3. Probar accesos
    test_results = test_shortcuts()
    
    # 4. Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CORRECCIÓN")
    print("=" * 50)
    print(f"🧹 Accesos antiguos eliminados: {removed}")
    print(f"📝 Acceso simple: {'✅' if simple_ok else '❌'}")
    print(f"🐍 Launcher Python: {'✅' if python_ok else '❌'}")
    print(f"🚀 Launcher directo: {'✅' if direct_ok else '❌'}")
    
    print("\n📋 ACCESOS DIRECTOS DISPONIBLES:")
    for shortcut, status in test_results.items():
        print(f"  {status} - {shortcut}")
    
    print("\n💡 RECOMENDACIÓN DE USO:")
    print("1. 🎯 Prueba 'RAULI System.bat' primero (más simple)")
    print("2. 🐍 Si no funciona, prueba 'RAULI_Python.bat'")
    print("3. 🚀 Como última opción, prueba 'RAULI_Direct.bat'")
    
    print("\n🔧 SI NINGUNO FUNCIONA:")
    print("• Abre terminal manualmente")
    print("• Navega a C:\\RAULI_CORE")
    print("• Ejecuta: python rauli_service_manager_fixed.py")

if __name__ == "__main__":
    main()
