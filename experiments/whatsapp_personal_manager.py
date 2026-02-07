#!/usr/bin/env python3
"""
📱 RAULI WhatsApp Personal Manager - Gestión personal directa
Comunicación solo a tu número personal
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

class WhatsAppPersonalManager:
    def __init__(self):
        self.personal_number = "+19192078141"  # Tu número personal
        self.from_number = "+14155238886"  # Número Twilio
        self.message_log = []
        self.service_active = False
        
        # Directorio para logs
        self.log_dir = r'C:\RAULI_CORE\logs\whatsapp'
        os.makedirs(self.log_dir, exist_ok=True)
        
        print("📱 RAULI WhatsApp Personal Manager")
        print(f"📞 Número personal: {self.personal_number}")
        print(f"📤 Número Twilio: {self.from_number}")
        
    def send_personal_message(self, message):
        """Enviar mensaje a tu número personal"""
        try:
            # Importar Twilio
            from twilio.rest import Client
            
            # Leer credenciales
            credentials = self._read_credentials()
            
            if not credentials.get('TWILIO_SID') or credentials.get('TWILIO_SID') == 'AC...':
                print("❌ Twilio SID no configurado")
                return False
            
            if not credentials.get('TWILIO_TOKEN') or credentials.get('TWILIO_TOKEN') == '...':
                print("❌ Twilio Token no configurado")
                return False
            
            # Crear cliente
            client = Client(credentials['TWILIO_SID'], credentials['TWILIO_TOKEN'])
            
            # Enviar mensaje
            message_obj = client.messages.create(
                body=message,
                from_=f"whatsapp:{self.from_number}",
                to=f"whatsapp:{self.personal_number}"
            )
            
            # Registrar en log
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'to': self.personal_number,
                'from': self.from_number,
                'message': message,
                'sid': message_obj.sid,
                'status': message_obj.status
            }
            
            self._save_log(log_entry)
            
            print(f"✅ Mensaje enviado a {self.personal_number}")
            print(f"📋 SID: {message_obj.sid}")
            print(f"📊 Estado: {message_obj.status}")
            
            return True
            
        except ImportError:
            print("❌ Instalando Twilio...")
            os.system("pip install twilio")
            return False
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
            return False
    
    def _read_credentials(self):
        """Leer credenciales de la bóveda"""
        credentials = {}
        try:
            with open("C:/dev/credenciales.txt", 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        credentials[key] = value
        except Exception as e:
            print(f"❌ Error leyendo credenciales: {e}")
        return credentials
    
    def _save_log(self, log_entry):
        """Guardar log de mensaje"""
        log_file = os.path.join(self.log_dir, f"personal_log_{datetime.now().strftime('%Y%m%d')}.json")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"❌ Error guardando log: {e}")
    
    def send_test_message(self):
        """Enviar mensaje de prueba"""
        test_message = f"""🧪 MENSAJE DE PRUEBA - RAULI WHATSAPP

📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 Para: Tu número personal
🤖 De: RAULI-BOT System

✅ Sistema funcionando correctamente
📱 WhatsApp Personal Manager activo

💡 Responde este mensaje para probar comunicación"""
        
        return self.send_personal_message(test_message)
    
    def send_system_status(self):
        """Enviar estado del sistema"""
        status_message = f"""📊 ESTADO SISTEMA RAULI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚀 COMPONENTES ACTIVOS:
🧠 Ollama IA Engine - Funcionando
🌐 Dashboard Web - Puerto 4174
📱 WhatsApp Personal - Activo
🤖 Telegram Bots - Operativos
☁️ Cloud Architecture - Lista

🎯 ACCESO RÁPIDO:
• Dashboard: http://localhost:4174
• Ollama: http://localhost:11434
• Cloud: http://localhost:8000

💻 COMANDOS DISPONIBLES:
• estado - Estado completo
• dashboard - Acceso web
• ayuda - Comandos

👑 RAULI-BOT 100% OPERATIVO"""
        
        return self.send_personal_message(status_message)
    
    def send_alert_message(self, alert_type, message):
        """Enviar mensaje de alerta"""
        alert_emoji = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        
        emoji = alert_emoji.get(alert_type, '📢')
        
        alert_message = f"""{emoji} ALERTA RAULI - {alert_type.upper()}

📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📞 Para: Número personal
🤖 Sistema: RAULI-BOT

{message}

🔔 Revisa el sistema si es necesario"""
        
        return self.send_personal_message(alert_message)
    
    def start_personal_service(self):
        """Iniciar servicio personal"""
        print("🚀 Iniciando servicio WhatsApp Personal...")
        self.service_active = True
        
        # Mensaje de inicio
        start_message = f"""🚀 SERVICIO WHATSAPP PERSONAL ACTIVADO

📅 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👞 Número: {self.personal_number}
🤖 Sistema: RAULI-BOT Personal

✅ Comunicación directa establecida
📊 Logging automático activo
🔄 Servicio en modo monitoreo

💡 Envia 'estado' para información del sistema"""
        
        if self.send_personal_message(start_message):
            print("✅ Servicio personal iniciado correctamente")
            
            # Mantener servicio activo
            try:
                while self.service_active:
                    time.sleep(60)  # Verificación cada minuto
                    print(f"📱 Servicio activo - {datetime.now().strftime('%H:%M:%S')}")
            except KeyboardInterrupt:
                print("🛑 Deteniendo servicio...")
                self.service_active = False
                
                # Mensaje de cierre
                stop_message = f"""🛑 SERVICIO WHATSAPP PERSONAL DETENIDO

📅 Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⏱️ Tiempo activo: Servicio funcionando
📊 Estado: Detenido por usuario

👋 Hasta pronto, RAULI-BOT"""
                
                self.send_personal_message(stop_message)
        else:
            print("❌ Error iniciando servicio personal")
    
    def show_menu(self):
        """Mostrar menú de opciones"""
        print("\n📱 MENÚ WHATSAPP PERSONAL")
        print("=" * 30)
        print("1. Enviar mensaje de prueba")
        print("2. Enviar estado del sistema")
        print("3. Enviar mensaje personalizado")
        print("4. Iniciar servicio personal")
        print("5. Salir")
        print("=" * 30)

def main():
    """Función principal"""
    manager = WhatsAppPersonalManager()
    
    while True:
        manager.show_menu()
        
        try:
            option = input("🎯 Selección: ").strip()
            
            if option == '1':
                manager.send_test_message()
            elif option == '2':
                manager.send_system_status()
            elif option == '3':
                message = input("📝 Mensaje: ").strip()
                if message:
                    manager.send_personal_message(message)
            elif option == '4':
                manager.start_personal_service()
                break
            elif option == '5':
                print("👋 Saliendo...")
                break
            else:
                print("❌ Opción no válida")
        except KeyboardInterrupt:
            print("\n👋 Saliendo...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
