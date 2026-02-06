#!/usr/bin/env python3
"""
📱 RAULI WhatsApp Link Manager - Gestión 100% gratuita
"""

import os
import webbrowser
import urllib.parse
from datetime import datetime

class WhatsAppLinkManager:
    def __init__(self):
        self.personal_number = "+19192078141"
        self.log_dir = r'C:\RAULI_CORE\logs\whatsapp_links'
        os.makedirs(self.log_dir, exist_ok=True)
        
    def create_link(self, message):
        """Crear link WhatsApp con mensaje"""
        # Codificar mensaje
        encoded_message = urllib.parse.quote(message)
        
        # Crear link
        number_clean = self.personal_number.replace('+', '')
        link = f"https://wa.me/{number_clean}?text={encoded_message}"
        
        return link
    
    def send_message_via_link(self, message):
        """Enviar mensaje via link WhatsApp"""
        link = self.create_link(message)
        
        # Registrar log
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'link': link,
            'method': 'whatsapp_link'
        }
        
        log_file = os.path.join(self.log_dir, f'links_{datetime.now().strftime("%Y%m%d")}.json')
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(str(log_entry) + '\n')
        
        # Abrir navegador
        print(f"📱 Abriendo WhatsApp: {link}")
        webbrowser.open(link)
        
        return link
    
    def send_system_status(self):
        """Enviar estado del sistema"""
        status_message = f"""🚀 RAULI-BOT STATUS REPORT
📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ COMPONENTES ACTIVOS:
🧠 Ollama IA Engine
🌐 Dashboard Web (puerto 4174)
📱 WhatsApp Link Manager
🤖 Telegram Bots
☁️ Cloud Architecture

🎯 ACCESO:
• Dashboard: http://localhost:4174
• Ollama: http://localhost:11434
• Cloud: http://localhost:8000

💡 Método: WhatsApp Link (100% gratis)
👑 RAULI-BOT System"""
        
        return self.send_message_via_link(status_message)
    
    def send_alert(self, alert_type, message):
        """Enviar alerta"""
        alert_emoji = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        
        emoji = alert_emoji.get(alert_type, '📢')
        
        alert_message = f"""{emoji} RAULI ALERT - {alert_type.upper()}
📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{message}

🔗 Método: WhatsApp Link (100% gratis)"""
        
        return self.send_message_via_link(alert_message)

# Uso
if __name__ == "__main__":
    manager = WhatsAppLinkManager()
    manager.send_system_status()
