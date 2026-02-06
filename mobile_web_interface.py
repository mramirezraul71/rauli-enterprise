#!/usr/bin/env python3
"""
📱 RAULI Mobile Web Interface
Interface web para acceso móvil al dashboard RAULI
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import requests
import threading
import time
from security_hardening import InputValidator, SecurityMiddleware, SecurityLevel, ThreatLevel

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'mobile_templates'))
CORS(app)

class RAULIMobileWebInterface:
    def __init__(self):
        self.dashboard_url = "http://localhost:8502"
        self.mobile_users = {}
        self.status = {
            'online': True,
            'last_update': datetime.now().isoformat(),
            'connected_users': 0
        }
        
        # Inicializar seguridad
        self.input_validator = InputValidator()
        self.security_middleware = SecurityMiddleware()
    
    def get_dashboard_status(self):
        """Obtener estado del dashboard principal"""
        try:
            response = requests.get(f"{self.dashboard_url}/_stcore/health", timeout=5)
            return {
                'status': 'online' if response.status_code == 200 else 'offline',
                'url': self.dashboard_url,
                'timestamp': datetime.now().isoformat()
            }
        except:
            return {
                'status': 'offline',
                'url': self.dashboard_url,
                'timestamp': datetime.now().isoformat()
            }
    
    def register_mobile_user(self, user_id, device_info):
        """Registrar usuario móvil"""
        self.mobile_users[user_id] = {
            'device_info': device_info,
            'connected_at': datetime.now(),
            'last_activity': datetime.now()
        }
        self.status['connected_users'] = len(self.mobile_users)
        return {'status': 'registered', 'user_id': user_id}

mobile_interface = RAULIMobileWebInterface()

@app.route('/')
def mobile_home():
    """Página principal móvil"""
    return render_template('mobile_home.html')

@app.route('/mobile')
def mobile_interface():
    """Interface móvil optimizada"""
    return render_template('mobile_dashboard.html')

@app.route('/api/status')
def api_status():
    """API de estado"""
    return jsonify({
        'system': mobile_interface.status,
        'dashboard': mobile_interface.get_dashboard_status(),
        'users': len(mobile_interface.mobile_users)
    })

@app.route('/api/register', methods=['POST'])
def register_user():
    """Registrar usuario móvil con validación de seguridad"""
    try:
        data = request.json
        user_id = data.get('user_id', f"user_{int(time.time())}")
        device_info = data.get('device_info', 'unknown')
        
        # Validar entradas
        user_id_validation = mobile_interface.input_validator.validate_input(
            str(user_id), 'username', SecurityLevel.MEDIUM
        )
        
        device_validation = mobile_interface.input_validator.validate_input(
            device_info, 'safe_text', SecurityLevel.LOW
        )
        
        if not user_id_validation['valid'] or not device_validation['valid']:
            return jsonify({
                'status': 'error',
                'message': 'Entrada inválida',
                'errors': user_id_validation['errors'] + device_validation['errors']
            }), 400
        
        # Rate limiting
        if not mobile_interface.security_middleware.rate_limit_check(
            user_id_validation['sanitized'], 'register', 5, 300
        ):
            return jsonify({
                'status': 'error',
                'message': 'Too many registration attempts'
            }), 429
        
        result = mobile_interface.register_mobile_user(
            user_id_validation['sanitized'], 
            device_validation['sanitized']
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Registration failed'
        }), 500

@app.route('/api/dashboard/iframe')
def dashboard_iframe():
    """iframe del dashboard principal"""
    return render_template('dashboard_iframe.html')

def create_mobile_templates():
    """Crear templates HTML para móvil"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'mobile_templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Template principal móvil
    mobile_home_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 RAULI Mobile</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .container { max-width: 100%; padding: 20px; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .card { background: white; border-radius: 15px; padding: 20px; margin: 15px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .card h3 { color: #333; margin-bottom: 15px; font-size: 1.3em; }
        .btn { display: block; width: 100%; padding: 15px; margin: 10px 0; border: none; border-radius: 10px; font-size: 1.1em; cursor: pointer; transition: all 0.3s; text-decoration: none; text-align: center; }
        .btn-primary { background: #667eea; color: white; }
        .btn-success { background: #48bb78; color: white; }
        .btn-info { background: #4299e1; color: white; }
        .btn-warning { background: #ed8936; color: white; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .status { display: flex; justify-content: space-between; align-items: center; padding: 10px; background: #f7fafc; border-radius: 8px; margin: 10px 0; }
        .status-online { color: #48bb78; font-weight: bold; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        @media (max-width: 480px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 RAULI Mobile</h1>
            <p>Asistente IA Enterprise en tu móvil</p>
        </div>
        
        <div class="card">
            <h3>📊 Estado del Sistema</h3>
            <div class="status">
                <span>Dashboard Principal</span>
                <span class="status-online">🟢 Online</span>
            </div>
            <div class="status">
                <span>API Services</span>
                <span class="status-online">🟢 Active</span>
            </div>
            <div class="status">
                <span>Mobile Bridge</span>
                <span class="status-online">🟢 Connected</span>
            </div>
        </div>
        
        <div class="card">
            <h3>🚀 Acceso Rápido</h3>
            <a href="/mobile" class="btn btn-primary">📱 Dashboard Móvil</a>
            <a href="/api/dashboard/iframe" class="btn btn-success">🖥️ Dashboard Completo</a>
            <a href="#" onclick="openChat()" class="btn btn-info">💬 Chat con RAULI</a>
            <a href="#" onclick="openVoice()" class="btn btn-warning">🎤 Comando de Voz</a>
        </div>
        
        <div class="card">
            <h3>🛠️ Funciones Disponibles</h3>
            <div class="grid">
                <div class="status">
                    <span>💬 Chat IA</span>
                    <span>✅</span>
                </div>
                <div class="status">
                    <span>👁️ Visión</span>
                    <span>✅</span>
                </div>
                <div class="status">
                    <span>📊 Análisis</span>
                    <span>✅</span>
                </div>
                <div class="status">
                    <span>🎮 Control</span>
                    <span>✅</span>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>📱 Enlaces Directos</h3>
            <a href="http://localhost:8502" class="btn btn-primary" target="_blank">🌐 Dashboard Web</a>
            <a href="http://localhost:3000" class="btn btn-info" target="_blank">📈 Grafana</a>
            <a href="http://localhost:9090" class="btn btn-warning" target="_blank">🔍 Prometheus</a>
        </div>
    </div>
    
    <script>
        function openChat() { alert('Chat IA: ¡Hola! Soy RAULI, tu asistente enterprise. ¿En qué puedo ayudarte?'); }
        function openVoice() { alert('Voz: Di "Hola RAULI" para activar comando de voz'); }
        
        // Auto-refresh status
        setInterval(() => {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => console.log('Status updated:', data));
        }, 30000);
    </script>
</body>
</html>
"""
    
    # Template dashboard móvil
    mobile_dashboard_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 RAULI Mobile Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #1a202c; color: white; }
        .header { background: #2d3748; padding: 15px; text-align: center; border-bottom: 3px solid #667eea; }
        .header h1 { font-size: 1.8em; }
        .nav { display: flex; justify-content: space-around; background: #2d3748; padding: 10px; position: sticky; top: 0; z-index: 100; }
        .nav-item { padding: 10px; text-align: center; cursor: pointer; border-radius: 8px; transition: background 0.3s; }
        .nav-item:hover, .nav-item.active { background: #667eea; }
        .content { padding: 20px; }
        .card { background: #2d3748; border-radius: 10px; padding: 15px; margin: 15px 0; }
        .card h3 { color: #667eea; margin-bottom: 10px; }
        .status-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #4a5568; }
        .status-value { color: #48bb78; font-weight: bold; }
        .btn { background: #667eea; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; margin: 5px 0; width: 100%; }
        .iframe-container { width: 100%; height: 600px; border: none; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 RAULI Mobile Dashboard</h1>
    </div>
    
    <div class="nav">
        <div class="nav-item active" onclick="showSection('status')">📊 Estado</div>
        <div class="nav-item" onclick="showSection('chat')">💬 Chat</div>
        <div class="nav-item" onclick="showSection('vision')">👁️ Visión</div>
        <div class="nav-item" onclick="showSection('control')">🎮 Control</div>
    </div>
    
    <div class="content">
        <div id="status" class="section">
            <div class="card">
                <h3>📊 Estado del Sistema</h3>
                <div class="status-item">
                    <span>Dashboard Principal</span>
                    <span class="status-value">🟢 Online</span>
                </div>
                <div class="status-item">
                    <span>API Services</span>
                    <span class="status-value">🟢 Active</span>
                </div>
                <div class="status-item">
                    <span>Conectados</span>
                    <span class="status-value">1 usuario</span>
                </div>
                <div class="status-item">
                    <span>Última actualización</span>
                    <span class="status-value">Ahora</span>
                </div>
            </div>
            
            <div class="card">
                <h3>📈 Métricas</h3>
                <div class="status-item">
                    <span>CPU Usage</span>
                    <span class="status-value">45%</span>
                </div>
                <div class="status-item">
                    <span>Memory</span>
                    <span class="status-value">2.1 GB</span>
                </div>
                <div class="status-item">
                    <span>Requests/min</span>
                    <span class="status-value">127</span>
                </div>
            </div>
        </div>
        
        <div id="chat" class="section" style="display:none;">
            <div class="card">
                <h3>💬 Chat con RAULI</h3>
                <div style="height: 300px; background: #1a202c; border-radius: 8px; padding: 10px; margin-bottom: 10px;">
                    <div style="margin-bottom: 10px;">
                        <strong>RAULI:</strong> ¡Hola! Soy tu asistente IA enterprise. ¿En qué puedo ayudarte?
                    </div>
                </div>
                <input type="text" placeholder="Escribe tu mensaje..." style="width: 100%; padding: 10px; border-radius: 8px; border: none; margin-bottom: 10px;">
                <button class="btn">📤 Enviar</button>
            </div>
        </div>
        
        <div id="vision" class="section" style="display:none;">
            <div class="card">
                <h3>👁️ Sistema de Visión</h3>
                <div style="height: 200px; background: #1a202c; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                    📷 Cámara en tiempo real
                </div>
                <button class="btn">📷 Capturar</button>
                <button class="btn">🔍 Analizar</button>
            </div>
        </div>
        
        <div id="control" class="section" style="display:none;">
            <div class="card">
                <h3>🎮 Panel de Control</h3>
                <button class="btn">🔄 Reiniciar Sistema</button>
                <button class="btn">📊 Generar Reporte</button>
                <button class="btn">🔧 Configuración</button>
                <button class="btn">📱 Modo Móvil</button>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(sectionId) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Remove active class from all nav items
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Show selected section
            document.getElementById(sectionId).style.display = 'block';
            
            // Add active class to clicked nav item
            event.target.classList.add('active');
        }
        
        // Auto-update status
        setInterval(() => {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    console.log('Status updated:', data);
                });
        }, 10000);
    </script>
</body>
</html>
"""
    
    # Template iframe
    dashboard_iframe_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖥️ RAULI Dashboard Completo</title>
    <style>
        body { margin: 0; padding: 0; }
        .iframe-container { width: 100vw; height: 100vh; border: none; }
        .mobile-header { background: #2d3748; color: white; padding: 10px; text-align: center; }
        .mobile-header a { color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <div class="mobile-header">
        <h3>🖥️ RAULI Dashboard</h3>
        <a href="/mobile">← Volver a versión móvil</a>
    </div>
    <iframe src="http://localhost:8502" class="iframe-container"></iframe>
</body>
</html>
"""
    
    # Guardar templates
    templates_dir = os.path.join(os.path.dirname(__file__), 'mobile_templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    with open(os.path.join(templates_dir, 'mobile_home.html'), 'w', encoding='utf-8') as f:
        f.write(mobile_home_html)
    
    with open(os.path.join(templates_dir, 'mobile_dashboard.html'), 'w', encoding='utf-8') as f:
        f.write(mobile_dashboard_html)
    
    with open(os.path.join(templates_dir, 'dashboard_iframe.html'), 'w', encoding='utf-8') as f:
        f.write(dashboard_iframe_html)
    
    print(f"📱 Templates móviles creados en: {templates_dir}")
    return templates_dir

if __name__ == "__main__":
    # Crear templates
    create_mobile_templates()
    
    # Iniciar servidor web móvil
    print("📱 Iniciando RAULI Mobile Web Interface...")
    print("🌐 Acceso móvil: http://localhost:5000")
    print("📱 Dashboard móvil: http://localhost:5000/mobile")
    print("🖥️ Dashboard completo: http://localhost:5000/api/dashboard/iframe")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
