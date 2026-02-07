#!/usr/bin/env python3
"""
🔍 RAULI ENTERPRISE - VERCEL CONFIG VALIDATOR
Validación detallada de configuración y parámetros
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
class ValidationResult:
    """Resultado de validación"""
    parameter: str
    expected: str
    actual: str
    status: str  # ok, warning, error
    details: str

class VercelConfigValidator:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.credenciales_file = self.base_dir / 'credenciales.env'
        self.validation_log_file = self.base_dir / 'validation_log.json'
        
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
        
        # Estado de validación
        self.validation_results = []
        self.critical_issues = []
        self.warnings = []
        
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
    
    def add_validation_result(self, parameter: str, expected: str, actual: str, status: str, details: str = ""):
        """Agregar resultado de validación"""
        result = ValidationResult(
            parameter=parameter,
            expected=expected,
            actual=actual,
            status=status,
            details=details
        )
        
        self.validation_results.append(result)
        
        if status == "error":
            self.critical_issues.append(result)
        elif status == "warning":
            self.warnings.append(result)
        
        icon = "✅" if status == "ok" else "⚠️" if status == "warning" else "❌"
        print(f"{icon} {parameter}")
        if expected != actual:
            print(f"   Esperado: {expected}")
            print(f"   Actual: {actual}")
        if details:
            print(f"   {details}")
    
    def validate_file_structure(self) -> bool:
        """Validar estructura de archivos"""
        print("📁 Validando estructura de archivos...")
        
        required_files = {
            'dashboard_rauli.py': 'Principal dashboard',
            'mobile_web_interface.py': 'Mobile interface',
            'requirements.txt': 'Dependencias Python',
            'vercel.json': 'Configuración Vercel',
            'package.json': 'Configuración Node.js',
            'README.md': 'Documentación',
            '.gitignore': 'Git ignore'
        }
        
        all_ok = True
        for file_path, description in required_files.items():
            full_path = self.base_dir / file_path
            if full_path.exists():
                self.add_validation_result(
                    f"Archivo {file_path}",
                    "Existe",
                    "Existe",
                    "ok",
                    description
                )
            else:
                self.add_validation_result(
                    f"Archivo {file_path}",
                    "Existe",
                    "No existe",
                    "error",
                    f"CRÍTICO: {description} - Archivo requerido"
                )
                all_ok = False
        
        return all_ok
    
    def validate_vercel_json(self) -> bool:
        """Validar configuración vercel.json"""
        print("⚙️ Validando vercel.json...")
        
        vercel_file = self.base_dir / 'vercel.json'
        if not vercel_file.exists():
            self.add_validation_result(
                "vercel.json",
                "Existe",
                "No existe",
                "error",
                "Archivo de configuración Vercel no encontrado"
            )
            return False
        
        try:
            with open(vercel_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validar versión
            version = config.get('version', '')
            if version == 2:
                self.add_validation_result("vercel.json version", "2", str(version), "ok")
            else:
                self.add_validation_result("vercel.json version", "2", str(version), "error", "Versión incorrecta")
            
            # Validar nombre del proyecto
            name = config.get('name', '')
            expected_name = "rauli-enterprise"
            if name.lower() == expected_name.lower():
                self.add_validation_result("vercel.json name", expected_name, name, "ok")
            else:
                self.add_validation_result("vercel.json name", expected_name, name, "error", "Nombre de proyecto incorrecto")
            
            # Validar builds
            builds = config.get('builds', [])
            expected_builds = [
                {"src": "dashboard_rauli.py", "use": "@vercel/python"},
                {"src": "mobile_web_interface.py", "use": "@vercel/python"}
            ]
            
            if len(builds) == 2:
                self.add_validation_result("vercel.json builds count", "2", str(len(builds)), "ok")
                
                # Validar cada build
                for i, expected_build in enumerate(expected_builds):
                    if i < len(builds):
                        actual_build = builds[i]
                        src_ok = actual_build.get('src', '') == expected_build['src']
                        use_ok = actual_build.get('use', '') == expected_build['use']
                        
                        if src_ok and use_ok:
                            self.add_validation_result(
                                f"vercel.json build {i+1}",
                                f"{expected_build['src']} -> {expected_build['use']}",
                                f"{actual_build.get('src', '')} -> {actual_build.get('use', '')}",
                                "ok"
                            )
                        else:
                            self.add_validation_result(
                                f"vercel.json build {i+1}",
                                f"{expected_build['src']} -> {expected_build['use']}",
                                f"{actual_build.get('src', '')} -> {actual_build.get('use', '')}",
                                "error",
                                "Configuración de build incorrecta"
                            )
            else:
                self.add_validation_result("vercel.json builds count", "2", str(len(builds)), "error", "Número de builds incorrecto")
            
            # Validar routes
            routes = config.get('routes', [])
            expected_routes = [
                {"src": "/api/(.*)", "dest": "/mobile_web_interface.py"},
                {"src": "/(.*)", "dest": "/dashboard_rauli.py"}
            ]
            
            if len(routes) == 2:
                self.add_validation_result("vercel.json routes count", "2", str(len(routes)), "ok")
                
                for i, expected_route in enumerate(expected_routes):
                    if i < len(routes):
                        actual_route = routes[i]
                        src_ok = actual_route.get('src', '') == expected_route['src']
                        dest_ok = actual_route.get('dest', '') == expected_route['dest']
                        
                        if src_ok and dest_ok:
                            self.add_validation_result(
                                f"vercel.json route {i+1}",
                                f"{expected_route['src']} -> {expected_route['dest']}",
                                f"{actual_route.get('src', '')} -> {actual_route.get('dest', '')}",
                                "ok"
                            )
                        else:
                            self.add_validation_result(
                                f"vercel.json route {i+1}",
                                f"{expected_route['src']} -> {expected_route['dest']}",
                                f"{actual_route.get('src', '')} -> {actual_route.get('dest', '')}",
                                "error",
                                "Configuración de route incorrecta"
                            )
            else:
                self.add_validation_result("vercel.json routes count", "2", str(len(routes)), "error", "Número de routes incorrecto")
            
            return True
            
        except Exception as e:
            self.add_validation_result("vercel.json parsing", "JSON válido", f"Error: {e}", "error", "Error parsing vercel.json")
            return False
    
    def validate_package_json(self) -> bool:
        """Validar package.json"""
        print("📦 Validando package.json...")
        
        package_file = self.base_dir / 'package.json'
        if not package_file.exists():
            self.add_validation_result("package.json", "Existe", "No existe", "error", "Archivo package.json no encontrado")
            return False
        
        try:
            with open(package_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validar nombre
            name = config.get('name', '')
            expected_name = "rauli-enterprise"
            if name.lower() == expected_name.lower():
                self.add_validation_result("package.json name", expected_name, name, "ok")
            else:
                self.add_validation_result("package.json name", expected_name, name, "error", "Nombre de paquete incorrecto")
            
            # Validar versión
            version = config.get('version', '')
            if version == "1.0.0":
                self.add_validation_result("package.json version", "1.0.0", version, "ok")
            else:
                self.add_validation_result("package.json version", "1.0.0", version, "warning", "Versión no estándar")
            
            # Validar scripts
            scripts = config.get('scripts', {})
            expected_scripts = {
                "build": "pip install -r requirements.txt",
                "start": "python dashboard_rauli.py"
            }
            
            for script_name, expected_command in expected_scripts.items():
                actual_command = scripts.get(script_name, '')
                if actual_command == expected_command:
                    self.add_validation_result(f"package.json script {script_name}", expected_command, actual_command, "ok")
                else:
                    self.add_validation_result(f"package.json script {script_name}", expected_command, actual_command, "error", "Script incorrecto")
            
            return True
            
        except Exception as e:
            self.add_validation_result("package.json parsing", "JSON válido", f"Error: {e}", "error", "Error parsing package.json")
            return False
    
    def validate_requirements_txt(self) -> bool:
        """Validar requirements.txt"""
        print("📋 Validando requirements.txt...")
        
        req_file = self.base_dir / 'requirements.txt'
        if not req_file.exists():
            self.add_validation_result("requirements.txt", "Existe", "No existe", "error", "Archivo requirements.txt no encontrado")
            return False
        
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                requirements = f.read().strip().split('\n')
            
            # Validar dependencias críticas
            critical_deps = {
                'streamlit': '>=1.28.0',
                'flask': '>=2.3.0',
                'requests': '>=2.31.0',
                'openai': '>=1.3.0'
            }
            
            found_deps = []
            for req in requirements:
                if req.strip() and not req.startswith('#'):
                    dep_name = req.split('>=')[0].split('==')[0].split('<=')[0].strip()
                    found_deps.append(dep_name.lower())
            
            for dep_name, expected_version in critical_deps.items():
                if dep_name in found_deps:
                    self.add_validation_result(f"requirements.txt {dep_name}", expected_version, "Encontrado", "ok")
                else:
                    self.add_validation_result(f"requirements.txt {dep_name}", expected_version, "No encontrado", "error", f"Dependencia crítica faltante: {dep_name}")
            
            return True
            
        except Exception as e:
            self.add_validation_result("requirements.txt parsing", "Válido", f"Error: {e}", "error", "Error parsing requirements.txt")
            return False
    
    def validate_python_files(self) -> bool:
        """Validar archivos Python"""
        print("🐍 Validando archivos Python...")
        
        python_files = {
            'dashboard_rauli.py': 'Dashboard principal',
            'mobile_web_interface.py': 'Interface móvil'
        }
        
        all_ok = True
        for file_name, description in python_files.items():
            file_path = self.base_dir / file_name
            if not file_path.exists():
                self.add_validation_result(f"Python file {file_name}", "Existe", "No existe", "error", f"Archivo Python crítico: {description}")
                all_ok = False
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Validar que no tenga errores de sintaxis básicos
                try:
                    compile(content, file_path, 'exec')
                    self.add_validation_result(f"Python syntax {file_name}", "Válido", "Válido", "ok")
                except SyntaxError as e:
                    self.add_validation_result(f"Python syntax {file_name}", "Válido", f"Error: {e}", "error", "Error de sintaxis")
                    all_ok = False
                
                # Validar imports críticos
                critical_imports = {
                    'dashboard_rauli.py': ['streamlit', 'openai', 'requests'],
                    'mobile_web_interface.py': ['flask', 'openai', 'requests']
                }
                
                if file_name in critical_imports:
                    for import_name in critical_imports[file_name]:
                        if import_name in content:
                            self.add_validation_result(f"Import {import_name} in {file_name}", "Presente", "Presente", "ok")
                        else:
                            self.add_validation_result(f"Import {import_name} in {file_name}", "Presente", "Ausente", "warning", f"Import opcional: {import_name}")
                
            except Exception as e:
                self.add_validation_result(f"Python file {file_name}", "Legible", f"Error: {e}", "error", "Error leyendo archivo")
                all_ok = False
        
        return all_ok
    
    def validate_github_repo(self) -> bool:
        """Validar repositorio GitHub"""
        print("🔗 Validando repositorio GitHub...")
        
        try:
            # Verificar si el repositorio existe
            response = requests.get("https://api.github.com/repos/mramirezraul71/rauli-enterprise", 
                                  headers=self.github_headers)
            
            if response.status_code == 200:
                repo_data = response.json()
                
                # Validar nombre
                name = repo_data.get('name', '')
                if name.lower() == 'rauli-enterprise':
                    self.add_validation_result("GitHub repo name", "rauli-enterprise", name, "ok")
                else:
                    self.add_validation_result("GitHub repo name", "rauli-enterprise", name, "error", "Nombre de repo incorrecto")
                
                # Validar que sea público
                if not repo_data.get('private', True):
                    self.add_validation_result("GitHub repo visibility", "Público", "Público", "ok")
                else:
                    self.add_validation_result("GitHub repo visibility", "Público", "Privado", "error", "Repo debe ser público")
                
                # Validar rama principal
                default_branch = repo_data.get('default_branch', '')
                if default_branch.lower() in ['main', 'master']:
                    self.add_validation_result("GitHub default branch", "main/master", default_branch, "ok")
                else:
                    self.add_validation_result("GitHub default branch", "main/master", default_branch, "warning", "Rama no estándar")
                
                return True
            else:
                self.add_validation_result("GitHub repo access", "Accesible", f"Error {response.status_code}", "error", "No se puede acceder al repo")
                return False
                
        except Exception as e:
            self.add_validation_result("GitHub repo validation", "Válido", f"Error: {e}", "error", "Error validando repo")
            return False
    
    def validate_vercel_project(self) -> bool:
        """Validar proyecto Vercel"""
        print("🚀 Validando proyecto Vercel...")
        
        try:
            # Listar proyectos
            response = requests.get("https://api.vercel.com/v9/projects", 
                                  headers=self.vercel_headers)
            
            if response.status_code == 200:
                projects = response.json().get('projects', [])
                
                # Buscar proyecto rauli-enterprise
                target_project = None
                for project in projects:
                    if project.get('name', '').lower() == 'rauli-enterprise':
                        target_project = project
                        break
                
                if target_project:
                    # Validar nombre
                    name = target_project.get('name', '')
                    if name.lower() == 'rauli-enterprise':
                        self.add_validation_result("Vercel project name", "rauli-enterprise", name, "ok")
                    else:
                        self.add_validation_result("Vercel project name", "rauli-enterprise", name, "error", "Nombre de proyecto incorrecto")
                    
                    # Validar framework
                    framework = target_project.get('framework', '')
                    if framework.lower() == 'python':
                        self.add_validation_result("Vercel framework", "python", framework, "ok")
                    else:
                        self.add_validation_result("Vercel framework", "python", framework, "error", "Framework incorrecto")
                    
                    # Validar que tenga linked repo
                    linked_repo = target_project.get('link', {})
                    if linked_repo:
                        self.add_validation_result("Vercel linked repo", "Conectado", "Conectado", "ok")
                    else:
                        self.add_validation_result("Vercel linked repo", "Conectado", "No conectado", "warning", "Repo no conectado")
                    
                    return True
                else:
                    self.add_validation_result("Vercel project", "rauli-enterprise", "No encontrado", "error", "Proyecto no existe en Vercel")
                    return False
            else:
                self.add_validation_result("Vercel API access", "Accesible", f"Error {response.status_code}", "error", "No se puede acceder a Vercel API")
                return False
                
        except Exception as e:
            self.add_validation_result("Vercel project validation", "Válido", f"Error: {e}", "error", "Error validando proyecto Vercel")
            return False
    
    def validate_case_sensitivity(self) -> bool:
        """Validar sensibilidad a mayúsculas/minúsculas"""
        print("🔤 Validando sensibilidad a mayúsculas/minúsculas...")
        
        # Validar nombres de archivos
        expected_names = {
            'dashboard_rauli.py': 'dashboard_rauli.py',
            'mobile_web_interface.py': 'mobile_web_interface.py',
            'requirements.txt': 'requirements.txt',
            'vercel.json': 'vercel.json',
            'package.json': 'package.json'
        }
        
        all_ok = True
        for expected_name, actual_name in expected_names.items():
            file_path = self.base_dir / expected_name
            if file_path.exists():
                # Verificar que el nombre exacto coincida
                actual_file_name = file_path.name
                if actual_file_name == expected_name:
                    self.add_validation_result(f"Case sensitivity {expected_name}", expected_name, actual_file_name, "ok")
                else:
                    self.add_validation_result(f"Case sensitivity {expected_name}", expected_name, actual_file_name, "error", "Nombre de archivo con mayúsculas/minúsculas incorrectas")
                    all_ok = False
            else:
                self.add_validation_result(f"Case sensitivity {expected_name}", expected_name, "No existe", "error", "Archivo no encontrado")
                all_ok = False
        
        return all_ok
    
    def validate_special_characters(self) -> bool:
        """Validar caracteres especiales"""
        print("🔣 Validando caracteres especiales...")
        
        # Validar que no haya caracteres problemáticos en nombres
        problematic_chars = [' ', 'á', 'é', 'í', 'ó', 'ú', 'ñ', 'ü']
        
        files_to_check = [
            'dashboard_rauli.py',
            'mobile_web_interface.py',
            'requirements.txt',
            'vercel.json',
            'package.json'
        ]
        
        all_ok = True
        for file_name in files_to_check:
            file_path = self.base_dir / file_name
            if file_path.exists():
                actual_name = file_path.name
                for char in problematic_chars:
                    if char in actual_name:
                        self.add_validation_result(f"Special chars {file_name}", f"Sin '{char}'", f"Contiene '{char}'", "error", f"Carácter problemático encontrado")
                        all_ok = False
                        break
                else:
                    self.add_validation_result(f"Special chars {file_name}", "Sin caracteres problemáticos", "Limpio", "ok")
            else:
                self.add_validation_result(f"Special chars {file_name}", "Existe", "No existe", "error", "Archivo no encontrado")
                all_ok = False
        
        return all_ok
    
    def generate_validation_report(self) -> str:
        """Generar reporte de validación"""
        print("📊 Generando reporte de validación...")
        
        # Contar resultados
        total_checks = len(self.validation_results)
        ok_count = len([r for r in self.validation_results if r.status == "ok"])
        warning_count = len([r for r in self.validation_results if r.status == "warning"])
        error_count = len([r for r in self.validation_results if r.status == "error"])
        
        # Generar reporte
        report = f"""
