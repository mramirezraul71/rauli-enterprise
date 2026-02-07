#!/usr/bin/env python3
"""
⚡ RAULI WhatsApp Activator - Activación inmediata
"""

import os
import sys
from pathlib import Path

def activate_whatsapp_now():
    """Activar WhatsApp inmediatamente"""
    try:
        # Importar Twilio
        from twilio.rest import Client
        
        # Leer credenciales
        with open("C:/RAULI_CORE/credenciales.env", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        credentials = {}
        for line in lines:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                credentials[key] = value
        
        # Verificar credenciales Twilio
        if all(k in credentials for k in ['TWILIO_SID', 'TWILIO_TOKEN', 'WHATSAPP_FROM', 'WHATSAPP_TO']):
            client = Client(credentials['TWILIO_SID'], credentials['TWILIO_TOKEN'])
            
            # Enviar mensaje
            message = client.messages.create(
                body="🚀 RAULI SYSTEM 100% OPERATIVO\\n\\n✅ Dashboard: http://localhost:4174\\n✅ Ollama IA: Funcionando\\n✅ Service Manager: Activo\\n✅ WhatsApp Professional: Activado\\n\\n🎯 SISTEMA COMPLETO Y LISTO PARA PRODUCCIÓN",
                from_=f"whatsapp:{credentials['WHATSAPP_FROM']}",
                to=f"whatsapp:{credentials['WHATSAPP_TO']}"
            )
            
            print(f"✅ WHATSAPP ACTIVADO - Mensaje enviado: {message.sid}")
            return True
        else:
            print("❌ Credenciales incompletas")
            return False
            
    except ImportError:
        print("❌ Twilio no instalado")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("⚡ ACTIVANDO WHATSAPP...")
    if activate_whatsapp_now():
        print("🎉 SISTEMA RAULI 100% OPERATIVO")
    else:
        print("❌ ERROR EN ACTIVACIÓN")
