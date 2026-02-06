
#!/usr/bin/env python3
"""
🌐 RAULI Web-Mobile Bridge
Puente de comunicación entre dashboard web y app móvil
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

class RAULIBridge:
    def __init__(self):
        self.mobile_connections = {}
        self.web_connections = {}
        self.messages = []
    
    def register_mobile(self, device_id):
        """Registrar dispositivo móvil"""
        self.mobile_connections[device_id] = {
            'connected_at': datetime.now(),
            'last_ping': datetime.now()
        }
        return {'status': 'connected', 'device_id': device_id}
    
    def register_web(self, session_id):
        """Registrar sesión web"""
        self.web_connections[session_id] = {
            'connected_at': datetime.now(),
            'last_ping': datetime.now()
        }
        return {'status': 'connected', 'session_id': session_id}
    
    def send_message(self, sender, receiver, message):
        """Enviar mensaje entre dispositivos"""
        msg = {
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.messages.append(msg)
        return msg

bridge = RAULIBridge()

@app.route('/api/mobile/register', methods=['POST'])
def register_mobile():
    data = request.json
    device_id = data.get('device_id')
    result = bridge.register_mobile(device_id)
    return jsonify(result)

@app.route('/api/web/register', methods=['POST'])
def register_web():
    data = request.json
    session_id = data.get('session_id')
    result = bridge.register_web(session_id)
    return jsonify(result)

@app.route('/api/message', methods=['POST'])
def send_message():
    data = request.json
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    result = bridge.send_message(sender, receiver, message)
    return jsonify(result)

@app.route('/api/messages/<device_id>', methods=['GET'])
def get_messages(device_id):
    messages = [msg for msg in bridge.messages if msg['receiver'] == device_id]
    return jsonify({'messages': messages})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        'mobile_devices': len(bridge.mobile_connections),
        'web_sessions': len(bridge.web_connections),
        'total_messages': len(bridge.messages)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
