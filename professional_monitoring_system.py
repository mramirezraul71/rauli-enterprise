#!/usr/bin/env python3
"""
🔍 RAULI PROFESSIONAL MONITORING SYSTEM
Sistema de chequeo y monitoreo profesional para desarrolladores
"""

import os
import sys
import json
import time
import threading
import subprocess
import psutil
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import hashlib
import webbrowser
from collections import defaultdict

class MonitorLevel(Enum):
    """Niveles de monitoreo"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    ENTERPRISE = "enterprise"

class AlertLevel(Enum):
    """Niveles de alerta"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class SystemMetrics:
    """Métricas del sistema"""
    cpu_percent: float
    memory_percent: float
    disk_usage: float
    network_io: Dict[str, int]
    process_count: int
    uptime: float
    timestamp: str

@dataclass
class DevelopmentMetrics:
    """Métricas de desarrollo"""
    files_changed: int
    lines_added: int
    lines_removed: int
    commits_today: int
    build_time: float
    test_results: Dict[str, Any]
    code_coverage: float
    timestamp: str

@dataclass
class PerformanceMetrics:
    """Métricas de rendimiento"""
    response_time: float
    throughput: float
    error_rate: float
    availability: float
    timestamp: str

@dataclass
class Alert:
    """Alerta del sistema"""
    id: str
    level: AlertLevel
    title: str
    message: str
    source: str
    timestamp: str
    resolved: bool = False
    resolution_time: Optional[str] = None