# 🔍 RAULI ENTERPRISE - VALIDATION REPORT

## 📊 FECHA
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📈 RESUMEN DE VALIDACIÓN

### 🎯 **Estado General**
- **Total de checks:** {total_checks}
- **✅ Exitosos:** {ok_count}
- **⚠️ Advertencias:** {warning_count}
- **❌ Errores:** {error_count}
- **📊 Porcentaje éxito:** {(ok_count/total_checks)*100:.1f}%

### 🚨 **Issues Críticos**
{len(self.critical_issues)} errores críticos encontrados

### ⚠️ **Advertencias**
{len(self.warnings)} advertencias encontradas

---

## 📋 DETALLE DE VALIDACIÓN

### ✅ **Checks Exitosos ({ok_count})**

"""
        
        # Agregar checks exitosos
        ok_results = [r for r in self.validation_results if r.status == "ok"]
        for result in ok_results:
            report += f"- ✅ **{result.parameter}** - {result.details if result.details else 'OK'}\n"
        
        if self.warnings:
            report += f"""

### ⚠️ **Advertencias ({warning_count})**

"""
            for result in self.warnings:
                report += f"- ⚠️ **{result.parameter}** - {result.details if result.details else 'Advertencia'}\n"
                if result.expected != result.actual:
                    report += f"  - Esperado: `{result.expected}`\n"
                    report += f"  - Actual: `{result.actual}`\n"
        
        if self.critical_issues:
            report += f"""

