#!/usr/bin/env python3
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
        self.log_area.insert(tk.END, f"{message}\n")
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
        
        messagebox.showinfo("Fix Suggestions", "\n".join(suggestions))
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RAULIServiceManagerFixed()
    app.run()
