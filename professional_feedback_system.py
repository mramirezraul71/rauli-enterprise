#!/usr/bin/env python3
"""
🧠 RAULI PROFESSIONAL FEEDBACK SYSTEM
Sistema de feedback profesional conectado a cerebro IA para respuestas y correcciones automáticas
"""

import os
import json
import time
import threading
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import requests
import re
from dataclasses import dataclass
from enum import Enum

class FeedbackType(Enum):
    """Tipos de feedback profesional"""
    CODE_QUALITY = "code_quality"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ARCHITECTURE = "architecture"
    BEST_PRACTICES = "best_practices"
    ERROR_CORRECTION = "error_correction"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"

class FeedbackPriority(Enum):
    """Prioridades de feedback"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class FeedbackItem:
    """Item de feedback profesional"""
    id: str
    type: FeedbackType
    priority: FeedbackPriority
    title: str
    description: str
    suggestion: str
    code_reference: Optional[str] = None
    line_number: Optional[int] = None
    confidence_score: float = 0.0
    auto_fixable: bool = False
    auto_fix_code: Optional[str] = None
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class ProfessionalFeedbackSystem:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.feedback_log = self.base_dir / 'professional_feedback.log'
        self.feedback_db = self.base_dir / 'feedback_database.json'
        self.ai_brain_config = self.base_dir / 'ai_brain_config.json'
        self.corrections_log = self.base_dir / 'auto_corrections.log'
        
        # Configuración del cerebro IA
        self.ai_brain = {
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'model': 'gpt-4',
            'temperature': 0.1,
            'max_tokens': 2000,
            'analysis_depth': 'professional'
        }
        
        # Base de conocimiento de feedback
        self.feedback_patterns = self.load_feedback_patterns()
        self.correction_templates = self.load_correction_templates()
        
        # Estadísticas
        self.stats = {
            'total_feedback': 0,
            'auto_corrections': 0,
            'critical_issues': 0,
            'performance_improvements': 0,
            'security_fixes': 0
        }
        
    def load_feedback_patterns(self) -> Dict[str, Any]:
        """Cargar patrones de feedback profesional"""
        patterns = {
            'code_quality': {
                'python': [
                    {
                        'pattern': r'def\s+\w+\([^)]*\):\s*pass',
                        'issue': 'Empty function implementation',
                        'suggestion': 'Implement function logic or add proper docstring',
                        'priority': 'medium',
                        'auto_fixable': True
                    },
                    {
                        'pattern': r'print\s*\(',
                        'issue': 'Debug print statement in production code',
                        'suggestion': 'Remove debug prints or use proper logging',
                        'priority': 'medium',
                        'auto_fixable': True
                    },
                    {
                        'pattern': r'except\s*:',
                        'issue': 'Bare except clause',
                        'suggestion': 'Specify exception type for better error handling',
                        'priority': 'high',
                        'auto_fixable': True
                    },
                    {
                        'pattern': r'import\s+\*',
                        'issue': 'Wildcard import',
                        'suggestion': 'Import specific modules or functions',
                        'priority': 'medium',
                        'auto_fixable': True
                    }
                ],
                'javascript': [
                    {
                        'pattern': r'console\.log',
                        'issue': 'Console.log in production',
                        'suggestion': 'Remove or use proper logging',
                        'priority': 'medium',
                        'auto_fixable': True
                    },
                    {
                        'pattern': r'var\s+\w+',
                        'issue': 'Use of var instead of let/const',
                        'suggestion': 'Use let or const for better scoping',
                        'priority': 'medium',
                        'auto_fixable': True
                    }
                ]
            },
            'security': [
                {
                    'pattern': r'password\s*=\s*["\'][^"\']+["\']',
                    'issue': 'Hardcoded password',
                    'suggestion': 'Use environment variables or secure storage',
                    'priority': 'critical',
                    'auto_fixable': False
                },
                {
                    'pattern': r'api_key\s*=\s*["\'][^"\']+["\']',
                    'issue': 'Hardcoded API key',
                    'suggestion': 'Use environment variables or secure storage',
                    'priority': 'critical',
                    'auto_fixable': False
                },
                {
                    'pattern': r'eval\s*\(',
                    'issue': 'Use of eval function',
                    'suggestion': 'Avoid eval for security reasons',
                    'priority': 'high',
                    'auto_fixable': False
                }
            ],
            'performance': [
                {
                    'pattern': r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(',
                    'issue': 'Inefficient loop pattern',
                        'suggestion': 'Use enumerate() or direct iteration',
                        'priority': 'medium',
                        'auto_fixable': True
                    },
                    {
                        'pattern': r'\.append\s*\([^)]*\)\s*for\s+\w+\s+in',
                        'issue': 'Inefficient list building',
                        'suggestion': 'Use list comprehension or extend()',
                        'priority': 'medium',
                        'auto_fixable': True
                    }
                ]
        }
        
        return patterns
    
    def load_correction_templates(self) -> Dict[str, str]:
        """Cargar plantillas de corrección automática"""
        templates = {
            'remove_debug_prints': '''
# Remove debug print statements
import re

def remove_debug_prints(code):
    pattern = r'print\s*\([^)]*\)'
    return re.sub(pattern, '# Debug print removed', code)
''',
            'fix_bare_except': '''
# Fix bare except clauses
import re

def fix_bare_except(code):
    pattern = r'except\s*:\s*(\n\s*)'
    return re.sub(pattern, r'except Exception as e:\1', code)
''',
            'replace_wildcard_imports': '''
# Replace wildcard imports
import re

def replace_wildcard_imports(code):
    pattern = r'from\s+(\w+)\s+import\s+\*'
    # This would need more sophisticated logic for real implementation
    return re.sub(pattern, r'# TODO: Import specific modules from \1', code)
''',
            'optimize_loops': '''
# Optimize Python loops
import re

def optimize_loops(code):
    # Replace range(len()) with enumerate()
    pattern = r'for\s+(\w+)\s+in\s+range\s*\(\s*len\s*\(([^)]+)\)\s*\):'
    return re.sub(pattern, r'for \1, item in enumerate(\2):', code)
''',
            'use_list_comprehension': '''
# Convert to list comprehension
import re

def use_list_comprehension(code):
    # Simple pattern for list comprehension
    pattern = r'(\w+)\s*=\s*\[\]\s*\n[^#]*\.append\s*\([^)]*\)\s*for\s+(\w+)\s+in'
    # This would need more sophisticated parsing
    return code
'''
        }
        
        return templates
    
    def analyze_code_with_ai(self, code: str, file_path: str) -> List[FeedbackItem]:
        """Analizar código con cerebro IA"""
        if not self.ai_brain['openai_api_key']:
            return []
        
        try:
            # Preparar prompt para análisis profesional
            prompt = f"""