### ❌ **Errores Críticos ({error_count})**

"""
            for result in self.critical_issues:
                report += f"- ❌ **{result.parameter}** - {result.details if result.details else 'Error'}\n"
                if result.expected != result.actual:
                    report += f"  - Esperado: `{result.expected}`\n"
                    report += f"  - Actual: `{result.actual}`\n"
        
        # Recomendaciones
        if self.critical_issues:
            report += f"""

## 🚨 **ACCIONES REQUERIDAS**

### 🔧 **Correcciones Críticas Necesarias:**

"""
            for issue in self.critical_issues:
                report += f"1. **{issue.parameter}**: {issue.details}\n"
                if issue.parameter.startswith("Archivo"):
                    report += f"   - Crear/verificar archivo: `{issue.expected}`\n"
                elif issue.parameter.startswith("vercel.json"):
                    report += f"   - Corregir configuración en vercel.json\n"
                elif issue.parameter.startswith("GitHub"):
                    report += f"   - Configurar repositorio GitHub\n"
                elif issue.parameter.startswith("Vercel"):
                    report += f"   - Configurar proyecto en Vercel\n"
        
        if self.warnings:
            report += f"""

### ⚠️ **Mejoras Recomendadas:**

"""
            for warning in self.warnings:
                report += f"1. **{warning.parameter}**: {warning.details}\n"
        
        # Conclusión
        if error_count == 0:
            report += f"""

