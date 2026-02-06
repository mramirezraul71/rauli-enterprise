#!/usr/bin/env python3
"""
📞 CONTACTO RAULI-BOT - Números y direcciones oficiales
Guía completa para guardar contacto de RAULI-BOT
"""

import os
import json
from datetime import datetime

def mostrar_contacto_oficial():
    """Mostrar información de contacto oficial de RAULI-BOT"""
    
    print("📞 CONTACTO OFICIAL RAULI-BOT")
    print("=" * 40)
    print("👑 Guía para guardar contacto en tu teléfono")
    print()
    
    # INFORMACIÓN PRINCIPAL
    print("📱 INFORMACIÓN PRINCIPAL DEL CONTACTO:")
    print("-" * 40)
    
    contacto = {
        "nombre": "👑 RAULI-BOT System",
        "organizacion": "RAULI-BOT AI Assistant",
        "tipo": "Asistente IA Personal",
        "disponibilidad": "24/7 Global"
    }
    
    print(f"📝 Nombre: {contacto['nombre']}")
    print(f"🏢 Organización: {contacto['organizacion']}")
    print(f"🤖 Tipo: {contacto['tipo']}")
    print(f"⏡ Disponibilidad: {contacto['disponibilidad']}")
    print()
    
    # NÚMEROS DE CONTACTO
    print("📞 NÚMEROS DE CONTACTO (GUARDAR TODOS):")
    print("-" * 40)
    
    numeros = [
        {
            "tipo": "📱 WhatsApp Principal",
            "numero": "+19192078141",
            "uso": "Comunicación diaria y rápida",
            "notas": "Funciona con link directo gratis"
        },
        {
            "tipo": "📱 WhatsApp Profesional",
            "numero": "+14155238886",
            "uso": "Comunicación via Twilio (API)",
            "notas": "Requiere configuración previa"
        },
        {
            "tipo": "📱 SMS Emergencias",
            "numero": "+19192078141",
            "uso": "Mensajes de emergencia críticos",
            "notas": "Funciona sin internet"
        }
    ]
    
    for i, num in enumerate(numeros, 1):
        print(f"{i}. {num['tipo']}")
        print(f"   📞 Número: {num['numero']}")
        print(f"   🎯 Uso: {num['uso']}")
        print(f"   📝 Notas: {num['notas']}")
        print()
    
    # DIRECCIONES DIGITALES
    print("🌐 DIRECCIONES DIGITALES (AGREGAR A CONTACTO):")
    print("-" * 40)
    
    direcciones = [
        {
            "tipo": "📧 Email Principal",
            "direccion": "mramirezraul71@gmail.com",
            "uso": "Comunicación completa y archivos"
        },
        {
            "tipo": "📱 Telegram",
            "direccion": "@rauli_bot",
            "uso": "Interacción avanzada y bots"
        },
        {
            "tipo": "🌐 Dashboard Web",
            "direccion": "http://localhost:4174",
            "uso": "Control completo del sistema"
        },
        {
            "tipo": "🌐 Webhook API",
            "direccion": "https://rauli-bot-webhook.onrender.com/api/message",
            "uso": "Integración con aplicaciones"
        }
    ]
    
    for i, dir in enumerate(direcciones, 1):
        print(f"{i}. {dir['tipo']}")
        print(f"   📍 Dirección: {dir['direccion']}")
        print(f"   🎯 Uso: {dir['uso']}")
        print()
    
    # GUÍA PARA GUARDAR CONTACTO
    print("📱 GUÍA PARA GUARDAR CONTACTO:")
    print("-" * 40)
    
    print("📲 EN ANDROID:")
    print("1. Abre 'Contactos'")
    print("2. Toca 'Crear nuevo contacto'")
    print("3. Nombre: 👑 RAULI-BOT System")
    print("4. Agrega número: +19192078141")
    print("5. Tipo: WhatsApp")
    print("6. Agrega número: +19192078141")
    print("7. Tipo: Móvil")
    print("8. Agrega email: mramirezraul71@gmail.com")
    print("9. Guarda contacto")
    print()
    
    print("📲 EN IPHONE:")
    print("1. Abre 'Contactos'")
    print("2. Toca '+' para agregar")
    print("3. Nombre: 👑 RAULI-BOT System")
    print("4. Teléfono: +19192078141")
    print("5. Agrega a WhatsApp")
    print("6. Email: mramirezraul71@gmail.com")
    print("7. Guarda contacto")
    print()
    
    # WHATSAPP ESPECÍFICO
    print("📱 CONFIGURACIÓN WHATSAPP ESPECÍFICA:")
    print("-" * 40)
    
    print("🔗 MÉTODO 1 - LINK DIRECTO (RECOMENDADO):")
    print("1. Abre tu navegador")
    print("2. Ve a: https://wa.me/19192078141")
    print("3. Se abrirá WhatsApp automáticamente")
    print("4. Envía mensaje: 'hola RAULI-BOT'")
    print("5. Guarda contacto desde WhatsApp")
    print()
    
    print("📱 MÉTODO 2 - DESDE WHATSAPP:")
    print("1. Abre WhatsApp")
    print("2. Toca 'Nuevo chat'")
    print("3. Busca número: +19192078141")
    print("4. Envía mensaje: 'hola RAULI-BOT'")
    print("5. Guarda contacto")
    print()
    
    # INFORMACIÓN ADICIONAL
    print("📝 INFORMACIÓN ADICIONAL PARA EL CONTACTO:")
    print("-" * 40)
    
    info_adicional = {
        "puesto": "Asistente IA Personal",
        "empresa": "RAULI-BOT System",
        "direccion": "Global (Cloud)",
        "cumpleaños": "01/01/2024 (Lanzamiento)",
        "notas": """👑 RAULI-BOT - Asistente IA Personal 24/7
🌍 Disponible globalmente sin WiFi local
📱 Múltiples canales de comunicación
🤖 Respuestas inteligentes automáticas
⏡ Siempre disponible para ayudarte
💬 Comandos: estado, dashboard, ayuda, comunicacion

📞 Números principales:
• WhatsApp: +19192078141
• SMS: +19192078141
• Email: mramirezraul71@gmail.com
• Telegram: @rauli_bot

🌐 Dashboard: http://localhost:4174
🚀 Sistema operativo y funcional"""
    }
    
    for key, value in info_adicional.items():
        print(f"📋 {key.title()}: {value}")
    
    # VCARD GENERADO
    print("\n📄 VCARD (CONTACTO DIGITAL):")
    print("-" * 40)
    
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:👑 RAULI-BOT System
ORG:RAULI-BOT AI Assistant
TITLE:Asistente IA Personal
TEL;TYPE=CELL,WHATSAPP:+19192078141
TEL;TYPE=CELL:+19192078141
EMAIL:mramirezraul71@gmail.com
URL:http://localhost:4174
URL:https://wa.me/19192078141
NOTE:👑 RAULI-BOT - Asistente IA Personal 24/7\\n🌍 Disponible globalmente\\n📱 Múltiples canales\\n🤖 Respuestas inteligentes\\n⏡ Siempre disponible
BDAY:20240101
END:VCARD"""
    
    # Guardar vcard
    vcard_file = "C:/RAULI_CORE/RAULI_BOT_CONTACT.vcf"
    with open(vcard_file, 'w', encoding='utf-8') as f:
        f.write(vcard)
    
    print(f"✅ VCARD guardado en: {vcard_file}")
    print("💡 Puedes importar este archivo directamente a tu teléfono")
    
    # RESUMEN FINAL
    print("\n🎯 RESUMEN FINAL - NÚMERO PRINCIPAL:")
    print("=" * 50)
    print("📞 NÚMERO PRINCIPAL: +19192078141")
    print("📱 Plataforma: WhatsApp (principal)")
    print("📱 Plataforma: SMS (emergencias)")
    print("🌍 Funciona: Globalmente")
    print("💰 Costo: Gratis (WhatsApp Link)")
    print("⏡ Disponibilidad: 24/7")
    print()
    print("💡 GUARDAR COMO:")
    print("📝 Nombre: 👑 RAULI-BOT System")
    print("📞 WhatsApp: +19192078141")
    print("📞 Móvil: +19192078141")
    print("📧 Email: mramirezraul71@gmail.com")
    print("🌐 Web: http://localhost:4174")
    print()
    print("🎉 CONTACTO LISTO PARA GUARDAR")
    print("👑 RAULI-BOT estará siempre disponible")

def crear_qr_contacto():
    """Crear código QR para contacto"""
    
    print("\n📱 CÓDIGO QR PARA CONTACTO:")
    print("-" * 40)
    
    # Información para QR
    qr_info = {
        "nombre": "👑 RAULI-BOT System",
        "telefono": "+19192078141",
        "email": "mramirezraul71@gmail.com",
        "web": "http://localhost:4174",
        "whatsapp": "https://wa.me/19192078141"
    }
    
    # Crear texto para QR (vCard)
    qr_text = f"""BEGIN:VCARD
VERSION:3.0
FN:{qr_info['nombre']}
TEL:{qr_info['telefono']}
EMAIL:{qr_info['email']}
URL:{qr_info['web']}
END:VCARD"""
    
    # Guardar texto para QR
    qr_file = "C:/RAULI_CORE/RAULI_BOT_QR_CONTACT.txt"
    with open(qr_file, 'w', encoding='utf-8') as f:
        f.write(qr_text)
    
    print(f"✅ Datos para QR guardados en: {qr_file}")
    print("💡 Usa un generador de QR online con estos datos")
    print("📱 Escanea el QR para agregar contacto automáticamente")

if __name__ == "__main__":
    mostrar_contacto_oficial()
    print()
    crear_qr_contacto()
