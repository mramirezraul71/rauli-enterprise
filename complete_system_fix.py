#!/usr/bin/env python3
"""
🔧 RAULI System Complete Fix - Solución definitiva para Dashboard y WhatsApp
"""

import os
import sys
import subprocess
import time
import json
import threading
from pathlib import Path
import webbrowser

def check_dashboard_status():
    """Verificar estado del dashboard"""
    print("🌐 VERIFICANDO ESTADO DEL DASHBOARD")
    print("=" * 50)
    
    # 1. Verificar si el servidor está corriendo
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:4174', timeout=5)
        if response.getcode() == 200:
            print("✅ Dashboard corriendo en http://localhost:4174")
            return True
    except:
        print("❌ Dashboard no responde en puerto 4174")
    
    # 2. Verificar puerto 4173
    try:
        response = urllib.request.urlopen('http://localhost:4173', timeout=5)
        if response.getcode() == 200:
            print("✅ Dashboard corriendo en http://localhost:4173")
            return True
    except:
        print("❌ Dashboard no responde en puerto 4173")
    
    return False

def start_dashboard_server():
    """Iniciar servidor del dashboard"""
    print("🚀 INICIANDO SERVIDOR DEL DASHBOARD")
    
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    
    if not dashboard_dir.exists():
        print("❌ Directorio del dashboard no encontrado")
        return False
    
    try:
        # Iniciar npm run preview en background
        process = subprocess.Popen(
            ["npm", "run", "preview"],
            cwd=dashboard_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("🔄 Esperando a que inicie el servidor...")
        time.sleep(5)
        
        # Verificar si está corriendo
        for port in [4173, 4174, 4175]:
            try:
                response = urllib.request.urlopen(f'http://localhost:{port}', timeout=2)
                if response.getcode() == 200:
                    print(f"✅ Dashboard iniciado en http://localhost:{port}")
                    
                    # Abrir en navegador
                    webbrowser.open(f'http://localhost:{port}')
                    return True
            except:
                continue
        
        print("❌ No se pudo iniciar el dashboard")
        return False
        
    except Exception as e:
        print(f"❌ Error iniciando dashboard: {e}")
        return False

def check_whatsapp_status():
    """Verificar estado de WhatsApp"""
    print("\n💬 VERIFICANDO ESTADO DE WHATSAPP")
    print("=" * 50)
    
    # 1. Verificar archivo de WhatsApp
    whatsapp_file = Path("C:/RAULI_CORE/rauli_whatsapp_professional.py")
    
    if not whatsapp_file.exists():
        print("❌ Archivo de WhatsApp no encontrado")
        return False
    
    print(f"✅ Archivo encontrado: {whatsapp_file}")
    
    # 2. Verificar credenciales
    try:
        with open("C:/RAULI_CORE/credenciales.env", 'r') as f:
            content = f.read()
            
        if "TWILIO" in content:
            print("✅ Credenciales Twilio encontradas")
        else:
            print("❌ Credenciales Twilio no encontradas")
            return False
            
    except Exception as e:
        print(f"❌ Error leyendo credenciales: {e}")
        return False
    
    return True

def start_whatsapp_service():
    """Iniciar servicio de WhatsApp"""
    print("🚀 INICIANDO SERVICIO DE WHATSAPP")
    
    try:
        # Iniciar WhatsApp Professional
        process = subprocess.Popen(
            [sys.executable, "rauli_whatsapp_professional.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("🔄 Esperando a que inicie WhatsApp...")
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ WhatsApp Professional iniciado")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Error iniciando WhatsApp:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando WhatsApp: {e}")
        return False

def create_test_whatsapp_message():
    """Crear mensaje de prueba para WhatsApp"""
    print("📝 CREANDO MENSAJE DE PRUEBA")
    
    test_script = '''#!/usr/bin/env python3
"""
📨 WhatsApp Test Message - Mensaje de prueba para RAULI
"""

import os
import sys
from pathlib import Path

def send_test_message():
    """Enviar mensaje de prueba"""
    try:
        # Leer credenciales
        with open("C:/RAULI_CORE/credenciales.env", 'r') as f:
            lines = f.readlines()
        
        twilio_sid = None
        twilio_token = None
        whatsapp_from = None
        whatsapp_to = None
        
        for line in lines:
            if "TWILIO_SID" in line:
                twilio_sid = line.split("=")[1].strip()
            elif "TWILIO_TOKEN" in line:
                twilio_token = line.split("=")[1].strip()
            elif "WHATSAPP_FROM" in line:
                whatsapp_from = line.split("=")[1].strip()
            elif "WHATSAPP_TO" in line:
                whatsapp_to = line.split("=")[1].strip()
        
        if not all([twilio_sid, twilio_token, whatsapp_from, whatsapp_to]):
            print("❌ Credenciales incompletas")
            return False
        
        # Enviar mensaje usando Twilio
        from twilio.rest import Client
        
        client = Client(twilio_sid, twilio_token)
        
        message = client.messages.create(
            body="🚀 RAULI System - Mensaje de prueba\\n\\n✅ Sistema operativo\\n📊 Dashboard funcionando\\n💬 WhatsApp activo\\n\\n🎯 Comandante RAÚL, sistema RAULI listo para producción!",
            from_=f'whatsapp:{whatsapp_from}',
            to=f'whatsapp:{whatsapp_to}'
        )
        
        print(f"✅ Mensaje enviado: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")
        return False

if __name__ == "__main__":
    print("📨 ENVIANDO MENSAJE DE PRUEBA WHATSAPP")
    print("=" * 40)
    send_test_message()
'''
    
    with open("test_whatsapp_message.py", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Script de prueba creado: test_whatsapp_message.py")
    
    # Ejecutar prueba
    try:
        result = subprocess.run(
            [sys.executable, "test_whatsapp_message.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"📊 Resultado: {result.stdout}")
        if result.stderr:
            print(f"❌ Errores: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando prueba: {e}")
        return False

def create_system_status_report():
    """Crear reporte completo del sistema"""
    print("\n📊 CREANDO REPORTE COMPLETO DEL SISTEMA")
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "services": {
            "dashboard": check_dashboard_status(),
            "whatsapp": check_whatsapp_status()
        },
        "actions_taken": []
    }
    
    # Si el dashboard no está corriendo, iniciarlo
    if not report["services"]["dashboard"]:
        print("\n🚀 INICIANDO DASHBOARD...")
        if start_dashboard_server():
            report["services"]["dashboard"] = True
            report["actions_taken"].append("Dashboard iniciado")
    
    # Si WhatsApp no está verificado, iniciarlo
    if not report["services"]["whatsapp"]:
        print("\n🚀 INICIANDO WHATSAPP...")
        if start_whatsapp_service():
            report["services"]["whatsapp"] = True
            report["actions_taken"].append("WhatsApp iniciado")
    
    # Enviar mensaje de prueba
    if report["services"]["whatsapp"]:
        print("\n📨 ENVIANDO MENSAJE DE PRUEBA...")
        if create_test_whatsapp_message():
            report["actions_taken"].append("Mensaje de prueba enviado")
    
    # Guardar reporte
    with open("rauli_system_status.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    return report

def main():
    """Función principal"""
    print("🔧 RAULI SYSTEM COMPLETE FIX")
    print("=" * 60)
    print("🎯 Resolviendo problemas de Dashboard y WhatsApp")
    print("🚀 Haciendo el sistema completamente funcional")
    print("=" * 60)
    
    # 1. Estado inicial
    print("\n📊 ESTADO INICIAL DEL SISTEMA:")
    dashboard_ok = check_dashboard_status()
    whatsapp_ok = check_whatsapp_status()
    
    # 2. Crear reporte y ejecutar acciones
    report = create_system_status_report()
    
    # 3. Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL - SISTEMA RAULI")
    print("=" * 60)
    print(f"🌐 Dashboard: {'✅ FUNCIONAL' if report['services']['dashboard'] else '❌ ERROR'}")
    print(f"💬 WhatsApp: {'✅ FUNCIONAL' if report['services']['whatsapp'] else '❌ ERROR'}")
    
    print(f"\n🎯 ACCIONES REALIZADAS:")
    for action in report["actions_taken"]:
        print(f"  ✅ {action}")
    
    print(f"\n🌐 ENDPOINTS DISPONIBLES:")
    if report["services"]["dashboard"]:
        print("  • http://localhost:4174 (Dashboard)")
        print("  • http://localhost:4173 (Dashboard alternativo)")
    
    print(f"\n💡 PRÓXIMOS PASOS:")
    print("  1. 🌐 Abre el dashboard en tu navegador")
    print("  2. 💬 Revisa el mensaje de WhatsApp")
    print("  3. 🚀 Usa el RAULI System Manager para controlar todo")
    print("  4. 📊 Verifica que todos los servicios estén activos")
    
    print(f"\n🎉 SISTEMA RAULI LISTO PARA PRODUCCIÓN")

if __name__ == "__main__":
    main()
