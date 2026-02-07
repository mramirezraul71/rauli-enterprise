#!/usr/bin/env python3
"""
🔧 RAULI System Error Fix - Corrección completa de errores del sistema
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

def check_ollama_installation():
    """Verificar instalación de Ollama"""
    print("🧠 Verificando instalación de Ollama...")
    
    try:
        # Verificar si ollama está en PATH
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama no responde correctamente")
            return False
    except FileNotFoundError:
        print("❌ Ollama no encontrado en PATH")
        return False
    except Exception as e:
        print(f"❌ Error verificando Ollama: {e}")
        return False

def install_ollama():
    """Instalar Ollama si no está presente"""
    print("📦 Instalando Ollama...")
    
    try:
        # Descargar Ollama para Windows
        ollama_url = "https://ollama.ai/download/OllamaSetup.exe"
        ollama_path = os.path.join(os.getcwd(), "OllamaSetup.exe")
        
        print(f"📥 Descargando Ollama desde {ollama_url}")
        
        # Usar PowerShell para descargar
        download_cmd = f'powershell -Command "Invoke-WebRequest -Uri \\"{ollama_url}\\" -OutFile \\"{ollama_path}\\""'
        result = subprocess.run(download_cmd, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(ollama_path):
            print(f"✅ Ollama descargado: {ollama_path}")
            print("🔧 Ejecuta manualmente OllamaSetup.exe para instalar")
            print("🔄 Después de instalar, reinicia RAULI System")
            return True
        else:
            print("❌ Error descargando Ollama")
            print("💡 Descarga manualmente desde https://ollama.ai/download")
            return False
            
    except Exception as e:
        print(f"❌ Error instalando Ollama: {e}")
        print("💡 Descarga manualmente desde https://ollama.ai/download")
        return False

def check_nodejs_npm():
    """Verificar instalación de Node.js y npm"""
    print("📱 Verificando Node.js y npm...")
    
    try:
        # Verificar Node.js
        node_result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if node_result.returncode == 0:
            print(f"✅ Node.js encontrado: {node_result.stdout.strip()}")
        else:
            print("❌ Node.js no encontrado")
            return False
        
        # Verificar npm
        npm_result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5)
        if npm_result.returncode == 0:
            print(f"✅ npm encontrado: {npm_result.stdout.strip()}")
        else:
            print("❌ npm no encontrado")
            return False
        
        return True
        
    except FileNotFoundError:
        print("❌ Node.js/npm no encontrados en PATH")
        return False
    except Exception as e:
        print(f"❌ Error verificando Node.js/npm: {e}")
        return False

def fix_dashboard_dependencies():
    """Corregir dependencias del dashboard"""
    print("📱 Corrigiendo dependencias del dashboard...")
    
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    
    if not dashboard_dir.exists():
        print(f"❌ Directorio del dashboard no encontrado: {dashboard_dir}")
        return False
    
    try:
        # Verificar package.json
        package_json = dashboard_dir / "package.json"
        if not package_json.exists():
            print("❌ package.json no encontrado")
            return False
        
        print("📦 Instalando dependencias del dashboard...")
        
        # Ejecutar npm install
        result = subprocess.run(
            ["npm", "install"],
            cwd=dashboard_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ Dependencias del dashboard instaladas")
            return True
        else:
            print(f"❌ Error instalando dependencias: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error corrigiendo dashboard: {e}")
        return False

def check_service_files():
    """Verificar archivos de servicios"""
    print("📁 Verificando archivos de servicios...")
    
    required_files = {
        "rauli_hybrid_system.py": "Sistema Híbrido IA",
        "rauli_whatsapp_professional.py": "WhatsApp Professional",
        "rauli_cloud_architecture.py": "Cloud Architecture"
    }
    
    missing_files = []
    
    for file, description in required_files.items():
        file_path = Path(file)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {description}: {file} ({size} bytes)")
        else:
            print(f"❌ {description}: {file} NO ENCONTRADO")
            missing_files.append(file)
    
    return len(missing_files) == 0

def create_service_status_report():
    """Crear reporte de estado de servicios"""
    print("📊 Creando reporte de estado...")
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system_checks": {
            "ollama": check_ollama_installation(),
            "nodejs_npm": check_nodejs_npm(),
            "service_files": check_service_files()
        },
        "recommendations": []
    }
    
    # Generar recomendaciones
    if not report["system_checks"]["ollama"]:
        report["recommendations"].append("Instalar Ollama desde https://ollama.ai/download")
    
    if not report["system_checks"]["nodejs_npm"]:
        report["recommendations"].append("Instalar Node.js desde https://nodejs.org")
    
    if not report["system_checks"]["service_files"]:
        report["recommendations"].append("Verificar archivos de servicios en C:/RAULI_CORE")
    
    # Guardar reporte
    report_path = "rauli_system_status.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Reporte guardado: {report_path}")
    return report

def create_fixed_service_manager():
    """Crear versión corregida del service manager"""
    print("🔧 Creando service manager corregido...")
    
    fixed_content = '''#!/usr/bin/env python3
"""
🚀 RAULI Service Manager - Versión Corregida
Maneja errores de forma robusta
"""

import os
import sys
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class RAULIServiceManagerFixed:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RAULI System Manager - Fixed")
        self.root.geometry("900x700")
        
        # Estado de servicios
        self.services = {
            "ollama": {"status": "checking", "port": 11434, "name": "Ollama IA Engine"},
            "hybrid_system": {"status": "checking", "port": None, "name": "Sistema Híbrido IA"},
            "whatsapp": {"status": "checking", "port": None, "name": "WhatsApp Professional"},
            "dashboard": {"status": "checking", "port": 4173, "name": "Dashboard Web"},
            "cloud_architecture": {"status": "checking", "port": 8000, "name": "Cloud Architecture"}
        }
        
        self.setup_ui()
        self.check_all_services()
        
    def setup_ui(self):
        """Configurar UI"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, text="RAULI System Manager - Fixed", 
                          font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        # Panel de servicios
        services_frame = ttk.LabelFrame(main_frame, text="Estado de Servicios", padding="10")
        services_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear widgets para servicios
        self.service_widgets = {}
        
        for i, (service_name, service_info) in enumerate(self.services.items()):
            frame = ttk.Frame(services_frame)
            frame.pack(fill=tk.X, pady=5)
            
            # Nombre
            ttk.Label(frame, text=service_info["name"], width=20).pack(side=tk.LEFT)
            
            # Estado
            status_label = ttk.Label(frame, text="Checking...", width=15)
            status_label.pack(side=tk.LEFT, padx=10)
            
            # Puerto
            port_text = str(service_info["port"]) if service_info["port"] else "N/A"
            ttk.Label(frame, text=port_text, width=10).pack(side=tk.LEFT)
            
            # Botón de acción
            action_btn = ttk.Button(frame, text="Retry", 
                                 command=lambda s=service_name: self.check_service(s))
            action_btn.pack(side=tk.RIGHT)
            
            self.service_widgets[service_name] = {
                "status": status_label,
                "action": action_btn
            }
        
        # Panel de logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        # Botones de control
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(control_frame, text="Check All", 
                  command=self.check_all_services).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Fix Issues", 
                  command=self.fix_issues).pack(side=tk.LEFT, padx=5)
        
        self.log_message("RAULI System Manager Fixed iniciado")
        
    def log_message(self, message):
        """Agregar mensaje al log"""
        self.log_area.insert(tk.END, f"{message}\\n")
        self.log_area.see(tk.END)
        self.root.update()
        
    def check_service(self, service_name):
        """Verificar un servicio específico"""
        self.log_message(f"Verificando {service_name}...")
        
        if service_name == "ollama":
            try:
                result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.update_service_status(service_name, "✅ Running", "green")
                    self.log_message("Ollama está corriendo")
                else:
                    self.update_service_status(service_name, "❌ Not Found", "red")
                    self.log_message("Ollama no encontrado - Instala desde https://ollama.ai/download")
            except FileNotFoundError:
                self.update_service_status(service_name, "❌ Not Installed", "red")
                self.log_message("Ollama no instalado - Descarga desde https://ollama.ai/download")
            except Exception as e:
                self.update_service_status(service_name, "❌ Error", "red")
                self.log_message(f"Error verificando Ollama: {e}")
                
        elif service_name == "dashboard":
            dashboard_dir = "C:/dev/RAULI-VISION/dashboard"
            if os.path.exists(dashboard_dir):
                package_json = os.path.join(dashboard_dir, "package.json")
                if os.path.exists(package_json):
                    node_modules = os.path.join(dashboard_dir, "node_modules")
                    if os.path.exists(node_modules):
                        self.update_service_status(service_name, "✅ Ready", "green")
                        self.log_message("Dashboard listo para iniciar")
                    else:
                        self.update_service_status(service_name, "⚠️ Needs npm install", "orange")
                        self.log_message("Dashboard necesita 'npm install' en el directorio")
                else:
                    self.update_service_status(service_name, "❌ package.json missing", "red")
                    self.log_message("package.json no encontrado en dashboard")
            else:
                self.update_service_status(service_name, "❌ Directory missing", "red")
                self.log_message("Directorio del dashboard no encontrado")
                
        else:
            # Verificar archivos de Python
            file_path = f"{service_name}.py"
            if os.path.exists(file_path):
                self.update_service_status(service_name, "✅ File exists", "green")
                self.log_message(f"Archivo {file_path} encontrado")
            else:
                self.update_service_status(service_name, "❌ File missing", "red")
                self.log_message(f"Archivo {file_path} no encontrado")
    
    def update_service_status(self, service_name, status, color):
        """Actualizar estado de servicio"""
        if service_name in self.service_widgets:
            self.service_widgets[service_name]["status"].config(text=status)
    
    def check_all_services(self):
        """Verificar todos los servicios"""
        self.log_message("Verificando todos los servicios...")
        for service_name in self.services:
            self.check_service(service_name)
    
    def fix_issues(self):
        """Intentar corregir problemas automáticamente"""
        self.log_message("Intentando corregir problemas...")
        
        # Sugerencias de corrección
        suggestions = [
            "1. Instala Ollama desde https://ollama.ai/download",
            "2. Instala Node.js desde https://nodejs.org",
            "3. Ejecuta 'npm install' en C:/dev/RAULI-VISION/dashboard",
            "4. Verifica que todos los archivos .py existan en C:/RAULI_CORE"
        ]
        
        for suggestion in suggestions:
            self.log_message(suggestion)
        
        messagebox.showinfo("Fix Suggestions", "\\n".join(suggestions))
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RAULIServiceManagerFixed()
    app.run()