## 🎉 **CONCLUSIÓN**

**✅ VALIDACIÓN EXITOSA**

No se encontraron errores críticos. La configuración está lista para deployment.

"""
            if warning_count > 0:
                report += f"Se encontraron {warning_count} advertencias que se recomienda corregir para optimizar el deployment.\n"
        else:
            report += f"""

## 🚨 **CONCLUSIÓN**

**❌ VALIDACIÓN FALLIDA**

Se encontraron {error_count} errores críticos que deben ser corregidos antes del deployment.

"""
        
        report += f"""

---

## 📊 **MÉTRICAS DE CALIDAD**

- **Precisión:** {(ok_count/total_checks)*100:.1f}%
- **Completitud:** {(ok_count + warning_count)/total_checks*100:.1f}%
- **Estado:** {'✅ Listo para deployment' if error_count == 0 else '❌ Requiere correcciones'}

---

**🔍 Validación completada - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        # Guardar reporte
        report_file = self.base_dir / 'validation_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Guardar resultados JSON
        validation_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_checks": total_checks,
                "ok_count": ok_count,
                "warning_count": warning_count,
                "error_count": error_count,
                "success_rate": (ok_count/total_checks)*100
            },
            "results": [
                {
                    "parameter": r.parameter,
                    "expected": r.expected,
                    "actual": r.actual,
                    "status": r.status,
                    "details": r.details
                } for r in self.validation_results
            ],
            "critical_issues": [
                {
                    "parameter": i.parameter,
                    "expected": i.expected,
                    "actual": i.actual,
                    "details": i.details
                } for i in self.critical_issues
            ],
            "warnings": [
                {
                    "parameter": w.parameter,
                    "expected": w.expected,
                    "actual": w.actual,
                    "details": w.details
                } for w in self.warnings
            ]
        }
        
        with open(self.validation_log_file, 'w', encoding='utf-8') as f:
            json.dump(validation_data, f, ensure_ascii=False, indent=2)
        
        return str(report_file)
    
    def execute_validation(self) -> bool:
        """Ejecutar validación completa"""
        print("🔍 INICIANDO VALIDACIÓN COMPLETA DE CONFIGURACIÓN")
        print("=" * 80)
        print("🎯 Validando todos los parámetros críticos para deployment")
        print("=" * 80)
        
        # Ejecutar todas las validaciones
        validations = [
            self.validate_file_structure,
            self.validate_vercel_json,
            self.validate_package_json,
            self.validate_requirements_txt,
            self.validate_python_files,
            self.validate_github_repo,
            self.validate_vercel_project,
            self.validate_case_sensitivity,
            self.validate_special_characters
        ]
        
        all_valid = True
        for validation_func in validations:
            try:
                if not validation_func():
                    all_valid = False
                print()  # Espacio entre validaciones
            except Exception as e:
                print(f"❌ Error en validación {validation_func.__name__}: {e}")
                all_valid = False
        
        # Generar reporte
        report_file = self.generate_validation_report()
        
        print("\n" + "=" * 80)
        print("🎉 VALIDACIÓN COMPLETADA")
        print("=" * 80)
        print(f"📊 Reporte: {report_file}")
        print(f"📈 Datos: {self.validation_log_file}")
        print(f"❌ Errores críticos: {len(self.critical_issues)}")
        print(f"⚠️ Advertencias: {len(self.warnings)}")
        
        if all_valid and len(self.critical_issues) == 0:
            print("✅ CONFIGURACIÓN VÁLIDA - Lista para deployment")
            return True
        else:
            print("❌ CONFIGURACIÓN INVÁLIDA - Requiere correcciones")
            return False

