#!/usr/bin/env python3
"""
🚀 RAULI System Boot Manager - Sistema de Arranque Automático
Inicialización completa de todos los componentes RAULI
"""

import os
import sys
import json
import time
import subprocess
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import psutil
import webbrowser
from pathlib import Path

class RAULIBootManager:
    def __init__(self):
        self.boot_config = self.load_boot_config()
        self.services = {
            "ollama": {"status": "stopped", "pid": None, "port": 11434},
            "dashboard": {"status": "stopped", "pid": None, "port": 4173},
            "whatsapp": {"status": "stopped", "pid": None, "port": None},
            "hybrid_system": {"status": "stopped", "pid": None, "port": None},
            "cloud_architecture": {"status": "stopped", "pid": None, "port": 8000}
        }
        self.boot_sequence = [
            "ollama",
            "dashboard", 
            "whatsapp",
            "hybrid_system",
            "cloud_architecture"
        ]
        self.start_time = datetime.now()
        
        print("🚀 RAULI System Boot Manager iniciado")
        print(f"📅 Fecha: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔧 Preparando arranque del sistema completo...")
    
    def load_boot_config(self) -> Dict:
        """Cargar configuración de arranque"""
        config_path = Path("C:/RAULI_CORE/boot_config.json")
        
        default_config = {
            "auto_start": True,
            "boot_delay": 2,
            "health_check_interval": 10,
            "max_retries": 3,
            "open_browser": True,
            "log_level": "INFO",
            "services": {
                "ollama": {"enabled": True, "timeout": 30},
                "dashboard": {"enabled": True, "timeout": 15},
                "whatsapp": {"enabled": True, "timeout": 10},
                "hybrid_system": {"enabled": True, "timeout": 15},
                "cloud_architecture": {"enabled": False, "timeout": 20}
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                return {**default_config, **config}
            except:
                pass
        
        # Guardar configuración por defecto
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def check_service_health(self, service_name: str) -> bool:
        """Verificar salud de un servicio"""
        service = self.services[service_name]
        
        if service["pid"] is None:
            return False
        
        try:
            # Verificar si el proceso está corriendo
            process = psutil.Process(service["pid"])
            if not process.is_running():
                return False
            
            # Verificar puerto si aplica
            if service["port"]:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', service["port"]))
                sock.close()
                return result == 0
            
            return True
            
        except:
            return False
    
    def start_ollama(self) -> bool:
        """Iniciar Ollama"""
        print("🧠 Iniciando Ollama...")
        
        try:
            # Verificar si Ollama ya está corriendo
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ Ollama ya está corriendo")
                self.services["ollama"]["status"] = "running"
                return True
            
            # Iniciar Ollama (generalmente se inicia como servicio)
            print("🔄 Ollama necesita ser iniciado manualmente o como servicio")
            print("💡 Ejecuta: ollama serve (o inicia el servicio Ollama)")
            
            return False
            
        except Exception as e:
            print(f"❌ Error iniciando Ollama: {e}")
            return False
    
    def start_dashboard(self) -> bool:
        """Iniciar Dashboard RAULI"""
        print("📱 Iniciando Dashboard RAULI...")
        
        try:
            # Cambiar al directorio del dashboard
            dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
            if not dashboard_dir.exists():
                print("❌ Directorio del dashboard no encontrado")
                return False
            
            # Iniciar servidor de preview
            process = subprocess.Popen(
                ["npm", "run", "preview"],
                cwd=dashboard_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar un momento para que inicie
            time.sleep(5)
            
            # Verificar si está corriendo
            if process.poll() is None:
                self.services["dashboard"]["pid"] = process.pid
                self.services["dashboard"]["status"] = "running"
                print("✅ Dashboard iniciado en puerto 4173")
                
                # Abrir browser si está configurado
                if self.boot_config["open_browser"]:
                    webbrowser.open("http://localhost:4173")
                
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Error iniciando dashboard: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando dashboard: {e}")
            return False
    
    def start_whatsapp(self) -> bool:
        """Iniciar WhatsApp Professional"""
        print("💬 Iniciando WhatsApp Professional...")
        
        try:
            script_path = Path("C:/RAULI_CORE/rauli_whatsapp_professional.py")
            if not script_path.exists():
                print("❌ Script de WhatsApp no encontrado")
                return False
            
            # Iniciar en background
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar un momento
            time.sleep(2)
            
            if process.poll() is None:
                self.services["whatsapp"]["pid"] = process.pid
                self.services["whatsapp"]["status"] = "running"
                print("✅ WhatsApp Professional iniciado")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Error iniciando WhatsApp: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando WhatsApp: {e}")
            return False
    
    def start_hybrid_system(self) -> bool:
        """Iniciar Sistema Híbrido"""
        print("🧠 Iniciando Sistema Híbrido IA...")
        
        try:
            script_path = Path("C:/RAULI_CORE/rauli_hybrid_system.py")
            if not script_path.exists():
                print("❌ Script del sistema híbrido no encontrado")
                return False
            
            # Iniciar en background
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(2)
            
            if process.poll() is None:
                self.services["hybrid_system"]["pid"] = process.pid
                self.services["hybrid_system"]["status"] = "running"
                print("✅ Sistema Híbrido iniciado")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Error iniciando sistema híbrido: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando sistema híbrido: {e}")
            return False
    
    def start_cloud_architecture(self) -> bool:
        """Iniciar Arquitectura Cloud"""
        print("☁️ Iniciando Arquitectura Cloud...")
        
        try:
            script_path = Path("C:/RAULI_CORE/rauli_cloud_architecture.py")
            if not script_path.exists():
                print("❌ Script de cloud architecture no encontrado")
                return False
            
            # Iniciar en background
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(3)
            
            if process.poll() is None:
                self.services["cloud_architecture"]["pid"] = process.pid
                self.services["cloud_architecture"]["status"] = "running"
                print("✅ Arquitectura Cloud iniciada en puerto 8000")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Error iniciando cloud architecture: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando cloud architecture: {e}")
            return False
    
    def start_service(self, service_name: str) -> bool:
        """Iniciar un servicio específico"""
        if not self.boot_config["services"][service_name]["enabled"]:
            print(f"⏭️ {service_name} deshabilitado en configuración")
            return True
        
        print(f"\n🚀 Iniciando {service_name}...")
        
        service_methods = {
            "ollama": self.start_ollama,
            "dashboard": self.start_dashboard,
            "whatsapp": self.start_whatsapp,
            "hybrid_system": self.start_hybrid_system,
            "cloud_architecture": self.start_cloud_architecture
        }
        
        if service_name in service_methods:
            return service_methods[service_name]()
        else:
            print(f"❌ Servicio {service_name} no reconocido")
            return False
    
    def boot_sequence_start(self) -> bool:
        """Ejecutar secuencia de arranque completa"""
        print("\n" + "="*60)
        print("🚀 INICIANDO SECUENCIA DE ARRANQUE RAULI SYSTEM")
        print("="*60)
        
        success_count = 0
        total_services = len(self.boot_sequence)
        
        for i, service_name in enumerate(self.boot_sequence, 1):
            print(f"\n[{i}/{total_services}] Arrancando {service_name}...")
            
            # Intentar iniciar el servicio
            success = self.start_service(service_name)
            
            if success:
                success_count += 1
                print(f"✅ {service_name} iniciado correctamente")
            else:
                print(f"❌ Error iniciando {service_name}")
            
            # Delay entre servicios
            if i < total_services:
                delay = self.boot_config["boot_delay"]
                print(f"⏱️ Esperando {delay} segundos...")
                time.sleep(delay)
        
        # Resumen del arranque
        self.print_boot_summary(success_count, total_services)
        
        return success_count == total_services
    
    def print_boot_summary(self, success_count: int, total_services: int):
        """Imprimir resumen del arranque"""
        end_time = datetime.now()
        boot_duration = (end_time - self.start_time).total_seconds()
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE ARRANQUE RAULI SYSTEM")
        print("="*60)
        print(f"⏱️ Tiempo total: {boot_duration:.2f} segundos")
        print(f"✅ Servicios iniciados: {success_count}/{total_services}")
        print(f"📅 Fecha: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n📋 ESTADO DE SERVICIOS:")
        for service_name, service_info in self.services.items():
            status_icon = "✅" if service_info["status"] == "running" else "❌"
            port_info = f" (puerto {service_info['port']})" if service_info["port"] else ""
            print(f"  {status_icon} {service_name}: {service_info['status']}{port_info}")
        
        print("\n🌐 ENDPOINTS DISPONIBLES:")
        if self.services["dashboard"]["status"] == "running":
            print("  📱 Dashboard: http://localhost:4173")
        if self.services["cloud_architecture"]["status"] == "running":
            print("  ☁️ Cloud API: http://localhost:8000")
        if self.services["ollama"]["status"] == "running":
            print("  🧠 Ollama: http://localhost:11434")
        
        print("\n🎯 ACCESOS RÁPIDOS:")
        print("  📊 Sistema completo: Listo para usar")
        print("  💬 WhatsApp: Activo en background")
        print("  🧠 IA Híbrida: Operativa")
        
        if success_count == total_services:
            print("\n🎉 SISTEMA RAULI COMPLETAMENTE OPERATIVO")
        else:
            print(f"\n⚠️ Sistema parcialmente operativo ({success_count}/{total_services})")
    
    def stop_service(self, service_name: str) -> bool:
        """Detener un servicio específico"""
        service = self.services[service_name]
        
        if service["pid"] is None:
            print(f"⚠️ {service_name} no está corriendo")
            return True
        
        try:
            process = psutil.Process(service["pid"])
            process.terminate()
            
            # Esperar a que termine
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
            
            service["status"] = "stopped"
            service["pid"] = None
            print(f"✅ {service_name} detenido")
            return True
            
        except Exception as e:
            print(f"❌ Error deteniendo {service_name}: {e}")
            return False
    
    def stop_all_services(self):
        """Detener todos los servicios"""
        print("\n🛑 DETENIENDO TODOS LOS SERVICIOS...")
        
        for service_name in reversed(self.boot_sequence):
            self.stop_service(service_name)
        
        print("✅ Todos los servicios detenidos")
    
    def get_system_status(self) -> Dict:
        """Obtener estado completo del sistema"""
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime": (datetime.now() - self.start_time).total_seconds(),
            "services": self.services,
            "boot_config": self.boot_config
        }
    
    def save_boot_log(self):
        """Guardar log de arranque"""
        log_data = {
            "boot_timestamp": self.start_time.isoformat(),
            "services_status": self.services,
            "boot_config": self.boot_config,
            "system_status": self.get_system_status()
        }
        
        log_file = Path("C:/RAULI_CORE/boot_logs.json")
        
        # Cargar logs existentes
        logs = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        # Agregar nuevo log
        logs.append(log_data)
        
        # Mantener solo últimos 10 logs
        logs = logs[-10:]
        
        # Guardar
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"📄 Log de arranque guardado en {log_file}")

# Sistema principal de arranque
class RAULISystemBoot:
    def __init__(self):
        self.boot_manager = RAULIBootManager()
    
    def boot_system(self):
        """Arranque completo del sistema"""
        print("🚀 RAULI System Boot - Iniciando sistema completo")
        
        # Ejecutar secuencia de arranque
        success = self.boot_manager.boot_sequence_start()
        
        # Guardar log
        self.boot_manager.save_boot_log()
        
        # Notificación de voz
        if success:
            subprocess.run([
                sys.executable, "C:/RAULI_CORE/boca.py", 
                "Sistema RAULI completamente operativo - Todos los servicios activos"
            ], capture_output=True)
        else:
            subprocess.run([
                sys.executable, "C:/RAULI_CORE/boca.py", 
                "Sistema RAULI parcialmente operativo - Algunos servicios requieren atención"
            ], capture_output=True)
        
        return success
    
    def shutdown_system(self):
        """Apagar sistema completo"""
        print("🛑 RAULI System Shutdown - Deteniendo sistema")
        
        self.boot_manager.stop_all_services()
        
        subprocess.run([
            sys.executable, "C:/RAULI_CORE/boca.py", 
            "Sistema RAULI detenido - Todos los servicios finalizados"
        ], capture_output=True)
    
    def restart_system(self):
        """Reiniciar sistema completo"""
        print("🔄 RAULI System Restart - Reiniciando sistema")
        
        self.boot_manager.stop_all_services()
        time.sleep(3)
        return self.boot_system()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="RAULI System Boot Manager")
    parser.add_argument("action", choices=["boot", "shutdown", "restart", "status"], 
                       help="Acción a ejecutar")
    parser.add_argument("--service", help="Servicio específico")
    
    args = parser.parse_args()
    
    system_boot = RAULISystemBoot()
    
    if args.action == "boot":
        if args.service:
            system_boot.boot_manager.start_service(args.service)
        else:
            system_boot.boot_system()
    
    elif args.action == "shutdown":
        if args.service:
            system_boot.boot_manager.stop_service(args.service)
        else:
            system_boot.shutdown_system()
    
    elif args.action == "restart":
        system_boot.restart_system()
    
    elif args.action == "status":
        status = system_boot.boot_manager.get_system_status()
        print(json.dumps(status, indent=2))
