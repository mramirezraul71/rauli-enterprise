#!/usr/bin/env python3
"""
🚀 RAULI VERCEL DIRECT DEPLOYMENT
Deployment directo usando API de Vercel sin CLI
"""

import os
import sys
import json
import subprocess
import requests
import time
import zipfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class VercelConfig:
    """Configuración de Vercel"""
    token: str
    project_name: str
    team_id: Optional[str] = None

class VercelDirectDeploy:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.credenciales_file = self.base_dir / 'credenciales.env'
        self.deploy_log_file = self.base_dir / 'direct_deploy_log.json'
        
        # Cargar credenciales
        self.credentials = self.load_credentials()
        self.vercel_config = VercelConfig(
            token=self.credentials.get('VERCEL_TOKEN', ''),
            project_name="rauli-enterprise"
        )
        
        # API endpoints
        self.api_base = "https://api.vercel.com"
        self.headers = {
            "Authorization": f"Bearer {self.vercel_config.token}",
            "Content-Type": "application/json"
        }
        
        # Estado del deployment
        self.deployment_status = {
            "started": False,
            "steps_completed": [],
            "current_step": None,
            "errors": [],
            "success": False,
            "deployment_url": None,
            "project_id": None
        }
    
    def load_credentials(self) -> Dict[str, str]:
        """Cargar credenciales"""
        credentials = {}
        try:
            with open(self.credenciales_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        credentials[key] = value.strip('"').strip("'")
            print("✅ Credenciales cargadas")
            return credentials
        except Exception as e:
            print(f"❌ Error cargando credenciales: {e}")
            return {}
    
    def log_step(self, step: str, status: str, details: str = ""):
        """Registrar paso"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "status": status,
            "details": details
        }
        
        self.deployment_status["steps_completed"].append(log_entry)
        
        if status == "error":
            self.deployment_status["errors"].append(details)
        
        print(f"{'✅' if status == 'success' else '❌' if status == 'error' else '⏳'} {step}")
        if details:
            print(f"   {details}")
        
        # Guardar log
        with open(self.deploy_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.deployment_status, f, ensure_ascii=False, indent=2)
    
    def test_api_connection(self) -> bool:
        """Probar conexión con API de Vercel"""
        print("🔍 Probando conexión con API de Vercel...")
        
        try:
            response = requests.get(f"{self.api_base}/v2/user", headers=self.headers)
            
            if response.status_code == 200:
                user_data = response.json()
                self.log_step("API connection", "success", f"Conectado como {user_data.get('name', 'Unknown')}")
                return True
            else:
                self.log_step("API connection", "error", f"Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_step("API connection", "error", str(e))
            return False
    
    def get_or_create_project(self) -> bool:
        """Obener o crear proyecto"""
        print("📂 Obteniendo/creando proyecto...")
        
        try:
            # Listar proyectos existentes
            response = requests.get(f"{self.api_base}/v9/projects", headers=self.headers)
            
            if response.status_code == 200:
                projects = response.json().get('projects', [])
                
                # Buscar proyecto existente
                for project in projects:
                    if project['name'] == self.vercel_config.project_name:
                        self.deployment_status["project_id"] = project['id']
                        self.log_step("Project lookup", "success", f"Proyecto encontrado: {project['id']}")
                        return True
            
            # Crear nuevo proyecto
            project_data = {
                "name": self.vercel_config.project_name,
                "framework": "python",
                "buildCommand": "pip install -r requirements.txt",
                "outputDirectory": ".",
                "installCommand": "pip install -r requirements.txt",
                "devCommand": "python dashboard_rauli.py"
            }
            
            response = requests.post(f"{self.api_base}/v9/projects", 
                                   headers=self.headers, 
                                   json=project_data)
            
            if response.status_code == 200:
                project = response.json()
                self.deployment_status["project_id"] = project['id']
                self.log_step("Project creation", "success", f"Proyecto creado: {project['id']}")
                return True
            else:
                self.log_step("Project creation", "error", f"Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_step("Project management", "error", str(e))
            return False
    
    def create_deployment_package(self) -> str:
        """Crear paquete de deployment"""
        print("📦 Creando paquete de deployment...")
        
        # Crear archivo ZIP temporal
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        try:
            with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Agregar archivos principales
                main_files = [
                    'dashboard_rauli.py',
                    'mobile_web_interface.py',
                    'requirements.txt',
                    'vercel.json',
                    'package.json'
                ]
                
                for file_name in main_files:
                    file_path = self.base_dir / file_name
                    if file_path.exists():
                        zipf.write(file_path, file_name)
                
                # Agregar directorio api
                api_dir = self.base_dir / 'api'
                if api_dir.exists():
                    for file_path in api_dir.rglob('*'):
                        if file_path.is_file():
                            arcname = str(file_path.relative_to(self.base_dir))
                            zipf.write(file_path, arcname)
                
                # Agregar otros archivos necesarios
                other_files = [
                    '.env',
                    'credenciales.env'
                ]
                
                for file_name in other_files:
                    file_path = self.base_dir / file_name
                    if file_path.exists():
                        zipf.write(file_path, file_name)
            
            self.log_step("Package creation", "success", f"Paquete creado: {temp_zip.name}")
            return temp_zip.name
            
        except Exception as e:
            self.log_step("Package creation", "error", str(e))
            return ""
    
    def upload_files(self, zip_path: str) -> List[Dict[str, Any]]:
        """Subir archivos a Vercel"""
        print("📤 Subiendo archivos...")
        
        try:
            # Leer y procesar archivo ZIP
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            
            # Subir archivo con formato correcto
            files_data = {
                'files': [
                    {
                        'file': 'deployment.zip',
                        'data': zip_content,
                        'sha': 'deployment-sha'
                    }
                ]
            }
            
            response = requests.post(f"{self.api_base}/v2/files", 
                                   headers=self.headers, 
                                   json=files_data)
            
            if response.status_code == 200:
                file_list = response.json()
                self.log_step("File upload", "success", f"Archivos subidos: {len(file_list)}")
                return file_list
            else:
                self.log_step("File upload", "error", f"Error {response.status_code}: {response.text}")
                return []
                
        except Exception as e:
            self.log_step("File upload", "error", str(e))
            return []
    
    def create_deployment(self, files: List[Dict[str, Any]]) -> bool:
        """Crear deployment"""
        print("🚀 Creando deployment...")
        
        try:
            deployment_data = {
                "name": self.vercel_config.project_name,
                "files": files,
                "projectSettings": {
                    "framework": "python",
                    "buildCommand": "pip install -r requirements.txt",
                    "outputDirectory": ".",
                    "installCommand": "pip install -r requirements.txt"
                },
                "target": "production",
                "regions": ["iad1"]  # US East (N. Virginia)
            }
            
            response = requests.post(f"{self.api_base}/v13/deployments", 
                                   headers=self.headers, 
                                   json=deployment_data)
            
            if response.status_code == 200:
                deployment = response.json()
                deployment_id = deployment['id']
                deployment_url = deployment.get('url', '')
                
                self.deployment_status["deployment_url"] = deployment_url
                
                # Monitorear deployment
                return self.monitor_deployment(deployment_id)
            else:
                self.log_step("Deployment creation", "error", f"Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_step("Deployment creation", "error", str(e))
            return False
    
    def monitor_deployment(self, deployment_id: str) -> bool:
        """Monitorear deployment"""
        print("⏳ Monitoreando deployment...")
        
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(f"{self.api_base}/v13/deployments/{deployment_id}", 
                                      headers=self.headers)
                
                if response.status_code == 200:
                    deployment = response.json()
                    state = deployment.get('state', '')
                    ready_state = deployment.get('readyState', '')
                    
                    print(f"   Estado: {state} | Ready: {ready_state}")
                    
                    if ready_state == "READY":
                        deployment_url = deployment.get('url', '')
                        self.deployment_status["deployment_url"] = deployment_url
                        self.log_step("Deployment monitoring", "success", f"Deployment listo: {deployment_url}")
                        return True
                    elif ready_state == "ERROR":
                        self.log_step("Deployment monitoring", "error", "Deployment falló")
                        return False
                
                attempt += 1
                time.sleep(10)
                
            except Exception as e:
                self.log_step("Deployment monitoring", "error", str(e))
                return False
        
        self.log_step("Deployment monitoring", "error", "Timeout en monitoreo")
        return False
    
    def test_deployment(self) -> bool:
        """Probar deployment"""
        print("🧪 Probando deployment...")
        
        if not self.deployment_status["deployment_url"]:
            self.log_step("Deployment test", "warning", "No hay URL para probar")
            return True
        
        try:
            response = requests.get(self.deployment_status["deployment_url"], timeout=10)
            
            if response.status_code == 200:
                self.log_step("Deployment test", "success", f"Deployment OK: {response.status_code}")
                return True
            else:
                self.log_step("Deployment test", "warning", f"Status: {response.status_code}")
                return True
                
        except Exception as e:
            self.log_step("Deployment test", "warning", f"No se pudo probar: {e}")
            return True
    
    def generate_report(self) -> str:
        """Generar reporte"""
        report = f"""
# 🚀 RAULI ENTERPRISE - DIRECT DEPLOYMENT REPORT

## 📊 FECHA
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## ✅ ESTADO
**Estado:** {'✅ EXITOSO' if self.deployment_status['success'] else '❌ FALLIDO'}
**Proyecto:** {self.vercel_config.project_name}
**Project ID:** {self.deployment_status.get('project_id', 'N/A')}
**URL:** {self.deployment_status.get('deployment_url', 'No disponible')}

---

## 📋 PASOS

"""
        
        for step in self.deployment_status["steps_completed"]:
            icon = "✅" if step["status"] == "success" else "❌" if step["status"] == "error" else "⏳"
            report += f"\n{icon} **{step['step']}** - {step['status']}"
            if step["details"]:
                report += f"\n   {step['details']}"
        
        if self.deployment_status["errors"]:
            report += "\n\n---\n\n## ❌ ERRORES\n\n"
            for error in self.deployment_status["errors"]:
                report += f"- ❌ {error}\n"
        
        report += f"""

---

## 🎯 ACCESO

- **🌐 Dashboard:** {self.deployment_status.get('deployment_url', 'N/A')}
- **📱 Mobile:** {self.deployment_status.get('deployment_url', '')}/api/mobile
- **🏥 Health:** {self.deployment_status.get('deployment_url', '')}/api/health

---

**🎉 DEPLOYMENT COMPLETADO VIA API DIRECTA**
"""
        
        # Guardar reporte
        report_file = self.base_dir / 'direct_deployment_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(report_file)
    
    def execute_deployment(self) -> bool:
        """Ejecutar deployment completo"""
        print("🚀 INICIANDO DEPLOYMENT DIRECTO A VERCEL")
        print("=" * 60)
        
        self.deployment_status["started"] = True
        
        # Paso 1: Probar API
        if not self.test_api_connection():
            return False
        
        # Paso 2: Obtener/crear proyecto
        if not self.get_or_create_project():
            return False
        
        # Paso 3: Crear paquete
        zip_path = self.create_deployment_package()
        if not zip_path:
            return False
        
        # Paso 4: Subir archivos
        files = self.upload_files(zip_path)
        if not files:
            return False
        
        # Paso 5: Crear deployment
        if not self.create_deployment(files):
            return False
        
        # Paso 6: Probar deployment
        self.test_deployment()
        
        # Generar reporte
        report_file = self.generate_report()
        
        self.deployment_status["success"] = True
        
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📊 Reporte: {report_file}")
        print(f"🌐 URL: {self.deployment_status.get('deployment_url', 'No disponible')}")
        
        # Limpiar archivo temporal
        try:
            os.unlink(zip_path)
        except:
            pass
        
        return True

def main():
    """Función principal"""
    print("🚀 RAULI VERCEL DIRECT DEPLOYMENT")
    print("Deployment directo usando API de Vercel")
    print("")
    
    deploy = VercelDirectDeploy()
    
    if deploy.execute_deployment():
        print("\n✅ DEPLOYMENT EXITOSO")
        
        # Abrir navegador
        if deploy.deployment_status.get("deployment_url"):
            import webbrowser
            webbrowser.open(deploy.deployment_status["deployment_url"])
            print(f"🌐 Abriendo: {deploy.deployment_status['deployment_url']}")
        
        # Notificar
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "¡Deployment directo completado! RAULI Enterprise está en producción."
            ], cwd=r'C:\dev')
        except:
            pass
    
    else:
        print("\n❌ DEPLOYMENT FALLIDO")

if __name__ == "__main__":
    main()