'''
    
    with open("rauli_service_manager_fixed_v2.py", 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Service Manager corregido creado: rauli_service_manager_fixed_v2.py")
    return True

def main():
    """Función principal"""
    print("🔧 RAULI SYSTEM ERROR FIX")
    print("=" * 50)
    
    # 1. Verificar Ollama
    ollama_ok = check_ollama_installation()
    
    # 2. Verificar Node.js/npm
    nodejs_ok = check_nodejs_npm()
    
    # 3. Verificar archivos de servicios
    files_ok = check_service_files()
    
    # 4. Crear reporte
    report = create_service_status_report()
    
    # 5. Crear service manager corregido
    manager_ok = create_fixed_service_manager()
    
    # 6. Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CORRECCIÓN")
    print("=" * 50)
    print(f"🧠 Ollama: {'✅' if ollama_ok else '❌'}")
    print(f"📱 Node.js/npm: {'✅' if nodejs_ok else '❌'}")
    print(f"📁 Archivos de servicios: {'✅' if files_ok else '❌'}")
    print(f"🔧 Service Manager corregido: {'✅' if manager_ok else '❌'}")
    
    print("\n💡 RECOMENDACIONES:")
    for rec in report["recommendations"]:
        print(f"  • {rec}")
    
    print("\n🚀 PARA PROBAR LA VERSIÓN CORREGIDA:")
    print("  python rauli_service_manager_fixed_v2.py")

if __name__ == "__main__":
    main()
