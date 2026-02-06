#!/usr/bin/env python3
"""
🚀 RAULI VERCEL SIMPLE DEPLOYMENT
Deployment simple usando GitHub + Vercel integration
"""

import os
import sys
import json
import subprocess
import requests
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import base64

@dataclass
class SimpleDeployConfig:
    """Configuración simple"""
    github_token: str
    vercel_token: str
    repo_name: str = "rauli-enterprise"
    project_name: str = "rauli-enterprise"

class VercelSimpleDeploy:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.credenciales_file = self.base_dir / 'credenciales.env'
        self.deploy_log_file = self.base_dir / 'simple_deploy_log.json'
        
        # Cargar credenciales
        self.credentials = self.load_credentials()
        self.config = SimpleDeployConfig(
            github_token=self.credentials.get('GITHUB_TOKEN', ''),
            vercel_token=self.credentials.get('VERCEL_TOKEN', '')
        )
        
        # Headers para APIs
        self.github_headers = {
            "Authorization": f"token {self.config.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        self.vercel_headers = {
            "Authorization": f"Bearer {self.config.vercel_token}",
            "Content-Type": "application/json"
        }
        
        # Estado
        self.deployment_status = {
            "started": False,
            "steps_completed": [],
            "current_step": None,
            "errors": [],
            "success": False,
            "repo_url": None,
            "deployment_url": None
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
    
    def check_github_connection(self) -> bool:
        """Verificar conexión con GitHub"""
        print("🔍 Verificando conexión con GitHub...")
        
        try:
            response = requests.get("https://api.github.com/user", headers=self.github_headers)
            
            if response.status_code == 200:
                user_data = response.json()
                self.log_step("GitHub connection", "success", f"Conectado como {user_data.get('login', 'Unknown')}")
                return True
            else:
                self.log_step("GitHub connection", "error", f"Error {response.status_code}")
                return False
                
        except Exception as e:
            self.log_step("GitHub connection", "error", str(e))
            return False
    
    def create_github_repo(self) -> bool:
        """Crear repositorio en GitHub"""
        print("📂 Creando repositorio en GitHub...")
        
        try:
            # Verificar si ya existe
            response = requests.get(f"https://api.github.com/repos/{self.credentials.get('GITHUB_USER', 'user')}/{self.config.repo_name}", 
                                 headers=self.github_headers)
            
            if response.status_code == 200:
                repo_data = response.json()
                self.deployment_status["repo_url"] = repo_data["html_url"]
                self.log_step("GitHub repo check", "success", f"Repo ya existe: {repo_data['html_url']}")
                return True
            
            # Crear nuevo repositorio
            repo_data = {
                "name": self.config.repo_name,
                "description": "RAULI Enterprise - Professional AI Assistant Platform",
                "private": False,
                "has_issues": True,
                "has_projects": True,
                "has_wiki": True
            }
            
            response = requests.post("https://api.github.com/user/repos", 
                                   headers=self.github_headers, 
                                   json=repo_data)
            
            if response.status_code == 201:
                repo = response.json()
                self.deployment_status["repo_url"] = repo["html_url"]
                self.log_step("GitHub repo creation", "success", f"Repo creado: {repo['html_url']}")
                return True
            else:
                self.log_step("GitHub repo creation", "error", f"Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_step("GitHub repo management", "error", str(e))
            return False
    
    def init_git_repo(self) -> bool:
        """Inicializar repositorio Git local"""
        print("🔧 Inicializando repositorio Git...")
        
        try:
            # Inicializar si no existe
            if not (self.base_dir / '.git').exists():
                subprocess.run(['git', 'init'], cwd=self.base_dir, shell=True, capture_output=True)
            
            # Configurar usuario
            subprocess.run(['git', 'config', 'user.name', 'RAULI Enterprise'], 
                         cwd=self.base_dir, shell=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'rauli@enterprise.com'], 
                         cwd=self.base_dir, shell=True, capture_output=True)
            
            # Agregar remote
            if self.deployment_status["repo_url"]:
                subprocess.run(['git', 'remote', 'add', 'origin', self.deployment_status["repo_url"]], 
                             cwd=self.base_dir, shell=True, capture_output=True)
            
            self.log_step("Git repo init", "success", "Repositorio Git configurado")
            return True
            
        except Exception as e:
            self.log_step("Git repo init", "error", str(e))
            return False
    
    def create_vercel_config_files(self) -> bool:
        """Crear archivos de configuración para Vercel"""
        print("⚙️ Creando archivos de configuración...")
        
        # vercel.json
        vercel_config = {
            "version": 2,
            "name": self.config.project_name,
            "builds": [
                {
                    "src": "dashboard_rauli.py",
                    "use": "@vercel/python"
                },
                {
                    "src": "mobile_web_interface.py", 
                    "use": "@vercel/python"
                }
            ],
            "routes": [
                {
                    "src": "/api/(.*)",
                    "dest": "/mobile_web_interface.py"
                },
                {
                    "src": "/(.*)",
                    "dest": "/dashboard_rauli.py"
                }
            ],
            "env": {
                "OPENAI_API_KEY": self.credentials.get('OPENAI_API_KEY', ''),
                "PYTHON_VERSION": "3.9"
            }
        }
        
        # package.json
        package_json = {
            "name": "rauli-enterprise",
            "version": "1.0.0",
            "description": "RAULI Enterprise Platform",
            "scripts": {
                "build": "pip install -r requirements.txt",
                "start": "python dashboard_rauli.py"
            },
            "dependencies": {
                "streamlit": "^1.28.0",
                "flask": "^2.3.0",
                "requests": "^2.31.0",
                "openai": "^1.3.0"
            }
        }
        
        try:
            with open(self.base_dir / 'vercel.json', 'w', encoding='utf-8') as f:
                json.dump(vercel_config, f, ensure_ascii=False, indent=2)
            
            with open(self.base_dir / 'package.json', 'w', encoding='utf-8') as f:
                json.dump(package_json, f, ensure_ascii=False, indent=2)
            
            self.log_step("Config files creation", "success", "Archivos de configuración creados")
            return True
            
        except Exception as e:
            self.log_step("Config files creation", "error", str(e))
            return False
    
    def commit_and_push(self) -> bool:
        """Hacer commit y push a GitHub"""
        print("📤 Haciendo commit y push...")
        
        try:
            # Agregar archivos
            subprocess.run(['git', 'add', '.'], cwd=self.base_dir, shell=True, capture_output=True)
            
            # Commit
            subprocess.run(['git', 'commit', '-m', '🚀 Initial deployment - RAULI Enterprise'], 
                         cwd=self.base_dir, shell=True, capture_output=True)
            
            # Push
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                         cwd=self.base_dir, shell=True, capture_output=True)
            
            self.log_step("Git push", "success", "Código subido a GitHub")
            return True
            
        except Exception as e:
            self.log_step("Git push", "error", str(e))
            return False
    
    def connect_vercel_to_github(self) -> bool:
        """Conectar Vercel a GitHub"""
        print("🔗 Conectando Vercel a GitHub...")
        
        try:
            # Importar proyecto en Vercel desde GitHub
            import_data = {
                "name": self.config.project_name,
                "framework": "python",
                "gitRepository": {
                    "repo": f"{self.credentials.get('GITHUB_USER', 'user')}/{self.config.repo_name}",
                    "type": "github"
                }
            }
            
            response = requests.post("https://api.vercel.com/v9/projects", 
                                   headers=self.vercel_headers, 
                                   json=import_data)
            
            if response.status_code == 200:
                project = response.json()
                self.log_step("Vercel-GitHub connection", "success", f"Proyecto conectado: {project['id']}")
                return True
            else:
                self.log_step("Vercel-GitHub connection", "error", f"Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_step("Vercel-GitHub connection", "error", str(e))
            return False
    
    def trigger_deployment(self) -> bool:
        """Trigger deployment en Vercel"""
        print("🚀 Trigger deployment en Vercel...")
        
        try:
            # Crear deployment
            deploy_data = {
                "name": self.config.project_name,
                "target": "production"
            }
            
            response = requests.post("https://api.vercel.com/v13/deployments", 
                                   headers=self.vercel_headers, 
                                   json=deploy_data)
            
            if response.status_code == 200:
                deployment = response.json()
                deployment_id = deployment['id']
                
                # Monitorear deployment
                return self.monitor_deployment(deployment_id)
            else:
                self.log_step("Deployment trigger", "error", f"Error {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_step("Deployment trigger", "error", str(e))
            return False
    
    def monitor_deployment(self, deployment_id: str) -> bool:
        """Monitorear deployment"""
        print("⏳ Monitoreando deployment...")
        
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(f"https://api.vercel.com/v13/deployments/{deployment_id}", 
                                      headers=self.vercel_headers)
                
                if response.status_code == 200:
                    deployment = response.json()
                    ready_state = deployment.get('readyState', '')
                    
                    print(f"   Estado: {ready_state}")
                    
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
    
    def generate_report(self) -> str:
        """Generar reporte"""
        report = f"""
# 🚀 RAULI ENTERPRISE - SIMPLE DEPLOYMENT REPORT

## 📊 FECHA
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## ✅ ESTADO
**Estado:** {'✅ EXITOSO' if self.deployment_status['success'] else '❌ FALLIDO'}
**Repositorio:** {self.deployment_status.get('repo_url', 'N/A')}
**Deployment:** {self.deployment_status.get('deployment_url', 'No disponible')}

---

## 📋 PASOS

"""
        
        for step in self.deployment_status["steps_completed"]:
            icon = "✅" if step["status"] == "success" else "❌" if step["status"] == "error" else "⏳"
            report += f"\n{icon} **{step['step']}** - {step['status']}"
            if step["details"]:
                report += f"\n   {step['details']}"
        
        report += f"""

---

## 🎯 ACCESO

- **🌐 GitHub:** {self.deployment_status.get('repo_url', 'N/A')}
- **🚀 Vercel:** {self.deployment_status.get('deployment_url', 'N/A')}

---

**🎉 DEPLOYMENT COMPLETADO VIA GITHUB + VERCEL**
"""
        
        # Guardar reporte
        report_file = self.base_dir / 'simple_deployment_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(report_file)
    
    def execute_deployment(self) -> bool:
        """Ejecutar deployment completo"""
        print("🚀 INICIANDO DEPLOYMENT SIMPLE (GITHUB + VERCEL)")
        print("=" * 60)
        
        self.deployment_status["started"] = True
        
        # Paso 1: Verificar GitHub
        if not self.check_github_connection():
            return False
        
        # Paso 2: Crear repo GitHub
        if not self.create_github_repo():
            return False
        
        # Paso 3: Configurar archivos
        if not self.create_vercel_config_files():
            return False
        
        # Paso 4: Inicializar Git
        if not self.init_git_repo():
            return False
        
        # Paso 5: Commit y push
        if not self.commit_and_push():
            return False
        
        # Paso 6: Conectar Vercel
        if not self.connect_vercel_to_github():
            return False
        
        # Paso 7: Trigger deployment
        if not self.trigger_deployment():
            return False
        
        # Generar reporte
        report_file = self.generate_report()
        
        self.deployment_status["success"] = True
        
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📊 Reporte: {report_file}")
        print(f"🌐 GitHub: {self.deployment_status.get('repo_url', 'No disponible')}")
        print(f"🚀 Vercel: {self.deployment_status.get('deployment_url', 'No disponible')}")
        
        return True

def main():
    """Función principal"""
    print("🚀 RAULI VERCEL SIMPLE DEPLOYMENT")
    print("Deployment via GitHub + Vercel integration")
    print("")
    
    deploy = VercelSimpleDeploy()
    
    if deploy.execute_deployment():
        print("\n✅ DEPLOYMENT EXITOSO")
        
        # Abrir navegador
        if deploy.deployment_status.get("deployment_url"):
            webbrowser.open(deploy.deployment_status["deployment_url"])
            print(f"🌐 Abriendo: {deploy.deployment_status['deployment_url']}")
        
        # Notificar
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "¡Deployment simple completado! RAULI Enterprise está en producción."
            ], cwd=r'C:\dev')
        except:
            pass
    
    else:
        print("\n❌ DEPLOYMENT FALLIDO")

if __name__ == "__main__":
    main()
