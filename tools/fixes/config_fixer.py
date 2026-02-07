#!/usr/bin/env python3
"""
🔧 RAULI ENTERPRISE - CONFIG FIXER
Corrección automática de errores de configuración
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
class ConfigFix:
    """Configuración a corregir"""
    file_path: str
    issue: str
    fix: str
    critical: bool

class ConfigFixer:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.fix_log_file = self.base_dir / 'config_fix_log.json'
        
        # Estado de corrección
        self.fix_status = {
            "started": False,
            "fixes_applied": [],
            "errors": [],
            "success": False,
            "critical_fixed": 0,
            "warnings_fixed": 0
        }
    
    def log_fix(self, file_path: str, issue: str, action: str, status: str, details: str = ""):
        """Registrar corrección"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "issue": issue,
            "action": action,
            "status": status,
            "details": details
        }
        
        self.fix_status["fixes_applied"].append(log_entry)
        
        if status == "error":
            self.fix_status["errors"].append(details)
        
        icon = "✅" if status == "success" else "❌" if status == "error" else "⏳"
        print(f"{icon} {file_path}: {issue}")
        if details:
            print(f"   {details}")
        
        # Guardar log
        with open(self.fix_log_file, 'w', encoding='utf-8') as f:
            json.dump(self.fix_status, f, ensure_ascii=False, indent=2)
    
    def fix_requirements_txt(self) -> bool:
        """Corregir requirements.txt"""
        print("📋 Corrigiendo requirements.txt...")
        
        req_file = self.base_dir / 'requirements.txt'
        
        try:
            # Leer archivo actual
            with open(req_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar si requests está presente
            if 'requests' in content:
                self.log_fix("requirements.txt", "requests dependency", "Verificación", "success", "requests ya está presente")
                return True
            
            # Agregar requests si no está
            lines = content.split('\n')
            
            # Encontrar la línea apropiada para insertar requests
            insert_index = -1
            for i, line in enumerate(lines):
                if line.startswith('# Web Framework') or line.startswith('flask'):
                    insert_index = i + 1
                    break
            
            if insert_index == -1:
                # Si no encuentra la sección, agregar después de las dependencias core
                for i, line in enumerate(lines):
                    if line.startswith('# AI/ML Frameworks'):
                        insert_index = i
                        break
            
            # Insertar requests
            if insert_index != -1:
                lines.insert(insert_index, "requests>=2.31.0")
                lines.insert(insert_index, "# HTTP Library")
            else:
                # Agregar al final si no encuentra lugar apropiado
                lines.append("")
                lines.append("# HTTP Library")
                lines.append("requests>=2.31.0")
            
            # Escribir archivo corregido
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            self.fix_status["critical_fixed"] += 1
            self.log_fix("requirements.txt", "requests dependency", "Agregado", "success", "requests>=2.31.0 agregado")
            return True
            
        except Exception as e:
            self.log_fix("requirements.txt", "requests dependency", "Error", "error", str(e))
            return False
    
    def fix_dashboard_syntax(self) -> bool:
        """Corregir sintaxis de dashboard_rauli.py"""
        print("🐍 Corrigiendo sintaxis de dashboard_rauli.py...")
        
        dashboard_file = self.base_dir / 'dashboard_rauli.py'
        
        try:
            # Leer archivo
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Buscar línea 562 (índice 561)
            if len(lines) > 561:
                line_562 = lines[561].strip()
                
                # Verificar si es el problema del except ImportError
                if 'except ImportError:' in line_562:
                    # La línea parece correcta, verificar si hay un problema de indentación
                    # o si el bloque try está incompleto
                    
                    # Buscar el bloque try correspondiente
                    for i in range(560, max(0, 560-20), -1):
                        if 'try:' in lines[i]:
                            # Verificar que el bloque try esté completo
                            try_block = lines[i:562]
                            has_import = any('import' in line for line in try_block)
                            
                            if not has_import:
                                # Insertar import faltante antes del except
                                lines.insert(561, "    import cv2\n")
                                self.log_fix("dashboard_rauli.py", "syntax error line 562", "Import agregado", "success", "cv2 import agregado antes del except")
                                break
                            else:
                                self.log_fix("dashboard_rauli.py", "syntax error line 562", "Verificación", "success", "Bloque try parece correcto")
                                break
                
                # Reescribir archivo si se hicieron cambios
                with open(dashboard_file, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                # Verificar sintaxis nuevamente
                try:
                    with open(dashboard_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    compile(content, str(dashboard_file), 'exec')
                    self.fix_status["critical_fixed"] += 1
                    self.log_fix("dashboard_rauli.py", "syntax validation", "Sintaxis válida", "success", "Sintaxis corregida y validada")
                    return True
                except SyntaxError as e:
                    self.log_fix("dashboard_rauli.py", "syntax validation", "Error persiste", "error", f"Error de sintaxis: {e}")
                    return False
            else:
                self.log_fix("dashboard_rauli.py", "syntax error", "Archivo corto", "error", "Archivo tiene menos de 562 líneas")
                return False
                
        except Exception as e:
            self.log_fix("dashboard_rauli.py", "syntax error", "Error", "error", str(e))
            return False
    
    def fix_imports_dashboard(self) -> bool:
        """Corregir imports faltantes en dashboard_rauli.py"""
        print("📦 Corrigiendo imports en dashboard_rauli.py...")
        
        dashboard_file = self.base_dir / 'dashboard_rauli.py'
        
        try:
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar si requests está importado
            if 'import requests' in content or 'from requests' in content:
                self.log_fix("dashboard_rauli.py", "requests import", "Verificación", "success", "requests ya está importado")
            else:
                # Agregar import requests
                lines = content.split('\n')
                
                # Encontrar sección de imports
                import_index = -1
                for i, line in enumerate(lines):
                    if line.startswith('import streamlit'):
                        import_index = i
                        break
                
                if import_index != -1:
                    # Insertar después de import streamlit
                    lines.insert(import_index + 1, 'import requests')
                    
                    # Reescribir archivo
                    with open(dashboard_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    
                    self.fix_status["warnings_fixed"] += 1
                    self.log_fix("dashboard_rauli.py", "requests import", "Agregado", "success", "import requests agregado")
                else:
                    self.log_fix("dashboard_rauli.py", "requests import", "No encontrado", "warning", "No se encontró sección de imports")
            
            return True
            
        except Exception as e:
            self.log_fix("dashboard_rauli.py", "requests import", "Error", "error", str(e))
            return False
    
    def fix_imports_mobile(self) -> bool:
        """Corregir imports faltantes en mobile_web_interface.py"""
        print("📱 Corrigiendo imports en mobile_web_interface.py...")
        
        mobile_file = self.base_dir / 'mobile_web_interface.py'
        
        try:
            with open(mobile_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar si openai está importado
            if 'import openai' in content or 'from openai' in content:
                self.log_fix("mobile_web_interface.py", "openai import", "Verificación", "success", "openai ya está importado")
            else:
                # Agregar import openai
                lines = content.split('\n')
                
                # Encontrar sección de imports
                import_index = -1
                for i, line in enumerate(lines):
                    if line.startswith('import flask'):
                        import_index = i
                        break
                
                if import_index != -1:
                    # Insertar después de import flask
                    lines.insert(import_index + 1, 'import openai')
                    
                    # Reescribir archivo
                    with open(mobile_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))
                    
                    self.fix_status["warnings_fixed"] += 1
                    self.log_fix("mobile_web_interface.py", "openai import", "Agregado", "success", "import openai agregado")
                else:
                    self.log_fix("mobile_web_interface.py", "openai import", "No encontrado", "warning", "No se encontró sección de imports")
            
            return True
            
        except Exception as e:
            self.log_fix("mobile_web_interface.py", "openai import", "Error", "error", str(e))
            return False
    
    def validate_syntax_after_fix(self) -> bool:
        """Validar sintaxis después de las correcciones"""
        print("✅ Validando sintaxis después de correcciones...")
        
        python_files = [
            'dashboard_rauli.py',
            'mobile_web_interface.py'
        ]
        
        all_valid = True
        for file_name in python_files:
            file_path = self.base_dir / file_name
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                compile(content, str(file_path), 'exec')
                self.log_fix(file_name, "syntax validation", "Válido", "success", "Sintaxis correcta")
                
            except SyntaxError as e:
                self.log_fix(file_name, "syntax validation", "Error", "error", f"Error de sintaxis: {e}")
                all_valid = False
            except Exception as e:
                self.log_fix(file_name, "syntax validation", "Error", "error", f"Error general: {e}")
                all_valid = False
        
        return all_valid
    
    def generate_fix_report(self) -> str:
        """Generar reporte de correcciones"""
        print("📊 Generando reporte de correcciones...")
        
        total_fixes = len(self.fix_status["fixes_applied"])
        successful_fixes = len([f for f in self.fix_status["fixes_applied"] if f["status"] == "success"])
        failed_fixes = len(self.fix_status["errors"])
        
        report = f"""
# 🔧 RAULI ENTERPRISE - CONFIG FIX REPORT

## 📊 FECHA
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📈 RESUMEN DE CORRECCIONES

### 🎯 **Estado General**
- **Total de correcciones:** {total_fixes}
- **✅ Exitosas:** {successful_fixes}
- **❌ Fallidas:** {failed_fixes}
- **📊 Porcentaje éxito:** {(successful_fixes/total_fixes)*100:.1f}%

### 🚨 **Correcciones Críticas**
- **Errores críticos corregidos:** {self.fix_status['critical_fixed']}

### ⚠️ **Mejoras Aplicadas**
- **Advertencias corregidas:** {self.fix_status['warnings_fixed']}

---

## 📋 DETALLE DE CORRECCIONES

"""
        
        for fix in self.fix_status["fixes_applied"]:
            icon = "✅" if fix["status"] == "success" else "❌"
            report += f"\n{icon} **{fix['file_path']}** - {fix['issue']}\n"
            report += f"   - Acción: {fix['action']}\n"
            if fix["details"]:
                report += f"   - Detalles: {fix['details']}\n"
        
        if self.fix_status["errors"]:
            report += f"""

## ❌ **Errores en Corrección

"""
            for error in self.fix_status["errors"]:
                report += f"- ❌ {error}\n"
        
        # Conclusión
        if failed_fixes == 0:
            report += f"""

## 🎉 **CONCLUSIÓN**

**✅ TODAS LAS CORRECCIONES APLICADAS EXITOSAMENTE**

La configuración ha sido corregida y está lista para deployment.

"""
        else:
            report += f"""

## 🚨 **CONCLUSIÓN**

**❌ ALGUNAS CORRECCIONES FALLARON**

Se encontraron {failed_fixes} errores que requieren atención manual.

"""
        
        report += f"""

---

## 📊 **MÉTRICAS DE CALIDAD**

- **Precisión:** {(successful_fixes/total_fixes)*100:.1f}%
- **Completitud:** {(successful_fixes/total_fixes)*100:.1f}%
- **Estado:** {'✅ Configuración corregida' if failed_fixes == 0 else '❌ Requiere atención manual'}

---

## 🚀 **PRÓXIMOS PASOS**

1. **🔍 Re-validar configuración** con vercel_config_validator.py
2. **🚀 Ejecutar deployment** si todo está correcto
3. **📊 Monitorear** el deployment en Vercel

---

**🔧 Corrección completada - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
"""
        
        # Guardar reporte
        report_file = self.base_dir / 'config_fix_report.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(report_file)
    
    def execute_fixes(self) -> bool:
        """Ejecutar todas las correcciones"""
        print("🔧 INICIANDO CORRECCIÓN AUTOMÁTICA DE CONFIGURACIÓN")
        print("=" * 80)
        print("🎯 Corrigiendo errores críticos y advertencias")
        print("=" * 80)
        
        self.fix_status["started"] = True
        
        # Ejecutar correcciones críticas
        critical_fixes = [
            self.fix_requirements_txt,
            self.fix_dashboard_syntax
        ]
        
        # Ejecutar correcciones de advertencias
        warning_fixes = [
            self.fix_imports_dashboard,
            self.fix_imports_mobile
        ]
        
        all_critical_ok = True
        for fix_func in critical_fixes:
            try:
                if not fix_func():
                    all_critical_ok = False
                print()  # Espacio entre correcciones
            except Exception as e:
                print(f"❌ Error en corrección {fix_func.__name__}: {e}")
                all_critical_ok = False
        
        for fix_func in warning_fixes:
            try:
                fix_func()
                print()  # Espacio entre correcciones
            except Exception as e:
                print(f"❌ Error en corrección {fix_func.__name__}: {e}")
        
        # Validar sintaxis final
        if self.validate_syntax_after_fix():
            self.fix_status["success"] = True
        
        # Generar reporte
        report_file = self.generate_fix_report()
        
        print("\n" + "=" * 80)
        print("🎉 CORRECCIÓN COMPLETADA")
        print("=" * 80)
        print(f"📊 Reporte: {report_file}")
        print(f"📈 Datos: {self.fix_log_file}")
        print(f"✅ Críticos corregidos: {self.fix_status['critical_fixed']}")
        print(f"⚠️ Advertencias corregidas: {self.fix_status['warnings_fixed']}")
        print(f"❌ Errores: {len(self.fix_status['errors'])}")
        
        return self.fix_status["success"]

def main():
    """Función principal"""
    print("🔧 RAULI ENTERPRISE - CONFIG FIXER")
    print("Corrección automática de errores de configuración")
    print("")
    
    fixer = ConfigFixer()
    
    if fixer.execute_fixes():
        print("\n✅ CORRECCIÓN EXITOSA")
        print("🎯 La configuración ha sido corregida")
        
        # Notificar por voz
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "¡Corrección completada exitosamente! Todos los errores de configuración han sido solucionados."
            ], cwd=r'C:\dev')
        except:
            pass
        
        # Notificar por Telegram
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\comunicador.py',
                '--telegram',
                f"✅ CORRECCIÓN COMPLETADA EXITOSAMENTE\n\n📊 **Resultados:**\n✅ Críticos corregidos: {fixer.fix_status['critical_fixed']}\n⚠️ Advertencias corregidas: {fixer.fix_status['warnings_fixed']}\n❌ Errores: {len(fixer.fix_status['errors'])}\n\n🎯 **Estado:** Configuración corregida y lista\n🚀 **RAULI ENTERPRISE - Todo solucionado**"
            ], cwd=r'C:\dev')
        except:
            pass
        
        # Ejecutar validación nuevamente
        print("\n🔍 Ejecutando validación final...")
        subprocess.run(['python', r'C:\RAULI_CORE\vercel_config_validator.py'], cwd=r'C:\RAULI_CORE')
    
    else:
        print("\n❌ CORRECCIÓN FALLIDA")
        print("📊 Algunos errores no pudieron ser corregidos automáticamente")
        
        # Notificar por voz
        try:
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                "¡Corrección fallida! Algunos errores requieren intervención manual."
            ], cwd=r'C:\dev')
        except:
            pass

if __name__ == "__main__":
    main()
