#!/usr/bin/env python3
"""
🚀 RAULI Service Manager - Versión Definitiva Corregida
Solución profesional sin errores de encoding ni variables
"""

import os
import sys
import time
import json
import threading
import subprocess
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import psutil

class RAULIServiceManager:
    def __init__(self):
        # Inicializar variables ANTES de usarlas
        self.root = tk.Tk()
        self.root.title("RAULI System Manager v1.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Servicios - definición clara y temprana
        self.services = {
            "ollama": {"status": "stopped", "pid": None, "port": 11434, "name": "Ollama IA Engine"},
            "hybrid_system": {"status": "stopped", "pid": None, "port": None, "name": "Sistema Híbrido IA"},
            "whatsapp": {"status": "stopped", "pid": None, "port": None, "name": "WhatsApp Professional"},
            "dashboard": {"status": "stopped", "pid": None, "port": 4173, "name": "Dashboard Web"},
            "cloud_architecture": {"status": "stopped", "pid": None, "port": 8000, "name": "Cloud Architecture"}
        }
        
        self.log_messages = []
        self.is_monitoring = False
        self.service_widgets = {}
        
        # Configurar UI
        self.setup_ui()
        
        # Iniciar monitoreo
        self.start_monitoring()
        
    def setup_ui(self):
        """Configurar interfaz gráfica profesional"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="RAULI System Manager", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        status_label = ttk.Label(header_frame, text="Ready", 
                               font=("Arial", 12), foreground="green")
        status_label.pack(side=tk.RIGHT)
        
        # Panel de servicios
        services_frame = ttk.LabelFrame(main_frame, text="Servicios RAULI", padding="10")
        services_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Headers
        headers = ["Servicio", "Estado", "Puerto", "PID", "Acciones"]
        for i, header in enumerate(headers):
            ttk.Label(services_frame, text=header, font=("Arial", 10, "bold")).grid(
                row=0, column=i, padx=5, pady=5
            )
        
        # Servicios
        service_names = ["ollama", "hybrid_system", "whatsapp", "dashboard", "cloud_architecture"]
        
        for i, service_name in enumerate(service_names, 1):
            service_info = self.services[service_name]
            
            # Nombre del servicio
            name_label = ttk.Label(services_frame, text=service_info["name"])
            name_label.grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            
            # Estado
            status_label = ttk.Label(services_frame, text="Stopped", foreground="red")
            status_label.grid(row=i, column=1, padx=5, pady=2)
            
            # Puerto
            port_text = str(service_info["port"]) if service_info["port"] else "N/A"
            port_label = ttk.Label(services_frame, text=port_text)
            port_label.grid(row=i, column=2, padx=5, pady=2)
            
            # PID
            pid_label = ttk.Label(services_frame, text="N/A")
            pid_label.grid(row=i, column=3, padx=5, pady=2)
            
            # Botones
            button_frame = ttk.Frame(services_frame)
            button_frame.grid(row=i, column=4, padx=5, pady=2)
            
            start_btn = ttk.Button(button_frame, text="Start", width=8,
                                 command=lambda s=service_name: self.start_service(s))
            start_btn.pack(side=tk.LEFT, padx=2)
            
            stop_btn = ttk.Button(button_frame, text="Stop", width=8,
                                command=lambda s=service_name: self.stop_service(s))
            stop_btn.pack(side=tk.LEFT, padx=2)
            
            # Guardar widgets
            self.service_widgets[service_name] = {
                "status": status_label,
                "port": port_label,
                "pid": pid_label,
                "start": start_btn,
                "stop": stop_btn
            }
        
        # Panel de control
        control_frame = ttk.LabelFrame(main_frame, text="Control del Sistema", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botones principales
        ttk.Button(control_frame, text="Iniciar Todo", 
                  command=self.start_all_services).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Detener Todo", 
                  command=self.stop_all_services).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Reiniciar Todo", 
                  command=self.restart_all_services).pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(control_frame, orient="vertical").pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # Botones de sistema
        ttk.Button(control_frame, text="Ver Estado", 
                  command=self.show_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Abrir Endpoints", 
                  command=self.open_endpoints).pack(side=tk.LEFT, padx=5)
        
        # Panel de logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs del Sistema", padding="10")
        log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Área de logs
        self.log_area = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        # Configurar colores para logs
        self.log_area.tag_configure("INFO", foreground="blue")
        self.log_area.tag_configure("SUCCESS", foreground="green")
        self.log_area.tag_configure("ERROR", foreground="red")
        self.log_area.tag_configure("WARNING", foreground="orange")
        
        # Barra de estado
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN)
        self.status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Mensaje inicial
        self.log_message("RAULI System Manager iniciado", "SUCCESS")
        self.log_message("Sistema listo para operar", "INFO")
        
    def log_message(self, message, level="INFO"):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_area.insert(tk.END, formatted_message, level)
        self.log_area.see(tk.END)
        
        # Actualizar barra de estado
        self.status_bar.config(text=f"{level}: {message.strip()}")
        
        # Guardar en memoria
        self.log_messages.append({"timestamp": timestamp, "message": message, "level": level})
    
    def start_service(self, service_name):
        """Iniciar un servicio específico"""
        self.log_message(f"Iniciando {service_name}...", "INFO")
        
        try:
            if service_name == "ollama":
                # Verificar si Ollama ya está corriendo
                result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.update_service_status(service_name, "running", None)
                    self.log_message(f"{service_name} ya estaba corriendo", "SUCCESS")
                    return
            
            elif service_name == "dashboard":
                # Iniciar dashboard
                dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
                if dashboard_dir.exists():
                    process = subprocess.Popen(
                        ["npm", "run", "preview"],
                        cwd=dashboard_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    self.services[service_name]["pid"] = process.pid
                    time.sleep(3)
                    self.update_service_status(service_name, "running", process.pid)
                    self.log_message(f"{service_name} iniciado correctamente", "SUCCESS")
                    return
            
            elif service_name == "hybrid_system":
                # Iniciar sistema híbrido
                script_path = Path("C:/RAULI_CORE/rauli_hybrid_system.py")
                if script_path.exists():
                    process = subprocess.Popen(
                        [sys.executable, str(script_path)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    self.services[service_name]["pid"] = process.pid
                    time.sleep(2)
                    self.update_service_status(service_name, "running", process.pid)
                    self.log_message(f"{service_name} iniciado correctamente", "SUCCESS")
                    return
            
            elif service_name == "whatsapp":
                # Iniciar WhatsApp
                script_path = Path("C:/RAULI_CORE/rauli_whatsapp_professional.py")
                if script_path.exists():
                    process = subprocess.Popen(
                        [sys.executable, str(script_path)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    self.services[service_name]["pid"] = process.pid
                    time.sleep(2)
                    self.update_service_status(service_name, "running", process.pid)
                    self.log_message(f"{service_name} iniciado correctamente", "SUCCESS")
                    return
            
            self.log_message(f"No se pudo iniciar {service_name}", "ERROR")
            
        except Exception as e:
            self.log_message(f"Error iniciando {service_name}: {e}", "ERROR")
    
    def stop_service(self, service_name):
        """Detener un servicio específico"""
        self.log_message(f"Deteniendo {service_name}...", "INFO")
        
        try:
            service = self.services[service_name]
            if service["pid"]:
                process = psutil.Process(service["pid"])
                process.terminate()
                
                # Esperar a que termine
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    process.kill()
                
                service["pid"] = None
                self.update_service_status(service_name, "stopped", None)
                self.log_message(f"{service_name} detenido correctamente", "SUCCESS")
            else:
                self.log_message(f"{service_name} no estaba corriendo", "WARNING")
                
        except Exception as e:
            self.log_message(f"Error deteniendo {service_name}: {e}", "ERROR")
    
    def update_service_status(self, service_name, status, pid):
        """Actualizar estado de servicio en la UI"""
        self.services[service_name]["status"] = status
        self.services[service_name]["pid"] = pid
        
        if service_name in self.service_widgets:
            widgets = self.service_widgets[service_name]
            
            if status == "running":
                widgets["status"].config(text="Running", foreground="green")
                widgets["pid"].config(text=str(pid) if pid else "N/A")
                widgets["start"].config(state="disabled")
                widgets["stop"].config(state="normal")
            else:
                widgets["status"].config(text="Stopped", foreground="red")
                widgets["pid"].config(text="N/A")
                widgets["start"].config(state="normal")
                widgets["stop"].config(state="disabled")
    
    def start_all_services(self):
        """Iniciar todos los servicios"""
        self.log_message("Iniciando todos los servicios...", "INFO")
        
        # Secuencia de inicio
        services_order = ["ollama", "hybrid_system", "whatsapp", "dashboard"]
        
        for service_name in services_order:
            self.start_service(service_name)
            time.sleep(2)
        
        self.log_message("Todos los servicios iniciados", "SUCCESS")
    
    def stop_all_services(self):
        """Detener todos los servicios"""
        self.log_message("Deteniendo todos los servicios...", "INFO")
        
        services_order = ["dashboard", "whatsapp", "hybrid_system", "ollama"]
        
        for service_name in services_order:
            self.stop_service(service_name)
            time.sleep(1)
        
        self.log_message("Todos los servicios detenidos", "SUCCESS")
    
    def restart_all_services(self):
        """Reiniciar todos los servicios"""
        self.log_message("Reiniciando todos los servicios...", "INFO")
        self.stop_all_services()
        time.sleep(3)
        self.start_all_services()
    
    def show_status(self):
        """Mostrar estado completo del sistema"""
        status_text = "ESTADO COMPLETO DEL SISTEMA\n"
        status_text += "=" * 50 + "\n\n"
        
        for service_name, service_info in self.services.items():
            status_text += f"{service_info['name']}\n"
            status_text += f"   Estado: {service_info['status']}\n"
            status_text += f"   Puerto: {service_info['port'] or 'N/A'}\n"
            status_text += f"   PID: {service_info['pid'] or 'N/A'}\n\n"
        
        messagebox.showinfo("Estado del Sistema", status_text)
    
    def open_endpoints(self):
        """Abrir endpoints disponibles"""
        endpoints = []
        
        if self.services["ollama"]["status"] == "running":
            endpoints.append("http://localhost:11434")
        
        if self.services["dashboard"]["status"] == "running":
            endpoints.append("http://localhost:4173")
        
        if self.services["cloud_architecture"]["status"] == "running":
            endpoints.append("http://localhost:8000")
        
        if endpoints:
            endpoint_text = "ENDPOINTS DISPONIBLES\n\n"
            for i, endpoint in enumerate(endpoints, 1):
                endpoint_text += f"{i}. {endpoint}\n"
            
            messagebox.showinfo("Endpoints", endpoint_text)
        else:
            messagebox.showwarning("Endpoints", "No hay endpoints activos")
    
    def start_monitoring(self):
        """Iniciar monitoreo automático de servicios"""
        def monitor():
            while self.is_monitoring:
                try:
                    # Verificar Ollama
                    if self.services["ollama"]["status"] == "running":
                        try:
                            import urllib.request
                            response = urllib.request.urlopen('http://localhost:11434/api/tags', timeout=2)
                            if response.getcode() != 200:
                                self.update_service_status("ollama", "stopped", None)
                                self.log_message("Ollama dejo de responder", "WARNING")
                        except:
                            self.update_service_status("ollama", "stopped", None)
                            self.log_message("Ollama dejo de responder", "WARNING")
                    
                    # Verificar PIDs
                    for service_name, service_info in self.services.items():
                        if service_info["pid"]:
                            try:
                                process = psutil.Process(service_info["pid"])
                                if not process.is_running():
                                    self.update_service_status(service_name, "stopped", None)
                                    self.log_message(f"{service_name} se detuvo inesperadamente", "WARNING")
                            except:
                                self.update_service_status(service_name, "stopped", None)
                    
                    time.sleep(10)  # Monitorear cada 10 segundos
                    
                except Exception as e:
                    self.log_message(f"Error en monitoreo: {e}", "ERROR")
                    time.sleep(5)
        
        self.is_monitoring = True
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def run(self):
        """Ejecutar aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Manejar cierre de aplicación"""
        if messagebox.askokcancel("Salir", "¿Detener todos los servicios y salir?"):
            self.is_monitoring = False
            self.stop_all_services()
            self.root.destroy()

def main():
    """Función principal"""
    try:
        app = RAULIServiceManager()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el gestor: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