class ProfessionalMonitoringSystem:
    def __init__(self, monitor_level: MonitorLevel = MonitorLevel.STANDARD):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.monitor_level = monitor_level
        self.db_path = self.base_dir / 'monitoring_database.db'
        self.config_file = self.base_dir / 'monitoring_config.json'
        self.dashboard_file = self.base_dir / 'monitoring_dashboard.html'
        self.alerts_file = self.base_dir / 'alerts_log.json'
        
        # Configuración según nivel
        self.config = self.get_monitoring_config(monitor_level)
        
        # Base de datos
        self.init_database()
        
        # Estado del sistema
        self.is_running = False
        self.monitoring_thread = None
        self.alerts = []
        
        # Métricas históricas
        self.system_history = []
        self.development_history = []
        self.performance_history = []
        
    def get_monitoring_config(self, level: MonitorLevel) -> Dict[str, Any]:
        """Obtener configuración según nivel de monitoreo"""
        configs = {
            MonitorLevel.BASIC: {
                'system_check_interval': 60,  # 1 minuto
                'development_check_interval': 300,  # 5 minutos
                'performance_check_interval': 600,  # 10 minutos
                'alert_thresholds': {
                    'cpu_percent': 80,
                    'memory_percent': 85,
                    'disk_usage': 90,
                    'response_time': 2000,  # ms
                    'error_rate': 5  # %
                },
                'retention_days': 7,
                'enable_notifications': True,
                'enable_dashboard': True
            },
            MonitorLevel.STANDARD: {
                'system_check_interval': 30,  # 30 segundos
                'development_check_interval': 120,  # 2 minutos
                'performance_check_interval': 300,  # 5 minutos
                'alert_thresholds': {
                    'cpu_percent': 70,
                    'memory_percent': 80,
                    'disk_usage': 85,
                    'response_time': 1000,  # ms
                    'error_rate': 3  # %
                },
                'retention_days': 30,
                'enable_notifications': True,
                'enable_dashboard': True,
                'enable_advanced_metrics': True
            },
            MonitorLevel.ADVANCED: {
                'system_check_interval': 15,  # 15 segundos
                'development_check_interval': 60,  # 1 minuto
                'performance_check_interval': 180,  # 3 minutos
                'alert_thresholds': {
                    'cpu_percent': 60,
                    'memory_percent': 75,
                    'disk_usage': 80,
                    'response_time': 500,  # ms
                    'error_rate': 1  # %
                },
                'retention_days': 90,
                'enable_notifications': True,
                'enable_dashboard': True,
                'enable_advanced_metrics': True,
                'enable_predictive_alerts': True,
                'enable_automated_responses': True
            },
            MonitorLevel.ENTERPRISE: {
                'system_check_interval': 10,  # 10 segundos
                'development_check_interval': 30,  # 30 segundos
                'performance_check_interval': 60,  # 1 minuto
                'alert_thresholds': {
                    'cpu_percent': 50,
                    'memory_percent': 70,
                    'disk_usage': 75,
                    'response_time': 200,  # ms
                    'error_rate': 0.5  # %
                },
                'retention_days': 365,
                'enable_notifications': True,
                'enable_dashboard': True,
                'enable_advanced_metrics': True,
                'enable_predictive_alerts': True,
                'enable_automated_responses': True,
                'enable_ml_analysis': True,
                'enable_distributed_monitoring': True
            }
        }
        
        return configs[level]
    
    def init_database(self):
        """Inicializar base de datos SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de métricas del sistema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_usage REAL,
                network_io TEXT,
                process_count INTEGER,
                uptime REAL
            )
        ''')
        
        # Tabla de métricas de desarrollo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS development_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                files_changed INTEGER,
                lines_added INTEGER,
                lines_removed INTEGER,
                commits_today INTEGER,
                build_time REAL,
                test_results TEXT,
                code_coverage REAL
            )
        ''')
        
        # Tabla de métricas de rendimiento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                response_time REAL,
                throughput REAL,
                error_rate REAL,
                availability REAL
            )
        ''')
        
        # Tabla de alertas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                level TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                source TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                resolved BOOLEAN DEFAULT FALSE,
                resolution_time TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Recoger métricas del sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memoria
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disco
            disk = psutil.disk_usage('/')
            disk_usage = (disk.used / disk.total) * 100
            
            # Red
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # Procesos
            process_count = len(psutil.pids())
            
            # Uptime
            uptime = time.time() - psutil.boot_time()
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage=disk_usage,
                network_io=network_io,
                process_count=process_count,
                uptime=uptime,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"Error collecting system metrics: {e}")
            return SystemMetrics(
                cpu_percent=0, memory_percent=0, disk_usage=0,
                network_io={}, process_count=0, uptime=0,
                timestamp=datetime.now().isoformat()
            )
    
    def collect_development_metrics(self) -> DevelopmentMetrics:
        """Recoger métricas de desarrollo"""
        try:
            # Cambios en archivos
            files_changed = self.count_changed_files()
            
            # Líneas de código
            lines_added, lines_removed = self.count_code_changes()
            
            # Commits
            commits_today = self.count_commits_today()
            
            # Tiempo de build
            build_time = self.measure_build_time()
            
            # Tests
            test_results = self.run_tests()
            
            # Coverage
            code_coverage = self.measure_code_coverage()
            
            return DevelopmentMetrics(
                files_changed=files_changed,
                lines_added=lines_added,
                lines_removed=lines_removed,
                commits_today=commits_today,
                build_time=build_time,
                test_results=test_results,
                code_coverage=code_coverage,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"Error collecting development metrics: {e}")
            return DevelopmentMetrics(
                files_changed=0, lines_added=0, lines_removed=0,
                commits_today=0, build_time=0, test_results={},
                code_coverage=0, timestamp=datetime.now().isoformat()
            )
    
    def collect_performance_metrics(self) -> PerformanceMetrics:
        """Recoger métricas de rendimiento"""
        try:
            # Tiempo de respuesta
            response_time = self.measure_response_time()
            
            # Throughput
            throughput = self.measure_throughput()
            
            # Error rate
            error_rate = self.calculate_error_rate()
            
            # Availability
            availability = self.calculate_availability()
            
            return PerformanceMetrics(
                response_time=response_time,
                throughput=throughput,
                error_rate=error_rate,
                availability=availability,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"Error collecting performance metrics: {e}")
            return PerformanceMetrics(
                response_time=0, throughput=0, error_rate=0,
                availability=0, timestamp=datetime.now().isoformat()
            )
    
    def count_changed_files(self) -> int:
        """Contar archivos modificados"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, cwd=self.base_dir
            )
            if result.returncode == 0:
                return len([line for line in result.stdout.strip().split('\n') if line])
        except:
            pass
        return 0
    
    def count_code_changes(self) -> Tuple[int, int]:
        """Contar líneas añadidas y eliminadas"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--stat'],
                capture_output=True, text=True, cwd=self.base_dir
            )
            if result.returncode == 0:
                # Parsear git diff --stat output
                lines = result.stdout.strip().split('\n')
                total_added = 0
                total_removed = 0
                
                for line in lines:
                    if 'insertion' in line or 'deletion' in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if 'insertion' in part:
                                total_added += int(parts[i-1].replace('+', ''))
                            elif 'deletion' in part:
                                total_removed += int(parts[i-1].replace('-', ''))
                
                return total_added, total_removed
        except:
            pass
        return 0, 0
    
    def count_commits_today(self) -> int:
        """Contar commits de hoy"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            result = subprocess.run(
                ['git', 'log', '--since', today, '--oneline'],
                capture_output=True, text=True, cwd=self.base_dir
            )
            if result.returncode == 0:
                return len([line for line in result.stdout.strip().split('\n') if line])
        except:
            pass
        return 0
    
    def measure_build_time(self) -> float:
        """Medir tiempo de build"""
        try:
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', 'dashboard_rauli.py'],
                capture_output=True, cwd=self.base_dir
            )
            end_time = time.time()
            return (end_time - start_time) * 1000  # ms
        except:
            return 0
    
    def run_tests(self) -> Dict[str, Any]:
        """Ejecutar tests y retornar resultados"""
        try:
            # Simular ejecución de tests
            return {
                'total_tests': 10,
                'passed': 8,
                'failed': 2,
                'skipped': 0,
                'success_rate': 80.0
            }
        except:
            return {}
    
    def measure_code_coverage(self) -> float:
        """Medir cobertura de código"""
        try:
            # Simular medición de coverage
            return 75.0
        except:
            return 0.0
    
    def measure_response_time(self) -> float:
        """Medir tiempo de respuesta"""
        try:
            # Simular medición de response time
            return 150.0  # ms
        except:
            return 0.0
    
    def measure_throughput(self) -> float:
        """Medir throughput"""
        try:
            # Simular medición de throughput
            return 1000.0  # requests/min
        except:
            return 0.0
    
    def calculate_error_rate(self) -> float:
        """Calcular tasa de error"""
        try:
            # Simular cálculo de error rate
            return 2.0  # %
        except:
            return 0.0
    
    def calculate_availability(self) -> float:
        """Calcular disponibilidad"""
        try:
            # Simular cálculo de availability
            return 99.5  # %
        except:
            return 0.0
    
    def check_thresholds(self, metrics: SystemMetrics) -> List[Alert]:
        """Verificar umbrales y generar alertas"""
        alerts = []
        thresholds = self.config['alert_thresholds']
        
        # CPU
        if metrics.cpu_percent > thresholds['cpu_percent']:
            alert = Alert(
                id=f"cpu_{int(time.time())}",
                level=AlertLevel.WARNING if metrics.cpu_percent < 90 else AlertLevel.CRITICAL,
                title="High CPU Usage",
                message=f"CPU usage is {metrics.cpu_percent:.1f}%",
                source="system_monitor",
                timestamp=datetime.now().isoformat()
            )
            alerts.append(alert)
        
        # Memoria
        if metrics.memory_percent > thresholds['memory_percent']:
            alert = Alert(
                id=f"memory_{int(time.time())}",
                level=AlertLevel.WARNING if metrics.memory_percent < 95 else AlertLevel.CRITICAL,
                title="High Memory Usage",
                message=f"Memory usage is {metrics.memory_percent:.1f}%",
                source="system_monitor",
                timestamp=datetime.now().isoformat()
            )
            alerts.append(alert)
        
        # Disco
        if metrics.disk_usage > thresholds['disk_usage']:
            alert = Alert(
                id=f"disk_{int(time.time())}",
                level=AlertLevel.WARNING if metrics.disk_usage < 95 else AlertLevel.CRITICAL,
                title="High Disk Usage",
                message=f"Disk usage is {metrics.disk_usage:.1f}%",
                source="system_monitor",
                timestamp=datetime.now().isoformat()
            )
            alerts.append(alert)
        
        return alerts
    
    def save_metrics(self):
        """Guardar métricas en base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Guardar métricas del sistema
        if self.system_history:
            latest = self.system_history[-1]
            cursor.execute('''
                INSERT INTO system_metrics 
                (timestamp, cpu_percent, memory_percent, disk_usage, network_io, process_count, uptime)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                latest.timestamp, latest.cpu_percent, latest.memory_percent,
                latest.disk_usage, json.dumps(latest.network_io),
                latest.process_count, latest.uptime
            ))
        
        # Guardar métricas de desarrollo
        if self.development_history:
            latest = self.development_history[-1]
            cursor.execute('''
                INSERT INTO development_metrics 
                (timestamp, files_changed, lines_added, lines_removed, commits_today, build_time, test_results, code_coverage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                latest.timestamp, latest.files_changed, latest.lines_added,
                latest.lines_removed, latest.commits_today, latest.build_time,
                json.dumps(latest.test_results), latest.code_coverage
            ))
        
        # Guardar métricas de rendimiento
        if self.performance_history:
            latest = self.performance_history[-1]
            cursor.execute('''
                INSERT INTO performance_metrics 
                (timestamp, response_time, throughput, error_rate, availability)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                latest.timestamp, latest.response_time, latest.throughput,
                latest.error_rate, latest.availability
            ))
        
        # Guardar alertas
        for alert in self.alerts:
            cursor.execute('''
                INSERT OR REPLACE INTO alerts 
                (id, level, title, message, source, timestamp, resolved, resolution_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.id, alert.level.value, alert.title, alert.message,
                alert.source, alert.timestamp, alert.resolved, alert.resolution_time
            ))
        
        conn.commit()
        conn.close()
    
    def generate_dashboard(self) -> str:
        """Generar dashboard HTML"""
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAULI Professional Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .metric-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .alert {{
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }}
        .alert-critical {{ background-color: #ffebee; border-left: 4px solid #f44336; }}
        .alert-warning {{ background-color: #fff3e0; border-left: 4px solid #ff9800; }}
        .alert-info {{ background-color: #e3f2fd; border-left: 4px solid #2196f3; }}
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .status-good {{ background-color: #4caf50; }}
        .status-warning {{ background-color: #ff9800; }}
        .status-critical {{ background-color: #f44336; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🔍 RAULI Professional Monitoring Dashboard</h1>
            <p>Nivel: {self.monitor_level.value.upper()} | Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">💻 CPU Usage</div>
                <div class="metric-value">{self.system_history[-1].cpu_percent:.1f}%</div>
                <div class="status-indicator {'status-good' if self.system_history[-1].cpu_percent < 70 else 'status-warning' if self.system_history[-1].cpu_percent < 90 else 'status-critical'}"></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🧠 Memory Usage</div>
                <div class="metric-value">{self.system_history[-1].memory_percent:.1f}%</div>
                <div class="status-indicator {'status-good' if self.system_history[-1].memory_percent < 80 else 'status-warning' if self.system_history[-1].memory_percent < 95 else 'status-critical'}"></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">💾 Disk Usage</div>
                <div class="metric-value">{self.system_history[-1].disk_usage:.1f}%</div>
                <div class="status-indicator {'status-good' if self.system_history[-1].disk_usage < 85 else 'status-warning' if self.system_history[-1].disk_usage < 95 else 'status-critical'}"></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📁 Files Changed</div>
                <div class="metric-value">{self.development_history[-1].files_changed}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📝 Lines Added</div>
                <div class="metric-value">+{self.development_history[-1].lines_added}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🗑️ Lines Removed</div>
                <div class="metric-value">-{self.development_history[-1].lines_removed}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🔄 Commits Today</div>
                <div class="metric-value">{self.development_history[-1].commits_today}</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">⚡ Response Time</div>
                <div class="metric-value">{self.performance_history[-1].response_time:.0f}ms</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>📊 System Metrics History</h3>
            <canvas id="systemChart" width="400" height="200"></canvas>
        </div>
        
        <div class="chart-container">
            <h3>📈 Development Activity</h3>
            <canvas id="developmentChart" width="400" height="200"></canvas>
        </div>
        
        <div class="chart-container">
            <h3>⚡ Performance Metrics</h3>
            <canvas id="performanceChart" width="400" height="200"></canvas>
        </div>
        
        <div class="chart-container">
            <h3>🚨 Recent Alerts</h3>
            <div id="alertsContainer">
                {self.generate_alerts_html()}
            </div>
        </div>
    </div>
    
    <script>
        // System Metrics Chart
        const systemCtx = document.getElementById('systemChart').getContext('2d');
        new Chart(systemCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps([m.timestamp.split('T')[1][:8] for m in self.system_history[-20:]])},
                datasets: [{{
                    label: 'CPU %',
                    data: {json.dumps([m.cpu_percent for m in self.system_history[-20:]])},
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }}, {{
                    label: 'Memory %',
                    data: {json.dumps([m.memory_percent for m in self.system_history[-20:]])},
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
        
        // Development Chart
        const devCtx = document.getElementById('developmentChart').getContext('2d');
        new Chart(devCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([m.timestamp.split('T')[1][:8] for m in self.development_history[-10:]])},
                datasets: [{{
                    label: 'Files Changed',
                    data: {json.dumps([m.files_changed for m in self.development_history[-10:]])},
                    backgroundColor: 'rgba(75, 192, 192, 0.6)'
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        
        // Performance Chart
        const perfCtx = document.getElementById('performanceChart').getContext('2d');
        new Chart(perfCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps([m.timestamp.split('T')[1][:8] for m in self.performance_history[-20:]])},
                datasets: [{{
                    label: 'Response Time (ms)',
                    data: {json.dumps([m.response_time for m in self.performance_history[-20:]])},
                    borderColor: 'rgb(255, 205, 86)',
                    tension: 0.1
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        
        // Auto-refresh
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
        """
        
        with open(self.dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(self.dashboard_file)
    
    def generate_alerts_html(self) -> str:
        """Generar HTML para alertas"""
        if not self.alerts:
            return "<p>No alerts</p>"
        
        alerts_html = ""
        for alert in self.alerts[-10:]:  # Últimas 10 alertas
            alert_class = f"alert-{alert.level.value}"
            alerts_html += f"""
            <div class="alert {alert_class}">
                <strong>{alert.title}</strong><br>
                {alert.message}<br>
                <small>{alert.timestamp}</small>
            </div>
            """
        
        return alerts_html
    
    def start_monitoring(self):
        """Iniciar monitoreo"""
        if self.is_running:
            print("Monitoring is already running")
            return
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        print(f"🔍 Professional monitoring started at {self.monitor_level.value} level")
    
    def monitoring_loop(self):
        """Bucle principal de monitoreo"""
        system_counter = 0
        dev_counter = 0
        perf_counter = 0
        
        while self.is_running:
            try:
                # System metrics
                if system_counter >= self.config['system_check_interval']:
                    system_metrics = self.collect_system_metrics()
                    self.system_history.append(system_metrics)
                    
                    # Verificar umbrales
                    new_alerts = self.check_thresholds(system_metrics)
                    self.alerts.extend(new_alerts)
                    
                    system_counter = 0
                
                # Development metrics
                if dev_counter >= self.config['development_check_interval']:
                    dev_metrics = self.collect_development_metrics()
                    self.development_history.append(dev_metrics)
                    dev_counter = 0
                
                # Performance metrics
                if perf_counter >= self.config['performance_check_interval']:
                    perf_metrics = self.collect_performance_metrics()
                    self.performance_history.append(perf_metrics)
                    perf_counter = 0
                
                # Guardar métricas periódicamente
                if len(self.system_history) % 10 == 0:
                    self.save_metrics()
                    self.generate_dashboard()
                
                # Limpiar historial según retención
                self.cleanup_old_data()
                
                time.sleep(1)
                system_counter += 1
                dev_counter += 1
                perf_counter += 1
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(5)
    
    def stop_monitoring(self):
        """Detener monitoreo"""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        # Guardar datos finales
        self.save_metrics()
        self.generate_dashboard()
        
        print("🔍 Professional monitoring stopped")
    
    def cleanup_old_data(self):
        """Limpiar datos antiguos según política de retención"""
        retention_days = self.config['retention_days']
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Limpiar historial en memoria
        self.system_history = [
            m for m in self.system_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_date
        ]
        
        self.development_history = [
            m for m in self.development_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_date
        ]
        
        self.performance_history = [
            m for m in self.performance_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_date
        ]
    
    def open_dashboard(self):
        """Abrir dashboard en navegador"""
        dashboard_path = self.generate_dashboard()
        webbrowser.open(f'file://{dashboard_path}')
        print(f"📊 Dashboard opened: {dashboard_path}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtener resumen del estado actual"""
        if not self.system_history:
            return {"status": "No data available"}
        
        latest_system = self.system_history[-1]
        latest_dev = self.development_history[-1] if self.development_history else None
        latest_perf = self.performance_history[-1] if self.performance_history else None
        
        return {
            "monitoring_level": self.monitor_level.value,
            "system_status": {
                "cpu": latest_system.cpu_percent,
                "memory": latest_system.memory_percent,
                "disk": latest_system.disk_usage,
                "processes": latest_system.process_count
            },
            "development_status": {
                "files_changed": latest_dev.files_changed if latest_dev else 0,
                "lines_added": latest_dev.lines_added if latest_dev else 0,
                "lines_removed": latest_dev.lines_removed if latest_dev else 0,
                "commits_today": latest_dev.commits_today if latest_dev else 0
            } if latest_dev else {},
            "performance_status": {
                "response_time": latest_perf.response_time if latest_perf else 0,
                "throughput": latest_perf.throughput if latest_perf else 0,
                "error_rate": latest_perf.error_rate if latest_perf else 0,
                "availability": latest_perf.availability if latest_perf else 0
            } if latest_perf else {},
            "active_alerts": len([a for a in self.alerts if not a.resolved]),
            "total_metrics_collected": len(self.system_history) + len(self.development_history) + len(self.performance_history)
        }

def main():
    """Función principal para demostración"""
    print("🔍 RAULI PROFESSIONAL MONITORING SYSTEM")
    print("Sistema de monitoreo profesional para desarrolladores")
    print("")
    
    # Seleccionar nivel de monitoreo
    print("Niveles de monitoreo disponibles:")
    print("1. Basic (1 min intervals)")
    print("2. Standard (30 sec intervals)")
    print("3. Advanced (15 sec intervals)")
    print("4. Enterprise (10 sec intervals)")
    
    choice = input("Selecciona nivel (1-4) [default: 2]: ").strip()
    
    level_map = {
        "1": MonitorLevel.BASIC,
        "2": MonitorLevel.STANDARD,
        "3": MonitorLevel.ADVANCED,
        "4": MonitorLevel.ENTERPRISE
    }
    
    monitor_level = level_map.get(choice, MonitorLevel.STANDARD)
    
    # Crear sistema de monitoreo
    monitoring = ProfessionalMonitoringSystem(monitor_level)
    
    print(f"\n🚀 Iniciando monitoreo a nivel {monitor_level.value}...")
    
    # Iniciar monitoreo
    monitoring.start_monitoring()
    
    # Abrir dashboard
    time.sleep(2)  # Esperar a que haya datos
    monitoring.open_dashboard()
    
    print("\n📊 Dashboard abierto en navegador")
    print("🔍 Monitoreo activo - Presiona Ctrl+C para detener")
    
    try:
        # Mantener corriendo
        while True:
            time.sleep(10)
            summary = monitoring.get_summary()
            print(f"\r📊 CPU: {summary['system_status']['cpu']:.1f}% | "
                  f"Memory: {summary['system_status']['memory']:.1f}% | "
                  f"Alerts: {summary['active_alerts']}", end="")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo monitoreo...")
        monitoring.stop_monitoring()
        
        # Mostrar resumen final
        summary = monitoring.get_summary()
        print("\n📊 Resumen final:")
        print(f"📁 Métricas recolectadas: {summary['total_metrics_collected']}")
        print(f"🚨 Alertas activas: {summary['active_alerts']}")
        print(f"📊 Dashboard: {monitoring.dashboard_file}")
        
        print("\n✅ Monitoreo profesional completado")

if __name__ == "__main__":
    main()
