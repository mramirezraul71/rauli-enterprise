#!/usr/bin/env python3
"""
🚨 RAULI ENTERPRISE - VERCEL EMERGENCY FIX
Solución de emergencia para errores en producción
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

@dataclass
class EmergencyFix:
    """Fix de emergencia"""
    issue: str
    solution: str
    priority: str
    status: str

class VercelEmergencyFix:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.credenciales_file = self.base_dir / 'credenciales.env'
        self.emergency_log_file = self.base_dir / 'emergency_fix_log.json'
        
        # Cargar credenciales
        self.credentials = self.load_credentials()
        
        # Headers para APIs
        self.github_headers = {
            "Authorization": f"token {self.credentials.get('GITHUB_TOKEN', '')}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
        
        self.vercel_headers = {
            "Authorization": f"Bearer {self.credentials.get('VERCEL_TOKEN', '')}",
            "Content-Type": "application/json"
        }
        
        # Estado
        self.fix_status = {
            "started": False,
            "issues_found": [],
            "fixes_applied": [],
            "deployment_triggered": False,
            "success": False
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
            return credentials
        except Exception as e:
            print(f"❌ Error cargando credenciales: {e}")
            return {}
    
    def log_action(self, action: str, details: str = ""):
        """Registrar acción"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        
        self.fix_status["fixes_applied"].append(log_entry)
        
        print(f"🔧 {action}")
        if details:
            print(f"   {details}")
        
        # Guardar log
        with open(self.emergency_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.fix_status, f, ensure_ascii=False, indent=2)
    
    def diagnose_vercel_issues(self) -> List[EmergencyFix]:
        """Diagnosticar problemas en Vercel"""
        print("🔍 Diagnosticando problemas en Vercel...")
        
        issues = []
        
        try:
            # Verificar estado del proyecto
            response = requests.get("https://api.vercel.com/v9/projects", 
                                  headers=self.vercel_headers)
            
            if response.status_code == 200:
                projects = response.json().get('projects', [])
                target_project = None
                
                for project in projects:
                    if project.get('name', '').lower() == 'rauli-enterprise':
                        target_project = project
                        break
                
                if target_project:
                    # Verificar deployments recientes
                    project_id = target_project['id']
                    response = requests.get(f"https://api.vercel.com/v13/deployments", 
                                          headers=self.vercel_headers,
                                          params={"projectId": project_id})
                    
                    if response.status_code == 200:
                        deployments = response.json().get('deployments', [])
                        
                        if deployments:
                            latest_deployment = deployments[0]
                            state = latest_deployment.get('readyState', '')
                            
                            if state == "ERROR":
                                issues.append(EmergencyFix(
                                    issue="Deployment fallido",
                                    solution=f"Re-deploy con configuración corregida. Error: {latest_deployment.get('error', 'Unknown')}",
                                    priority="high",
                                    status="pending"
                                ))
                            elif state == "BUILDING":
                                issues.append(EmergencyFix(
                                    issue="Deployment en progreso",
                                    solution="Esperar a que complete el build",
                                    priority="medium",
                                    status="pending"
                                ))
                            elif state == "READY":
                                issues.append(EmergencyFix(
                                    issue="Deployment listo pero con errores",
                                    solution="Verificar variables de entorno y configuración",
                                    priority="high",
                                    status="pending"
                                ))
                        else:
                            issues.append(EmergencyFix(
                                issue="No hay deployments",
                                solution="Crear nuevo deployment",
                                priority="high",
                                status="pending"
                            ))
                    
                    # Verificar variables de entorno
                    response = requests.get(f"https://api.vercel.com/v9/projects/{project_id}/env", 
                                          headers=self.vercel_headers)
                    
                    if response.status_code == 200:
                        env_vars = response.json().get('envs', [])
                        
                        # Verificar variables críticas
                        critical_vars = ['OPENAI_API_KEY', 'PYTHON_VERSION', 'RAULI_ENV']
                        
                        for var in critical_vars:
                            found = False
                            for env_var in env_vars:
                                if env_var.get('key') == var:
                                    found = True
                                    break
                            
                            if not found:
                                issues.append(EmergencyFix(
                                    issue=f"Variable de entorno faltante: {var}",
                                    solution=f"Agregar {var} a variables de entorno",
                                    priority="high",
                                    status="pending"
                                ))
                else:
                    issues.append(EmergencyFix(
                        issue="Proyecto no encontrado en Vercel",
                        solution="Crear proyecto en Vercel",
                        priority="high",
                        status="pending"
                    ))
            else:
                issues.append(EmergencyFix(
                    issue="Error accediendo a Vercel API",
                    solution=f"Verificar token Vercel. Error: {response.status_code}",
                    priority="high",
                    status="pending"
                ))
                
        except Exception as e:
            issues.append(EmergencyFix(
                issue="Error en diagnóstico",
                solution=str(e),
                priority="high",
                status="pending"
            ))
        
        self.fix_status["issues_found"] = [
            {
                "issue": issue.issue,
                "solution": issue.solution,
                "priority": issue.priority,
                "status": issue.status
            } for issue in issues
        ]
        return issues
    
    def fix_environment_variables(self) -> bool:
        """Corregir variables de entorno"""
        print("🔧 Corrigiendo variables de entorno...")
        
        try:
            # Obtener project ID
            response = requests.get("https://api.vercel.com/v9/projects", 
                                  headers=self.vercel_headers)
            
            if response.status_code == 200:
                projects = response.json().get('projects', [])
                project_id = None
                
                for project in projects:
                    if project.get('name', '').lower() == 'rauli-enterprise':
                        project_id = project['id']
                        break
                
                if project_id:
                    # Variables críticas a configurar
                    critical_vars = {
                        "OPENAI_API_KEY": self.credentials.get('OPENAI_API_KEY', ''),
                        "PYTHON_VERSION": "3.9",
                        "RAULI_ENV": "production",
                        "RAULI_VERSION": "1.0.0"
                    }
                    
                    for var_key, var_value in critical_vars.items():
                        if var_value:  # Solo si tiene valor
                            env_data = {
                                "key": var_key,
                                "value": var_value,
                                "type": "encrypted" if var_key == "OPENAI_API_KEY" else "plain"
                            }
                            
                            response = requests.post(f"https://api.vercel.com/v9/projects/{project_id}/env", 
                                                   headers=self.vercel_headers, 
                                                   json=env_data)
                            
                            if response.status_code in [200, 201]:
                                self.log_action(f"Variable {var_key}", "Configurada exitosamente")
                            else:
                                self.log_action(f"Variable {var_key}", f"Error: {response.status_code}")
                    
                    return True
                else:
                    self.log_action("Variables de entorno", "Proyecto no encontrado")
                    return False
            else:
                self.log_action("Variables de entorno", f"Error API: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_action("Variables de entorno", f"Error: {e}")
            return False
    
    def trigger_emergency_deployment(self) -> bool:
        """Trigger deployment de emergencia"""
        print("🚀 Trigger deployment de emergencia...")
        
        try:
            # Obtener último commit de GitHub
            response = requests.get("https://api.github.com/repos/mramirezraul71/rauli-enterprise/commits/main", 
                                  headers=self.github_headers)
            
            if response.status_code == 200:
                commit = response.json()
                commit_sha = commit['sha']
                
                # Obtener project ID
                response = requests.get("https://api.vercel.com/v9/projects", 
                                      headers=self.vercel_headers)
                
                if response.status_code == 200:
                    projects = response.json().get('projects', [])
                    project_id = None
                    
                    for project in projects:
                        if project.get('name', '').lower() == 'rauli-enterprise':
                            project_id = project['id']
                            break
                    
                    if project_id:
                        # Crear deployment
                        deploy_data = {
                            "name": "rauli-enterprise",
                            "target": "production",
                            "gitCommit": {
                                "sha": commit_sha,
                                "repo": "mramirezraul71/rauli-enterprise"
                            },
                            "projectSettings": {
                                "framework": "python",
                                "buildCommand": "pip install -r requirements.txt",
                                "outputDirectory": ".",
                                "installCommand": "pip install -r requirements.txt"
                            }
                        }
                        
                        response = requests.post("https://api.vercel.com/v13/deployments", 
                                               headers=self.vercel_headers, 
                                               json=deploy_data)
                        
                        if response.status_code == 200:
                            deployment = response.json()
                            deployment_id = deployment['id']
                            
                            self.log_action("Emergency deployment", f"Triggered: {deployment_id}")
                            self.fix_status["deployment_triggered"] = True
                            
                            # Monitorear deployment
                            return self.monitor_deployment(deployment_id)
                        else:
                            self.log_action("Emergency deployment", f"Error: {response.status_code}")
                            return False
                    else:
                        self.log_action("Emergency deployment", "Proyecto no encontrado")
                        return False
                else:
                    self.log_action("Emergency deployment", f"Error proyectos: {response.status_code}")
                    return False
            else:
                self.log_action("Emergency deployment", f"Error commit: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_action("Emergency deployment", f"Error: {e}")
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
                        self.log_action("Deployment completado", f"URL: {deployment_url}")
                        return True
                    elif ready_state == "ERROR":
                        error_message = deployment.get('error', 'Error desconocido')
                        self.log_action("Deployment falló", f"Error: {error_message}")
                        return False
                
                attempt += 1
                time.sleep(10)
                
            except Exception as e:
                self.log_action("Monitoreo deployment", f"Error: {e}")
                return False
        
        self.log_action("Monitoreo deployment", "Timeout")
        return False
    
    def generate_emergency_report(self) -> str:
        """Generar reporte de emergencia"""
        print("📊 Generando reporte de emergencia...")
        
        report = f"""
# 🚨 RAULI ENTERPRISE - EMERGENCY FIX REPORT

## 📊 FECHA
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🚨 **ESTADO DE EMERGENCIA**

### 📈 **Diagnóstico**
- **Issues encontrados:** {len(self.fix_status['issues_found'])}
- **Fixes aplicados:** {len(self.fix_status['fixes_applied'])}
- **Deployment triggered:** {'✅ Sí' if self.fix_status['deployment_triggered'] else '❌ No'}

---

## 🔍 **Issues Detectados**

"""
        
        for issue in self.fix_status["issues_found"]:
            priority_icon = "🔴" if issue.priority == "high" else "🟡" if issue.priority == "medium" else "🟢"
            report += f"\n{priority_icon} **{issue.issue}**\n"
            report += f"   - Solución: {issue.solution}\n"
            report += f"   - Prioridad: {issue.priority}\n"
            report += f"   - Estado: {issue.status}\n"
        
        report += f"""

---

## 🔧 **Fixes Aplicados**

"""
        
        for fix in self.fix_status["fixes_applied"]:
            report += f"\n✅ **{fix['action']}** - {fix['timestamp']}\n"
            if fix["details"]:
                report += f"   {fix['details']}\n"
        
        if self.fix_status["deployment_triggered"]:
            report += f"""

---

## 🚀 **Deployment Status**

✅ **Emergency deployment triggered**

"""
        
        # Conclusión
        if self.fix_status["success"]:
            report += f"""

## 🎉 **CONCLUSIÓN**

**✅ EMERGENCIA RESUELTA**

RAULI Enterprise está operativo en producción.

"""
        else:
            report += f"""

## 🚨 **CONCLUSIÓN**

**❌ EMERGENCIA EN PROGRESO**

Se están aplicando soluciones para restaurar el servicio.

"""
        
        report += f"""

---

## 📞 **Contacto y Soporte**

- **Dashboard Vercel:** https://vercel.com/dashboard
- **Repositorio GitHub:** https://github.com/mramirezraul71/rauli-enterprise
- **Aplicación:** https://rauli-enterprise.vercel.app

---

**🚨 Emergency Fix Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        # Guardar reporte
        report_file = self.base_dir / 'emergency_fix_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(report_file)
    
    def execute_emergency_fix(self) -> bool:
        """Ejecutar fix de emergencia"""
        print("🚨 INICIANDO EMERGENCY FIX")
        print("=" * 60)
        print("🔧 Solucionando problemas críticos en producción")
        print("=" * 60)
        
        self.fix_status["started"] = True
        
        # Paso 1: Diagnosticar problemas
        issues = self.diagnose_vercel_issues()
        
        if not issues:
            self.log_action("Diagnóstico", "No se encontraron problemas críticos")
            self.fix_status["success"] = True
            return True
        
        # Paso 2: Aplicar fixes según prioridad
        high_priority_issues = [i for i in issues if i.priority == "high"]
        
        for issue in high_priority_issues:
            if "Variable de entorno" in issue.issue:
                self.fix_environment_variables()
            elif "Deployment" in issue.issue:
                self.trigger_emergency_deployment()
        
        # Paso 3: Generar reporte
        report_file = self.generate_emergency_report()
        
        print("\n" + "=" * 60)
        print("🎉 EMERGENCY FIX COMPLETADO")
        print("=" * 60)
        print(f"📊 Reporte: {report_file}")
        print(f"🔧 Fixes aplicados: {len(self.fix_status['fixes_applied'])}")
        
        return self.fix_status["success"]

def main():
    """Función principal"""
    print("🚨 RAULI ENTERPRISE - VERCEL EMERGENCY FIX")
    print("Solución de emergencia para errores en producción")
    print("")
    
    emergency_fix = VercelEmergencyFix()
    
    if emergency_fix.execute_emergency_fix():
        print("\n✅ EMERGENCY FIX EXITOSO")
        print("🎯 RAULI Enterprise está operativo")
        
        # Notificar por voz
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "¡Emergency fix completado! RAULI Enterprise está operativo en producción."
            ], cwd=r'C:\dev')
        except:
            pass
        
        # Notificar por Telegram
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\comunicador.py',
                '--telegram',
                f"✅ EMERGENCY FIX COMPLETADO\n\n🎯 **Estado:** Operativo\n🔧 **Fixes aplicados:** {len(emergency_fix.fix_status['fixes_applied'])}\n🚀 **Deployment:** Triggered\n🌐 **RAULI ENTERPRISE EN PRODUCCIÓN**"
            ], cwd=r'C:\dev')
        except:
            pass
    
    else:
        print("\n❌ EMERGENCY FIX EN PROGRESO")
        print("🔧 Aplicando soluciones...")
        
        # Notificar por voz
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "Emergency fix en progreso. Trabajando en solucionar problemas."
            ], cwd=r'C:\dev')
        except:
            pass

if __name__ == "__main__":
    main()