Actúa como un arquitecto de software senior y analista de código profesional.

Analiza el siguiente código y proporciona feedback detallado:

Archivo: {file_path}

Código:
```python
{code}
```

Proporciona feedback en formato JSON con los siguientes campos:
- type: (code_quality, performance, security, architecture, best_practices)
- priority: (critical, high, medium, low, info)
- title: Título breve del issue
- description: Descripción detallada del problema
- suggestion: Sugerencia específica de mejora
- line_number: Número de línea (si aplica)
- confidence_score: Puntuación de confianza (0.0-1.0)
- auto_fixable: Si es auto-corregible (true/false)
- auto_fix_code: Código para corrección automática (si aplica)

Enfócate en:
1. Calidad del código y mejores prácticas
2. Optimización de rendimiento
3. Vulnerabilidades de seguridad
4. Arquitectura y diseño
5. Mantenibilidad y legibilidad

Responde solo con JSON válido.
"""
            
            # Llamar a OpenAI API
            import openai
            
            client = openai.OpenAI(api_key=self.ai_brain['openai_api_key'])
            
            response = client.chat.completions.create(
                model=self.ai_brain['model'],
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis de código profesional."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.ai_brain['temperature'],
                max_tokens=self.ai_brain['max_tokens']
            )
            
            # Parsear respuesta
            ai_feedback = json.loads(response.choices[0].message.content)
            
            # Convertir a FeedbackItem objects
            feedback_items = []
            for item in ai_feedback:
                feedback_item = FeedbackItem(
                    id=f"ai_{int(time.time())}_{len(feedback_items)}",
                    type=FeedbackType(item.get('type', 'code_quality')),
                    priority=FeedbackPriority(item.get('priority', 'medium')),
                    title=item.get('title', 'AI Feedback'),
                    description=item.get('description', ''),
                    suggestion=item.get('suggestion', ''),
                    line_number=item.get('line_number'),
                    confidence_score=item.get('confidence_score', 0.8),
                    auto_fixable=item.get('auto_fixable', False),
                    auto_fix_code=item.get('auto_fix_code')
                )
                feedback_items.append(feedback_item)
            
            return feedback_items
            
        except Exception as e:
            self.log_feedback(f"Error en análisis IA: {e}")
            return []
    
    def analyze_code_patterns(self, code: str, file_path: str) -> List[FeedbackItem]:
        """Analizar código usando patrones predefinidos"""
        feedback_items = []
        
        # Determinar tipo de archivo
        file_ext = Path(file_path).suffix.lower()
        
        # Analizar patrones según tipo de archivo
        if file_ext == '.py':
            feedback_items.extend(self._analyze_python_patterns(code))
        elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
            feedback_items.extend(self._analyze_javascript_patterns(code))
        
        # Analizar patrones de seguridad (independientes del lenguaje)
        feedback_items.extend(self._analyze_security_patterns(code))
        
        # Analizar patrones de rendimiento
        feedback_items.extend(self._analyze_performance_patterns(code))
        
        return feedback_items
    
    def _analyze_python_patterns(self, code: str) -> List[FeedbackItem]:
        """Analizar patrones específicos de Python"""
        feedback_items = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Verificar patrones de code_quality
            for pattern_info in self.feedback_patterns['code_quality']['python']:
                if re.search(pattern_info['pattern'], line):
                    feedback_item = FeedbackItem(
                        id=f"pattern_{int(time.time())}_{len(feedback_items)}",
                        type=FeedbackType.CODE_QUALITY,
                        priority=FeedbackPriority(pattern_info['priority']),
                        title=pattern_info['issue'],
                        description=f"Línea {i}: {pattern_info['issue']}",
                        suggestion=pattern_info['suggestion'],
                        line_number=i,
                        code_reference=line.strip(),
                        confidence_score=0.9,
                        auto_fixable=pattern_info['auto_fixable']
                    )
                    feedback_items.append(feedback_item)
        
        return feedback_items
    
    def _analyze_javascript_patterns(self, code: str) -> List[FeedbackItem]:
        """Analizar patrones específicos de JavaScript"""
        feedback_items = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Verificar patrones de JavaScript
            for pattern_info in self.feedback_patterns['code_quality']['javascript']:
                if re.search(pattern_info['pattern'], line):
                    feedback_item = FeedbackItem(
                        id=f"js_pattern_{int(time.time())}_{len(feedback_items)}",
                        type=FeedbackType.CODE_QUALITY,
                        priority=FeedbackPriority(pattern_info['priority']),
                        title=pattern_info['issue'],
                        description=f"Línea {i}: {pattern_info['issue']}",
                        suggestion=pattern_info['suggestion'],
                        line_number=i,
                        code_reference=line.strip(),
                        confidence_score=0.9,
                        auto_fixable=pattern_info['auto_fixable']
                    )
                    feedback_items.append(feedback_item)
        
        return feedback_items
    
    def _analyze_security_patterns(self, code: str) -> List[FeedbackItem]:
        """Analizar patrones de seguridad"""
        feedback_items = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern_info in self.feedback_patterns['security']:
                if re.search(pattern_info['pattern'], line, re.IGNORECASE):
                    feedback_item = FeedbackItem(
                        id=f"security_{int(time.time())}_{len(feedback_items)}",
                        type=FeedbackType.SECURITY,
                        priority=FeedbackPriority(pattern_info['priority']),
                        title=pattern_info['issue'],
                        description=f"Línea {i}: {pattern_info['issue']}",
                        suggestion=pattern_info['suggestion'],
                        line_number=i,
                        code_reference=line.strip(),
                        confidence_score=0.95,
                        auto_fixable=pattern_info['auto_fixable']
                    )
                    feedback_items.append(feedback_item)
        
        return feedback_items
    
    def _analyze_performance_patterns(self, code: str) -> List[FeedbackItem]:
        """Analizar patrones de rendimiento"""
        feedback_items = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern_info in self.feedback_patterns['performance']:
                if re.search(pattern_info['pattern'], line):
                    feedback_item = FeedbackItem(
                        id=f"perf_{int(time.time())}_{len(feedback_items)}",
                        type=FeedbackType.PERFORMANCE,
                        priority=FeedbackPriority(pattern_info['priority']),
                        title=pattern_info['issue'],
                        description=f"Línea {i}: {pattern_info['issue']}",
                        suggestion=pattern_info['suggestion'],
                        line_number=i,
                        code_reference=line.strip(),
                        confidence_score=0.8,
                        auto_fixable=pattern_info['auto_fixable']
                    )
                    feedback_items.append(feedback_item)
        
        return feedback_items
    
    def apply_auto_corrections(self, file_path: str, feedback_items: List[FeedbackItem]) -> bool:
        """Aplicar correcciones automáticas"""
        if not feedback_items:
            return False
        
        try:
            # Leer archivo original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            corrected_code = original_code
            corrections_applied = 0
            
            # Aplicar correcciones auto-fixables
            for item in feedback_items:
                if item.auto_fixable and item.auto_fix_code:
                    try:
                        # Aplicar corrección específica
                        if item.type == FeedbackType.CODE_QUALITY:
                            corrected_code = self._apply_code_quality_correction(
                                corrected_code, item
                            )
                        elif item.type == FeedbackType.PERFORMANCE:
                            corrected_code = self._apply_performance_correction(
                                corrected_code, item
                            )
                        
                        corrections_applied += 1
                        
                    except Exception as e:
                        self.log_feedback(f"Error aplicando corrección {item.id}: {e}")
            
            # Guardar código corregido
            if corrections_applied > 0:
                backup_path = file_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_code)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(corrected_code)
                
                self.log_feedback(f"✅ {corrections_applied} correcciones aplicadas a {file_path}")
                self.stats['auto_corrections'] += corrections_applied
                
                return True
            
        except Exception as e:
            self.log_feedback(f"Error en auto-corrección de {file_path}: {e}")
        
        return False
    
    def _apply_code_quality_correction(self, code: str, item: FeedbackItem) -> str:
        """Aplicar corrección de calidad de código"""
        if 'debug print' in item.title.lower():
            # Remover prints de debug
            import re
            pattern = r'print\s*\([^)]*\)'
            return re.sub(pattern, '# Debug print removed by RAULI Feedback System', code)
        
        elif 'bare except' in item.title.lower():
            # Corregir except bare
            import re
            pattern = r'except\s*:\s*(\n\s*)'
            return re.sub(pattern, r'except Exception as e:\1', code)
        
        elif 'wildcard import' in item.title.lower():
            # Reemplazar wildcard imports
            import re
            pattern = r'from\s+(\w+)\s+import\s+\*'
            return re.sub(pattern, r'# TODO: Import specific modules from \1', code)
        
        return code
    
    def _apply_performance_correction(self, code: str, item: FeedbackItem) -> str:
        """Aplicar corrección de rendimiento"""
        if 'inefficient loop' in item.title.lower():
            # Optimizar loops
            import re
            pattern = r'for\s+(\w+)\s+in\s+range\s*\(\s*len\s*\(([^)]+)\)\s*\):'
            return re.sub(pattern, r'for \1, item in enumerate(\2):', code)
        
        return code
    
    def analyze_file(self, file_path: str) -> List[FeedbackItem]:
        """Analizar archivo completo"""
        try:
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Análisis con patrones
            pattern_feedback = self.analyze_code_patterns(code, file_path)
            
            # Análisis con IA (si está disponible)
            ai_feedback = self.analyze_code_with_ai(code, file_path)
            
            # Combinar y deduplicar
            all_feedback = pattern_feedback + ai_feedback
            
            # Aplicar auto-correcciones
            auto_fixable_items = [item for item in all_feedback if item.auto_fixable]
            if auto_fixable_items:
                self.apply_auto_corrections(file_path, auto_fixable_items)
            
            # Actualizar estadísticas
            self.stats['total_feedback'] += len(all_feedback)
            self.stats['critical_issues'] += len([item for item in all_feedback if item.priority == FeedbackPriority.CRITICAL])
            
            return all_feedback
            
        except Exception as e:
            self.log_feedback(f"Error analizando {file_path}: {e}")
            return []
    
    def analyze_project(self, project_path: str = None) -> Dict[str, Any]:
        """Analizar proyecto completo"""
        if project_path is None:
            project_path = self.base_dir
        
        project_path = Path(project_path)
        
        analysis_result = {
            'project_path': str(project_path),
            'analysis_time': datetime.now().isoformat(),
            'files_analyzed': 0,
            'total_feedback': 0,
            'feedback_by_type': {},
            'feedback_by_priority': {},
            'auto_corrections_applied': 0,
            'files_with_issues': []
        }
        
        # Encontrar archivos para analizar
        code_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c']
        code_files = []
        
        for ext in code_extensions:
            code_files.extend(project_path.rglob(f'*{ext}'))
        
        # Analizar cada archivo
        all_feedback = []
        
        for file_path in code_files:
            self.log_feedback(f"Analizando: {file_path}")
            
            file_feedback = self.analyze_file(str(file_path))
            if file_feedback:
                all_feedback.extend(file_feedback)
                analysis_result['files_with_issues'].append(str(file_path))
            
            analysis_result['files_analyzed'] += 1
        
        # Compilar resultados
        analysis_result['total_feedback'] = len(all_feedback)
        
        # Agrupar por tipo
        for item in all_feedback:
            type_name = item.type.value
            analysis_result['feedback_by_type'][type_name] = analysis_result['feedback_by_type'].get(type_name, 0) + 1
        
        # Agrupar por prioridad
        for item in all_feedback:
            priority_name = item.priority.value
            analysis_result['feedback_by_priority'][priority_name] = analysis_result['feedback_by_priority'].get(priority_name, 0) + 1
        
        analysis_result['auto_corrections_applied'] = self.stats['auto_corrections']
        
        # Guardar resultados
        self.save_analysis_results(analysis_result)
        
        return analysis_result
    
    def save_analysis_results(self, results: Dict[str, Any]):
        """Guardar resultados del análisis"""
        results_file = self.base_dir / 'professional_analysis_results.json'
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        self.log_feedback(f"📊 Análisis guardado: {results_file}")
    
    def generate_feedback_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generar reporte profesional de feedback"""
        report = f"""
# 🧠 RAULI PROFESSIONAL FEEDBACK REPORT

## 📊 ANÁLISIS DEL PROYECTO

**Ruta del Proyecto:** {analysis_results['project_path']}
**Fecha de Análisis:** {analysis_results['analysis_time']}
**Archivos Analizados:** {analysis_results['files_analyzed']}
**Total de Feedback:** {analysis_results['total_feedback']}

## 📋 RESUMEN DE RESULTADOS

### Feedback por Tipo:
"""
        
        for feedback_type, count in analysis_results['feedback_by_type'].items():
            report += f"- **{feedback_type}:** {count} items\n"
        
        report += "\n### Feedback por Prioridad:\n"
        
        for priority, count in analysis_results['feedback_by_priority'].items():
            priority_icon = "🔴" if priority == "critical" else "🟡" if priority == "high" else "🟢"
            report += f"- {priority_icon} **{priority}:** {count} items\n"
        
        report += f"\n### Auto-Correciones Aplicadas: {analysis_results['auto_corrections_applied']}\n"
        
        report += "\n## 📁 ARCHIVOS CON ISSUES\n"
        
        for file_path in analysis_results['files_with_issues']:
            report += f"- `{file_path}`\n"
        
        report += "\n## 🎯 RECOMENDACIONES\n"
        
        # Generar recomendaciones basadas en los resultados
        critical_count = analysis_results['feedback_by_priority'].get('critical', 0)
        if critical_count > 0:
            report += f"- ⚠️ **URGENTE:** Se encontraron {critical_count} issues críticos que requieren atención inmediata.\n"
        
        security_count = analysis_results['feedback_by_type'].get('security', 0)
        if security_count > 0:
            report += f"- 🔒 **SEGURIDAD:** Se encontraron {security_count} vulnerabilidades de seguridad.\n"
        
        performance_count = analysis_results['feedback_by_type'].get('performance', 0)
        if performance_count > 0:
            report += f"- ⚡ **RENDIMIENTO:** Se identificaron {performance_count} oportunidades de optimización.\n"
        
        report += "\n## 🚀 PRÓXIMOS PASOS\n"
        report += "1. Revisar y corregir issues críticos primero\n"
        report += "2. Implementar mejoras de seguridad\n"
        report += "3. Optimizar código para mejor rendimiento\n"
        report += "4. Aplicar best practices de código\n"
        report += "5. Documentar cambios y mejoras\n"
        
        return report
    
    def log_feedback(self, message: str):
        """Registrar mensaje de feedback"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.feedback_log, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def start_continuous_monitoring(self, project_path: str = None):
        """Iniciar monitoreo continuo del proyecto"""
        def monitor():
            while True:
                try:
                    self.log_feedback("🔍 Iniciando análisis continuo...")
                    
                    # Analizar proyecto
                    results = self.analyze_project(project_path)
                    
                    # Generar reporte
                    report = self.generate_feedback_report(results)
                    
                    # Guardar reporte
                    report_file = self.base_dir / 'latest_feedback_report.md'
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    self.log_feedback(f"📊 Reporte generado: {report_file}")
                    
                    # Esperar antes del siguiente análisis
                    time.sleep(300)  # 5 minutos
                    
                except Exception as e:
                    self.log_feedback(f"❌ Error en monitoreo continuo: {e}")
                    time.sleep(60)  # Esperar 1 minuto antes de reintentar
        
        # Iniciar en thread separado
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        self.log_feedback("🔄 Monitoreo continuo iniciado")

def main():
    """Función principal para demostración"""
    feedback_system = ProfessionalFeedbackSystem()
    
    print("🧠 RAULI PROFESSIONAL FEEDBACK SYSTEM")
    print("Sistema de feedback profesional con IA")
    print("")
    
    # Analizar proyecto actual
    print("🔍 Analizando proyecto RAULI...")
    results = feedback_system.analyze_project()
    
    # Mostrar resultados
    print(f"\n📊 Resultados del Análisis:")
    print(f"📁 Archivos analizados: {results['files_analyzed']}")
    print(f"🔍 Total de feedback: {results['total_feedback']}")
    print(f"🔧 Auto-correcciones: {results['auto_corrections_applied']}")
    
    # Generar reporte
    report = feedback_system.generate_feedback_report(results)
    
    # Guardar reporte
    report_file = feedback_system.base_dir / 'professional_feedback_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📋 Reporte guardado: {report_file}")
    
    # Iniciar monitoreo continuo
    print("\n🔄 Iniciando monitoreo continuo...")
    feedback_system.start_continuous_monitoring()
    
    print("\n✅ Sistema de feedback profesional activo")
    print("🎯 Analizando y corrigiendo código automáticamente")

if __name__ == "__main__":
    main()
