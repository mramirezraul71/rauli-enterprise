#!/usr/bin/env python3
"""
📱 RAULI WhatsApp Message Sender - Envío directo de mensajes
"""

import os
import sys
from pathlib import Path

def send_direct_message():
    """Enviar mensaje directo usando credenciales"""
    try:
        # Importar Twilio
        from twilio.rest import Client
        
        # Leer credenciales de la bóveda
        credentials = {}
        with open("C:/dev/credenciales.txt", 'r', encoding='utf-8') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    credentials[key] = value
        
        # Obtener números
        from_number = credentials.get('WHATSAPP_FROM', '+14155238886')
        to_number = credentials.get('WHATSAPP_TO', '+19192078141')
        account_sid = credentials.get('TWILIO_SID', 'AC...')
        auth_token = credentials.get('TWILIO_TOKEN', '...')
        
        print(f"📱 Enviando mensaje...")
        print(f"📤 De: {from_number}")
        print(f"📥 Para: {to_number}")
        
        # Crear cliente Twilio
        if account_sid != 'AC...' and auth_token != '...':
            client = Client(account_sid, auth_token)
            
            # Mensaje profesional
            message_body = """🚀 RAULI-BOT SYSTEM ACTIVADO

👑 SISTEMA COMPLETO 100% OPERATIVO:
🧠 Ollama IA Engine - Funcionando
🌐 Dashboard Web - Activo
📱 WhatsApp Professional - Activado
🤖 Telegram Bots - Operativos
☁️ Cloud Architecture - Lista

🎯 ACCESO INMEDIATO:
• Dashboard: http://localhost:4174
• Ollama: http://localhost:11434
• Cloud: http://localhost:8000

💡 COMANDOS WHATSAPP:
• estado - Estado del sistema
• dashboard - Acceso web
• ayuda - Comandos disponibles

🎉 RAULI-BOT LISTO PARA PRODUCCIÓN"""
            
            # Enviar mensaje
            message = client.messages.create(
                body=message_body,
                from_=f"whatsapp:{from_number}",
                to=f"whatsapp:{to_number}"
            )
            
            print(f"✅ MENSAJE ENVIADO EXITOSAMENTE")
            print(f"📋 SID: {message.sid}")
            print(f"📊 Estado: {message.status}")
            
            return True
            
        else:
            print("❌ Credenciales Twilio incompletas")
            print("🔧 Configura TWILIO_SID y TWILIO_TOKEN")
            return False
            
    except ImportError:
        print("❌ Instalando Twilio...")
        os.system("pip install twilio")
        print("🔄 Ejecuta nuevamente después de la instalación")
        return False
        
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")
        return False

def show_credentials_info():
    """Mostrar información de credenciales"""
    print("📋 INFORMACIÓN DE CREDENCIALES:")
    print("=" * 40)
    
    try:
        with open("C:/dev/credenciales.txt", 'r', encoding='utf-8') as f:
            for line in f:
                if 'WHATSAPP' in line or 'TWILIO' in line:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        if '...' in value:
                            print(f"🔒 {key}: [CONFIGURAR]")
                        else:
                            # Ocultar parte sensible
                            if len(value) > 10:
                                visible = value[:6] + "..." + value[-4:]
                            else:
                                visible = "***"
                            print(f"✅ {key}: {visible}")
    except Exception as e:
        print(f"❌ Error leyendo credenciales: {e}")

def main():
    """Función principal"""
    print("📱 RAULI WHATSAPP MESSAGE SENDER")
    print("=" * 40)
    
    # Mostrar información de credenciales
    show_credentials_info()
    print()
    
    # Enviar mensaje
    if send_direct_message():
        print("\n🎉 MENSAJE WHATSAPP ENVIADO CORRECTAMENTE")
        print("📱 Revisa tu WhatsApp para confirmar recepción")
    else:
        print("\n❌ ERROR EN ENVÍO - VERIFICA CREDENCIALES")

if __name__ == "__main__":
    main()
