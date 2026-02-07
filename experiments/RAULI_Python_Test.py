#!/usr/bin/env python3
"""
🧪 RAULI System Test Launcher - Prueba completa del sistema
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    print("🧪 RAULI SYSTEM TEST LAUNCHER")
    print("=" * 50)
    
    # 1. Verificar entorno
    print("\n🐍 Verificando Python...")
    print(f"✅ Versión: {sys.version}")
    
    # 2. Verificar dependencias
    print("\n📦 Verificando dependencias...")
    try:
        import tkinter
        print("✅ tkinter")
    except ImportError as e:
        print(f"❌ tkinter: {e}")
        return
    
    try:
        import psutil
        print("✅ psutil")
    except ImportError as e:
        print(f"❌ psutil: {e}")
        return
    
    # 3. Verificar archivos
    print("\n📁 Verificando archivos...")
    required_files = ["rauli_service_manager.py", "rauli_icon.ico"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    # 4. Probar GUI básica
    print("\n🧪 Probando GUI básica...")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        print("✅ GUI básica funcional")
    except Exception as e:
        print(f"❌ GUI básica error: {e}")
        return
    
    # 5. Importar service manager
    print("\n📦 Importando Service Manager...")
    try:
        from rauli_service_manager import RAULIServiceManager
        print("✅ Service Manager importado")
    except Exception as e:
        print(f"❌ Error importando: {e}")
        return
    
    # 6. Crear instancia (prueba)
    print("\n🏗️ Creando instancia de Service Manager...")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        
        manager = RAULIServiceManager()
        manager.root.withdraw()
        
        print("✅ Instancia creada correctamente")
        
        # Destruir
        manager.root.destroy()
        root.destroy()
        
        print("✅ Prueba completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando instancia: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 7. Preguntar si ejecutar completo
    print("\n🚀 ¿Deseas ejecutar el Service Manager completo?")
    print("📝 Escribe 'si' para continuar, cualquier otra cosa para salir:")
    
    try:
        response = input("> ").strip().lower()
        if response == 'si':
            print("\n🚀 Iniciando Service Manager completo...")
            subprocess.run([sys.executable, "rauli_service_manager.py"])
        else:
            print("📊 Prueba finalizada. El sistema parece estar funcional.")
    except KeyboardInterrupt:
        print("\n📊 Prueba cancelada por usuario")

if __name__ == "__main__":
    main()
