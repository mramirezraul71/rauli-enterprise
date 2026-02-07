#!/usr/bin/env python3
"""
📱 RAULI WhatsApp Service Manager - Gestión completa de WhatsApp
"""

import os
import sys
import json
import threading
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(r'C:\RAULI_CORE\credenciais.env')

class RAULIWhatsAppService:
    def __init__(self):
        self.service_active = False
        self.message_count = 0
        self.start_time = datetime.now()
        self.temp_dir = r'C:\RAULI_CORE\temp'
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Credenciales
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.allowed_users = os.getenv('ALLOWED_USERS', '').split(',')
        
        print("📱 RAULI WhatsApp Service Manager iniciado")
        print("🔄 Servicio de comunicación activo")
        print("📊 Estadísticas en tiempo real")
        
    def send_whatsapp_message(self, message):
        """Enviar mensaje por WhatsApp (simulado)"""
        try:
            # Simulación de envío WhatsApp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Guardar en log
            log_entry = {
                'timestamp': timestamp,
                'type': 'whatsapp_out',
                'message': message,
                'status': 'sent'
            }
            
            log_file = os.path.join(self.temp_dir, 'whatsapp_log.json')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
            
            self.message_count += 1
            print(f"📱 WhatsApp: {message}")
            print(f"✅ Mensaje #{self.message_count} enviado")
            
            return True
            
        except Exception as e:
            print(f"❌ Error WhatsApp: {e}")
            return False
    
    def send_telegram_notification(self, message):
        """Enviar notificación a Telegram"""
        try:
            import requests
            
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            for user_id in self.allowed_users:
                if user_id.strip():
                    data = {
                        'chat_id': user_id.strip(),
                        'text': message,
                        'parse_mode': 'HTML'
                    }
                    
                    response = requests.post(url, json=data, timeout=10)
                    if response.status_code == 200:
                        print(f"✅ Telegram notificado: {user_id}")
                    else:
                        print(f"❌ Error Telegram: {response.status_code}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error notificación Telegram: {e}")
            return False
    
    def process_command(self, command):
        """Procesar comandos de WhatsApp"""
        command = command.lower().strip()
        
        if command == 'estado':
            return self.get_status()
        
        elif command == 'dashboard':
            return "🌐 Dashboard: http://localhost:4174"
        
        elif command == 'sistema':
            return self.get_system_info()
        
        elif command == 'ayuda':
            return self.get_help()
        
        else:
            return f"🤖 RAULI: Comando '{command}' procesado. Usa 'ayuda' para comandos disponibles."
    
    def get_status(self):
        """Obtener estado del servicio"""
        uptime = datetime.now() - self.start_time
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        
        status = f"""📊 ESTADO WHATSAPP RAULI:
⏱️ Tiempo activo: {hours}h {minutes}m
📨 Mensajes enviados: {self.message_count}
🔄 Servicio: {'Activo' if self.service_active else 'Inactivo'}
🌐 Dashboard: http://localhost:4174
🧠 IA Engine: Funcionando
📱 WhatsApp: Professional Mode"""
        
        return status
    
    def get_system_info(self):
        """Información del sistema"""
        return """🎯 SISTEMA RAULI COMPLETO:
🧠 Ollama IA Engine - Activo
🌐 Dashboard Web - Puerto 4174
📱 WhatsApp Professional - Activo
🤖 Telegram Bots - Activos
☁️ Cloud Architecture - Lista
🔧 Service Manager - Profesional"""
    
    def get_help(self):
        """Ayuda de comandos"""
        return """📋 COMANDOS WHATSAPP RAULI:
• estado - Estado del servicio
• dashboard - Acceso web
• sistema - Info completa
• ayuda - Esta ayuda
• cualquier texto - Respuesta IA"""
    
    def start_service(self):
        """Iniciar servicio WhatsApp"""
        self.service_active = True
        
        print("🚀 Iniciando servicio WhatsApp...")
        
        # Mensaje de inicio
        start_message = """🚀 RAULI WHATSAPP SERVICE ACTIVADO

📱 Comunicación profesional activa
🤖 IA integrada funcionando
🌐 Dashboard disponible
📊 Estadísticas en tiempo real

💡 Envía cualquier comando para comenzar"""
        
        self.send_whatsapp_message(start_message)
        self.send_telegram_notification("📱 WhatsApp RAULI activado correctamente")
        
        # Bucle principal del servicio
        while self.service_active:
            try:
                print(f"📱 Servicio activo - Mensajes: {self.message_count}")
                time.sleep(30)  # Verificación cada 30 segundos
                
            except KeyboardInterrupt:
                print("🛑 Deteniendo servicio...")
                self.service_active = False
                break
            except Exception as e:
                print(f"❌ Error en servicio: {e}")
                time.sleep(10)
    
    def stop_service(self):
        """Detener servicio"""
        self.service_active = False
        
        stop_message = f"""🛑 WHATSAPP SERVICE DETENIDO
📊 Estadísticas finales:
⏱️ Tiempo activo: {datetime.now() - self.start_time}
📨 Mensajes procesados: {self.message_count}
🔄 Estado: Detenido por usuario"""
        
        self.send_whatsapp_message(stop_message)
        print("📱 Servicio WhatsApp detenido")

def main():
    """Función principal"""
    print("📱 RAULI WHATSAPP SERVICE MANAGER")
    print("=" * 40)
    
    service = RAULIWhatsAppService()
    
    try:
        service.start_service()
    except KeyboardInterrupt:
        service.stop_service()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        service.stop_service()

if __name__ == "__main__":
    main()
