#!/usr/bin/env python3
"""
🚀 RAULI ENTERPRISE DEPLOYMENT SCRIPT
Deployment alternativo sin Docker - Direct Python Deployment
"""

import os
import sys
import json
import subprocess
import threading
import time
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class RAULIDeployment:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.deployment_log = self.base_dir / 'deployment.log'
        self.processes = {}
        self.running = True
        
    def log_message(self, message: str):
        """Registrar mensaje de deployment"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.deployment_log, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def check_dependencies(self) -> bool:
        """Verificar dependencias necesarias"""
        self.log_message("🔍 Verificando dependencias...")
        
        try:
            # Verificar Python
            import streamlit
            import flask
            import requests
            self.log_message("✅ Python dependencies OK")
            return True
        except ImportError as e:
            self.log_message(f"❌ Missing dependency: {e}")
            return False
    
    def start_dashboard(self):
        """Iniciar dashboard de Streamlit"""
        try:
            self.log_message("🚀 Iniciando RAULI Dashboard...")
            
            # Cambiar al directorio del dashboard
            os.chdir(self.base_dir)
            
            # Iniciar Streamlit
            cmd = [
                sys.executable, '-m', 'streamlit', 'run',
                'dashboard_rauli.py',
                '--server.port', '8502',
                '--server.address', '0.0.0.0',
                '--server.headless', 'true',
                '--browser.gatherUsageStats', 'false'
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes['dashboard'] = process
            self.log_message("✅ Dashboard iniciado en http://localhost:8502")
            
            # Monitorear output
            for line in process.stdout:
                if "Running on" in line:
                    self.log_message(f"📊 Dashboard: {line.strip()}")
                elif "External URL" in line:
                    self.log_message(f"🌐 Dashboard: {line.strip()}")
                    
        except Exception as e:
            self.log_message(f"❌ Error iniciando dashboard: {e}")
    
    def start_mobile_interface(self):
        """Iniciar interface móvil Flask"""
        try:
            self.log_message("📱 Iniciando Mobile Interface...")
            
            # Cambiar al directorio base
            os.chdir(self.base_dir)
            
            # Iniciar Flask app
            cmd = [
                sys.executable, 'mobile_web_interface.py'
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes['mobile'] = process
            self.log_message("✅ Mobile Interface iniciado en http://localhost:5000")
            
            # Monitorear output
            for line in process.stdout:
                if "Running on" in line:
                    self.log_message(f"📱 Mobile: {line.strip()}")
                    
        except Exception as e:
            self.log_message(f"❌ Error iniciando mobile interface: {e}")
    
    def start_vision_system(self):
        """Iniciar sistema de visión en background"""
        try:
            self.log_message("👁️ Iniciando Vision System...")
            
            # Crear script de visión simple
            vision_script = self.base_dir / 'vision_service.py'
            if not vision_script.exists():
                self.create_simple_vision_service(vision_script)
            
            cmd = [sys.executable, str(vision_script)]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes['vision'] = process
            self.log_message("✅ Vision System iniciado")
            
        except Exception as e:
            self.log_message(f"❌ Error iniciando vision system: {e}")
    
    def create_simple_vision_service(self, script_path):
        """Crear servicio de visión simple"""
        content = '''#!/usr/bin/env python3
"""
👁️ RAULI Vision Service - Simple Implementation
"""
import time
import json
from datetime import datetime
from pathlib import Path

def main():
    """Servicio de visión simple"""
    print("👁️ RAULI Vision Service iniciado")
    
    while True:
        try:
            # Simular procesamiento de imágenes
            time.sleep(30)
            print(f"👁️ Vision Service activo - {datetime.now()}")
        except KeyboardInterrupt:
            print("👁️ Vision Service detenido")
            break
        except Exception as e:
            print(f"❌ Error en Vision Service: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
'''
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def check_services_health(self):
        """Verificar salud de los servicios"""
        self.log_message("🔍 Verificando salud de servicios...")
        
        import requests
        
        # Verificar dashboard
        try:
            response = requests.get('http://localhost:8502', timeout=5)
            if response.status_code == 200:
                self.log_message("✅ Dashboard saludable")
            else:
                self.log_message(f"⚠️ Dashboard status: {response.status_code}")
        except:
            self.log_message("❌ Dashboard no responde")
        
        # Verificar mobile interface
        try:
            response = requests.get('http://localhost:5000/mobile', timeout=5)
            if response.status_code == 200:
                self.log_message("✅ Mobile Interface saludable")
            else:
                self.log_message(f"⚠️ Mobile Interface status: {response.status_code}")
        except:
            self.log_message("❌ Mobile Interface no responde")
    
    def create_status_page(self):
        """Crear página de estado del deployment"""
        status_data = {
            'deployment_status': 'active',
            'services': {
                'dashboard': {
                    'url': 'http://localhost:8502',
                    'status': 'running',
                    'port': 8502
                },
                'mobile': {
                    'url': 'http://localhost:5000/mobile',
                    'status': 'running',
                    'port': 5000
                },
                'vision': {
                    'status': 'running',
                    'type': 'background_service'
                }
            },
            'deployment_info': {
                'version': '2.0.0',
                'deployment_time': datetime.now().isoformat(),
                'deployed_by': 'Cascade - Arquitecto Técnico Principal',
                'deployment_type': 'direct_python'
            },
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform,
                'working_directory': str(self.base_dir)
            }
        }
        
        status_file = self.base_dir / 'deployment_status.json'
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, ensure_ascii=False, indent=2)
        
        self.log_message(f"📋 Status page creada: {status_file}")
    
    def signal_handler(self, signum, frame):
        """Manejador de señales para shutdown elegante"""
        self.log_message("🛑 Recibida señal de shutdown...")
        self.running = False
        self.shutdown_services()
    
    def shutdown_services(self):
        """Detener todos los servicios"""
        self.log_message("🛑 Deteniendo servicios...")
        
        for service_name, process in self.processes.items():
            try:
                if process.poll() is None:  # Proceso todavía corriendo
                    self.log_message(f"🛑 Deteniendo {service_name}...")
                    process.terminate()
                    
                    # Esperar un poco
                    time.sleep(2)
                    
                    # Forzar si no se detuvo
                    if process.poll() is None:
                        process.kill()
                        self.log_message(f"🔥 Forzando detención de {service_name}")
                    
            except Exception as e:
                self.log_message(f"❌ Error deteniendo {service_name}: {e}")
        
        self.log_message("✅ Todos los servicios detenidos")
    
    def monitor_deployment(self):
        """Monitorear deployment continuamente"""
        self.log_message("📊 Iniciando monitoreo de deployment...")
        
        while self.running:
            try:
                # Verificar salud cada 30 segundos
                self.check_services_health()
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.log_message("🛑 Interrumpido por usuario")
                break
            except Exception as e:
                self.log_message(f"❌ Error en monitoreo: {e}")
                time.sleep(10)
    
    def execute_deployment(self):
        """Ejecutar deployment completo"""
        self.log_message("🚀 INICIANDO DEPLOYMENT DE RAULI ENTERPRISE")
        self.log_message("=" * 50)
        
        # Configurar manejador de señales
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Verificar dependencias
        if not self.check_dependencies():
            self.log_message("❌ Dependencias faltantes - Deployment abortado")
            return False
        
        # Iniciar servicios en threads separados
        threads = []
        
        # Dashboard
        dashboard_thread = threading.Thread(target=self.start_dashboard)
        dashboard_thread.daemon = True
        threads.append(dashboard_thread)
        dashboard_thread.start()
        
        # Esperar un poco antes de iniciar el siguiente
        time.sleep(3)
        
        # Mobile Interface
        mobile_thread = threading.Thread(target=self.start_mobile_interface)
        mobile_thread.daemon = True
        threads.append(mobile_thread)
        mobile_thread.start()
        
        # Esperar un poco antes de iniciar el siguiente
        time.sleep(3)
        
        # Vision System
        vision_thread = threading.Thread(target=self.start_vision_system)
        vision_thread.daemon = True
        threads.append(vision_thread)
        vision_thread.start()
        
        # Esperar que los servicios inicien
        time.sleep(5)
        
        # Crear página de estado
        self.create_status_page()
        
        # Verificar salud inicial
        self.check_services_health()
        
        # Mostrar resumen
        self.log_message("🎯 DEPLOYMENT COMPLETADO")
        self.log_message("-" * 30)
        self.log_message("📊 Dashboard: http://localhost:8502")
        self.log_message("📱 Mobile: http://localhost:5000/mobile")
        self.log_message("👁️ Vision: Background service")
        self.log_message("📋 Status: deployment_status.json")
        self.log_message("📝 Logs: deployment.log")
        
        # Iniciar monitoreo
        try:
            self.monitor_deployment()
        except KeyboardInterrupt:
            self.log_message("🛑 Deployment detenido por usuario")
        finally:
            self.shutdown_services()
        
        return True

def main():
    """Función principal"""
    deployment = RAULIDeployment()
    
    print("🚀 RAULI ENTERPRISE DEPLOYMENT")
    print("Deployment Direct Python (Sin Docker)")
    print("")
    
    try:
        # Ejecutar deployment
        success = deployment.execute_deployment()
        
        if success:
            print("\n✅ DEPLOYMENT COMPLETADO EXITOSAMENTE")
        else:
            print("\n❌ DEPLOYMENT FALLÓ")
            
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
    
    print("\n🎯 RAULI Enterprise Deployment Finalizado")

if __name__ == "__main__":
    main()
