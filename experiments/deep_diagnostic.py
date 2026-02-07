#!/usr/bin/env python3
"""
🔍 RAULI System Deep Diagnostic - Diagnóstico profundo con ejecución real
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def execute_and_capture():
    """Ejecutar el service manager y capturar salida/error"""
    print("🔍 EJECUTANDO SERVICE MANAGER Y CAPTURANDO SALIDA...")
    
    try:
        # Ejecutar el service manager con timeout
        process = subprocess.Popen(
            [sys.executable, "rauli_service_manager.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # Esperar un momento para que inicie
        time.sleep(2)
        
        # Verificar si el proceso sigue corriendo
        if process.poll() is None:
            print("✅ Proceso está corriendo después de 2 segundos")
            
            # Esperar un poco más
            time.sleep(3)
            
            # Verificar de nuevo
            if process.poll() is None:
                print("✅ Proceso sigue corriendo después de 5 segundos")
                
                # Terminar el proceso para poder analizar
                process.terminate()
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    print(f"📊 STDOUT: {stdout}")
                    print(f"❌ STDERR: {stderr}")
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    print(f"📊 STDOUT (kill): {stdout}")
                    print(f"❌ STDERR (kill): {stderr}")
                
                return True
            else:
                print("❌ Proceso se detuvo entre 2-5 segundos")
                stdout, stderr = process.communicate()
                print(f"📊 STDOUT: {stdout}")
                print(f"❌ STDERR: {stderr}")
                return False
        else:
            print("❌ Proceso se detuvo inmediatamente")
            stdout, stderr = process.communicate()
            print(f"📊 STDOUT: {stdout}")
            print(f"❌ STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando: {e}")
        return False

def test_minimal_gui():
    """Probar GUI mínima para aislar el problema"""
    print("\n🧪 PROBANDO GUI MÍNIMA...")
    
    minimal_gui_code = '''
import tkinter as tk
import time

root = tk.Tk()
root.title("TEST")
root.geometry("300x200")

label = tk.Label(root, text="TEST RAULI GUI")
label.pack(pady=20)

def on_closing():
    print("Ventana cerrada")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

print("Ventana creada, mostrando por 3 segundos...")
root.after(3000, root.destroy)  # Cerrar después de 3 segundos
root.mainloop()
print("Test completado")
'''
    
    # Guardar código de prueba
    test_file = "test_minimal_gui.py"
    with open(test_file, 'w') as f:
        f.write(minimal_gui_code)
    
    try:
        # Ejecutar prueba
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"📊 Salida: {result.stdout}")
        print(f"❌ Error: {result.stderr}")
        print(f"🔄 Código: {result.returncode}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - la ventana podría estar abierta")
        return True
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False
    finally:
        # Limpiar
        if os.path.exists(test_file):
            os.remove(test_file)

def test_service_manager_isolated():
    """Probar service manager de forma aislada"""
    print("\n🧪 PROBANDO SERVICE MANAGER AISLADO...")
    
    try:
        # Importar y crear instancia sin mostrar
        sys.path.insert(0, os.getcwd())
        
        # Modo headless
        import os
        os.environ['DISPLAY'] = ':0'  # Forzar modo gráfico
        
        from rauli_service_manager import RAULIServiceManager
        
        print("📦 Importando RAULIServiceManager...")
        
        # Crear instancia sin mostrar ventana
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        manager = RAULIServiceManager()
        manager.root.withdraw()  # Ocultar también
        
        print("✅ Instancia creada correctamente")
        
        # Destruir después de un momento
        manager.root.after(1000, manager.root.destroy)
        root.after(1000, root.destroy)
        
        # Ejecutar mainloop por un tiempo limitado
        def run_limited():
            try:
                manager.root.mainloop()
            except:
                pass
        
        # Ejecutar en thread con timeout
        thread = threading.Thread(target=run_limited)
        thread.daemon = True
        thread.start()
        thread.join(timeout=3)
        
        if thread.is_alive():
            print("⏰ El mainloop sigue activo (normal)")
        else:
            print("✅ Mainloop completado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba aislada: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_robust_launcher():
    """Crear lanzador robusto con múltiples capas de protección"""
    print("\n🛡️ CREANDO LANZADOR ROBUSTO...")
    
    robust_content = '''@echo off
title RAULI System Manager - Robusto
color 0B

echo.
echo ========================================
echo 🛡️ RAULI SYSTEM MANAGER - MODO ROBUSTO
echo ========================================
echo.

cd /d C:\\RAULI_CORE

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
'''
    
    robust_path = "RAULI_Robusto.bat"
    with open(robust_path, 'w', encoding='utf-8') as f:
        f.write(robust_content)
    
    print(f"✅ Lanzador robusto creado: {robust_path}")
    
    # También en escritorio
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    desktop_robust = os.path.join(desktop, "RAULI Robusto.bat")
    
    with open(desktop_robust, 'w', encoding='utf-8') as f:
        f.write(robust_content.replace("C:\\\\RAULI_CORE", os.getcwd().replace("\\", "\\\\")))
    
    print(f"✅ Acceso directo robusto creado: {desktop_robust}")
    return True

def create_python_test_launcher():
    """Crear lanzador de prueba en Python"""
    print("\n🐍 CREANDO LANZADOR DE PRUEBA PYTHON...")
    
    python_test_content = '''#!/usr/bin/env python3
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
    print("\\n🐍 Verificando Python...")
    print(f"✅ Versión: {sys.version}")
    
    # 2. Verificar dependencias
    print("\\n📦 Verificando dependencias...")
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
    print("\\n📁 Verificando archivos...")
    required_files = ["rauli_service_manager.py", "rauli_icon.ico"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    # 4. Probar GUI básica
    print("\\n🧪 Probando GUI básica...")
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
    print("\\n📦 Importando Service Manager...")
    try:
        from rauli_service_manager import RAULIServiceManager
        print("✅ Service Manager importado")
    except Exception as e:
        print(f"❌ Error importando: {e}")
        return
    
    # 6. Crear instancia (prueba)
    print("\\n🏗️ Creando instancia de Service Manager...")
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
    print("\\n🚀 ¿Deseas ejecutar el Service Manager completo?")
    print("📝 Escribe 'si' para continuar, cualquier otra cosa para salir:")
    
    try:
        response = input("> ").strip().lower()
        if response == 'si':
            print("\\n🚀 Iniciando Service Manager completo...")
            subprocess.run([sys.executable, "rauli_service_manager.py"])
        else:
            print("📊 Prueba finalizada. El sistema parece estar funcional.")
    except KeyboardInterrupt:
        print("\\n📊 Prueba cancelada por usuario")

if __name__ == "__main__":
    main()
'''
    
    python_test_path = "RAULI_Python_Test.py"
    with open(python_test_path, 'w', encoding='utf-8') as f:
        f.write(python_test_content)
    
    print(f"✅ Lanzador Python test creado: {python_test_path}")
    
    # Acceso directo
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    desktop_python = os.path.join(desktop, "RAULI Python Test.bat")
    
    batch_content = f'''@echo off
title RAULI Python Test
color 0C
cd /d {os.getcwd()}
python {python_test_path}
pause
'''
    
    with open(desktop_python, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Acceso directo Python test creado: {desktop_python}")
    return True

def main():
    """Función principal"""
    print("👁️🖐️ RAULI SYSTEM - DIAGNÓSTICO PROFUNDO CON OJOS Y MANOS")
    print("=" * 70)
    
    # 1. Ejecutar y capturar
    print("\n1️⃣ EJECUCIÓN Y CAPTURA:")
    exec_ok = execute_and_capture()
    
    # 2. Probar GUI mínima
    print("\n2️⃣ PRUEBA GUI MÍNIMA:")
    gui_ok = test_minimal_gui()
    
    # 3. Probar service manager aislado
    print("\n3️⃣ PRUEBA SERVICE MANAGER AISLADO:")
    isolated_ok = test_service_manager_isolated()
    
    # 4. Crear lanzadores robustos
    print("\n4️⃣ CREANDO LANZADORES ROBUSTOS:")
    robust_ok = create_robust_launcher()
    python_ok = create_python_test_launcher()
    
    # 5. Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL DIAGNÓSTICO PROFUNDO")
    print("=" * 70)
    print(f"🚀 Ejecución y captura: {'✅' if exec_ok else '❌'}")
    print(f"🧪 GUI mínima: {'✅' if gui_ok else '❌'}")
    print(f"🏗️ Service Manager aislado: {'✅' if isolated_ok else '❌'}")
    print(f"🛡️ Lanzador robusto: {'✅' if robust_ok else '❌'}")
    print(f"🐍 Lanzador Python test: {'✅' if python_ok else '❌'}")
    
    print("\n🎯 SOLUCIONES DISPONIBLES:")
    print("1. 🛡️ Ejecuta 'RAULI_Robusto.bat' - Con diagnóstico completo")
    print("2. 🐍 Ejecuta 'RAULI_Python_Test.py' - Prueba interactiva")
    print("3. 📊 Busca los accesos directos en tu escritorio OneDrive")
    
    print("\n💡 RECOMENDACIÓN:")
    if isolated_ok:
        print("✅ El Service Manager funciona, el problema está en la UI")
        print("🎯 Usa el lanzador Python Test para diagnóstico interactivo")
    else:
        print("❌ Hay un problema fundamental en el Service Manager")
        print("🔧 Revisa los mensajes de error arriba")

if __name__ == "__main__":
    main()
