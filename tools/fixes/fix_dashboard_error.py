#!/usr/bin/env python3
"""
🔧 RAULI Dashboard Error Fix - Diagnóstico y corrección de errores del dashboard
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def diagnose_dashboard_error():
    """Diagnosticar error específico del dashboard"""
    print("🔍 DIAGNOSTICANDO ERROR EN DASHBOARD")
    print("=" * 50)
    
    # 1. Verificar directorio del dashboard
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    print(f"\n📁 Verificando directorio: {dashboard_dir}")
    
    if not dashboard_dir.exists():
        print(f"❌ Directorio no encontrado: {dashboard_dir}")
        return False
    
    print(f"✅ Directorio encontrado")
    
    # 2. Verificar archivos críticos
    critical_files = ["package.json", "vite.config.ts", "src/main.tsx", "index.html"]
    
    print("\n📋 Verificando archivos críticos:")
    for file in critical_files:
        file_path = dashboard_dir / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} NO ENCONTRADO")
            return False
    
    # 3. Verificar node_modules
    node_modules = dashboard_dir / "node_modules"
    print(f"\n📦 Verificando node_modules: {node_modules}")
    
    if not node_modules.exists():
        print("❌ node_modules no encontrado - Ejecutando npm install...")
        return install_dashboard_deps()
    else:
        print("✅ node_modules encontrado")
    
    # 4. Probar comando npm run preview
    print("\n🚀 Probando comando npm run preview...")
    
    try:
        # Ejecutar npm run preview con timeout
        process = subprocess.Popen(
            ["npm", "run", "preview"],
            cwd=dashboard_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Esperar un momento para ver si inicia
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ npm run preview inició correctamente")
            
            # Verificar si el servidor está corriendo
            time.sleep(3)
            
            # Intentar conectarse al servidor
            try:
                import urllib.request
                response = urllib.request.urlopen('http://localhost:4173', timeout=5)
                if response.getcode() == 200:
                    print("✅ Dashboard accesible en http://localhost:4173")
                    
                    # Terminar el proceso
                    process.terminate()
                    return True
                else:
                    print(f"⚠️ Dashboard respondió con código {response.getcode()}")
            except Exception as e:
                print(f"❌ Error accediendo al dashboard: {e}")
            
            # Terminar el proceso
            process.terminate()
            return False
        else:
            stdout, stderr = process.communicate()
            print(f"❌ npm run preview falló")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando npm run preview: {e}")
        return False

def install_dashboard_deps():
    """Instalar dependencias del dashboard"""
    print("📦 Instalando dependencias del dashboard...")
    
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    
    try:
        # Ejecutar npm install
        result = subprocess.run(
            ["npm", "install"],
            cwd=dashboard_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ Dependencias instaladas correctamente")
            return True
        else:
            print(f"❌ Error instalando dependencias: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def check_dashboard_build():
    """Verificar si el dashboard está construido"""
    print("🏗️ Verificando build del dashboard...")
    
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    dist_dir = dashboard_dir / "dist"
    
    if not dist_dir.exists():
        print("❌ Directorio dist no encontrado - Construyendo...")
        return build_dashboard()
    else:
        print("✅ Build encontrado")
        
        # Verificar archivos críticos en dist
        critical_files = ["index.html", "assets/"]
        for file in critical_files:
            file_path = dist_dir / file
            if file_path.exists():
                print(f"✅ {file} encontrado")
            else:
                print(f"❌ {file} no encontrado en dist")
                return build_dashboard()
        
        return True

def build_dashboard():
    """Construir el dashboard"""
    print("🏗️ Construyendo dashboard...")
    
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    
    try:
        # Ejecutar npm run build
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=dashboard_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ Dashboard construido correctamente")
            return True
        else:
            print(f"❌ Error construyendo dashboard: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error construyendo dashboard: {e}")
        return False

def create_simple_dashboard_server():
    """Crear servidor simple para el dashboard"""
    print("🌐 Creando servidor simple para dashboard...")
    
    server_code = '''#!/usr/bin/env python3
"""
🌐 RAULI Dashboard Simple Server
"""

import http.server
import socketserver
import os
from pathlib import Path

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dist", **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    port = 4173
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    
    if not dashboard_dir.exists():
        print("❌ Directorio del dashboard no encontrado")
        return
    
    # Cambiar al directorio del dashboard
    os.chdir(dashboard_dir)
    
    if not Path("dist").exists():
        print("❌ Build no encontrado - Ejecuta 'npm run build' primero")
        return
    
    print(f"🌐 Iniciando servidor en http://localhost:{port}")
    print("📱 Dashboard RAULI disponible")
    print("🛑 Presiona Ctrl+C para detener")
    
    with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\n🛑 Servidor detenido")

if __name__ == "__main__":
    main()
'''
    
    server_path = "dashboard_server.py"
    with open(server_path, 'w', encoding='utf-8') as f:
        f.write(server_code)
    
    print(f"✅ Servidor simple creado: {server_path}")
    return True

def create_dashboard_launcher():
    """Crear launcher para el dashboard"""
    print("🚀 Creando launcher para dashboard...")
    
    launcher_content = '''@echo off
title RAULI Dashboard Launcher
color 0A

echo.
echo ========================================
echo RAULI DASHBOARD LAUNCHER
echo ========================================
echo.

cd /d C:\\dev\\RAULI-VISION\\dashboard

REM Verificar build
if not exist "dist" (
    echo 🏗️ Build no encontrado - Construyendo...
    npm run build
)

REM Iniciar servidor simple
echo 🌐 Iniciando servidor dashboard...
python C:\\RAULI_CORE\\dashboard_server.py

pause
'''
    
    launcher_path = "RAULI_Dashboard.bat"
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"✅ Launcher creado: {launcher_path}")
    
    # También en escritorio
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    desktop_launcher = os.path.join(desktop, "RAULI Dashboard.bat")
    
    with open(desktop_launcher, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"✅ Launcher en escritorio: {desktop_launcher}")
    return True

def main():
    """Función principal"""
    print("🔧 RAULI DASHBOARD ERROR FIX")
    print("=" * 50)
    
    # 1. Diagnosticar error
    diagnosis_ok = diagnose_dashboard_error()
    
    # 2. Verificar build
    build_ok = check_dashboard_build()
    
    # 3. Crear servidor simple
    server_ok = create_simple_dashboard_server()
    
    # 4. Crear launcher
    launcher_ok = create_dashboard_launcher()
    
    # 5. Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CORRECCIÓN")
    print("=" * 50)
    print(f"🔍 Diagnóstico: {'✅' if diagnosis_ok else '❌'}")
    print(f"🏗️ Build: {'✅' if build_ok else '❌'}")
    print(f"🌐 Servidor simple: {'✅' if server_ok else '❌'}")
    print(f"🚀 Launcher: {'✅' if launcher_ok else '❌'}")
    
    print("\n💡 SOLUCIONES DISPONIBLES:")
    print("1. 🚀 Ejecuta 'RAULI_Dashboard.bat' (escritorio)")
    print("2. 🌐 Ejecuta 'python dashboard_server.py'")
    print("3. 📦 Ejecuta 'npm run build' manualmente")
    print("4. 🔧 Ejecuta 'npm run preview' manualmente")
    
    print("\n🎯 RECOMENDACIÓN:")
    if diagnosis_ok:
        print("✅ El dashboard debería funcionar con el launcher")
    else:
        print("❌ Revisa los errores mostrados arriba")

if __name__ == "__main__":
    main()