def main():
    """Función principal"""
    print("🔍 RAULI ENTERPRISE - VERCEL CONFIG VALIDATOR")
    print("Validación detallada de configuración y parámetros")
    print("")
    
    validator = VercelConfigValidator()
    
    if validator.execute_validation():
        print("\n✅ VALIDACIÓN EXITOSA")
        print("🎯 La configuración es válida y está lista para deployment")
        
        # Notificar por voz
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "¡Validación completada exitosamente! La configuración es correcta y está lista para deployment."
            ], cwd=r'C:\dev')
        except:
            pass
        
        # Notificar por Telegram
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\comunicador.py',
                '--telegram',
                f"✅ VALIDACIÓN COMPLETADA EXITOSAMENTE\n\n📊 **Resultados:**\n✅ Checks válidos: {len([r for r in validator.validation_results if r.status == 'ok'])}\n⚠️ Advertencias: {len(validator.warnings)}\n❌ Errores: {len(validator.critical_issues)}\n\n🎯 **Estado:** Configuración válida y lista para deployment\n🚀 **RAULI ENTERPRISE - Todo configurado correctamente**"
            ], cwd=r'C:\dev')
        except:
            pass
    
    else:
        print("\n❌ VALIDACIÓN FALLIDA")
        print("📊 Se encontraron errores que deben ser corregidos")
        
        # Notificar por voz
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "¡Validación fallida! Se encontraron errores críticos que deben ser corregidos antes del deployment."
            ], cwd=r'C:\dev')
        except:
            pass
        
        # Notificar por Telegram
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\comunicador.py',
                '--telegram',
                f"❌ VALIDACIÓN FALLIDA\n\n📊 **Resultados:**\n❌ Errores críticos: {len(validator.critical_issues)}\n⚠️ Advertencias: {len(validator.warnings)}\n✅ Checks válidos: {len([r for r in validator.validation_results if r.status == 'ok'])}\n\n🚨 **Acción requerida:** Corregir errores antes de deployment\n📊 **Revisar:** validation_report.md\n🔧 **RAULI ENTERPRISE - Requiere correcciones**"
            ], cwd=r'C:\dev')
        except:
            pass

if __name__ == "__main__":
    main()
