#!/usr/bin/env python3
"""
🔧 RAULI Services Fix - Corrección completa de todos los servicios
"""

import os
import sys
import subprocess
from pathlib import Path
import json

def fix_dashboard_service():
    """Corregir servicio Dashboard"""
    print("🔧 Corrigiendo servicio Dashboard...")
    
    # Verificar Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Node.js encontrado:", result.stdout.strip())
        else:
            print("❌ Node.js no encontrado")
            return False
    except:
        print("❌ Node.js no instalado")
        return False
    
    # Verificar npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ npm encontrado:", result.stdout.strip())
        else:
            print("❌ npm no encontrado")
            return False
    except:
        print("❌ npm no instalado")
        return False
    
    # Verificar directorio del dashboard
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    if not dashboard_dir.exists():
        print("❌ Directorio del dashboard no encontrado")
        return False
    
    # Verificar package.json
    package_json = dashboard_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json no encontrado")
        return False
    
    print("✅ Dashboard service verificado")
    return True

def fix_whatsapp_service():
    """Corregir servicio WhatsApp"""
    print("🔧 Corrigiendo servicio WhatsApp...")
    
    script_path = Path("C:/RAULI_CORE/rauli_whatsapp_professional.py")
    if not script_path.exists():
        print("❌ Script de WhatsApp no encontrado")
        return False
    
    try:
        # Leer y limpiar encoding
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar emojis restantes
        emoji_fixes = {
            '🔔': '[BELL]',
            '📱': '[PHONE]',
            '🎤': '[MIC]',
            '📹': '[VIDEO]',
            '📁': '[FOLDER]',
            '🧠': '[AI]',
            '🌐': '[WEB]',
            '📊': '[METRICS]',
            '✅': '[OK]',
            '❌': '[ERROR]',
            '🔄': '[RESTART]',
            '⚡': '[SPEED]',
            '🎯': '[TARGET]',
            '🚀': '[BOOT]',
            '⚠️': '[WARNING]',
            '🔧': '[FIX]',
            '📦': '[PACKAGE]',
            '🔍': '[SEARCH]',
            '🛡️': '[SECURITY]',
            '📈': '[GRAPH]',
            '🔥': '[FIRE]',
            '💎': '[DIAMOND]',
            '🌟': '[STAR]',
            '🎉': '[PARTY]',
            '📋': '[LIST]',
            '🔗': '[LINK]',
            '🔐': '[LOCK]',
            '⏱️': '[TIME]',
            '🌍': '[WORLD]',
            '🤖': '[ROBOT]',
            '👁️': '[EYE]',
            '🖐️': '[HAND]',
            '🗣️': '[SPEAK]',
            '📢': '[SPEAKER]',
            '💡': '[IDEA]',
            '🏥': '[HOSPITAL]',
            '☁️': '[CLOUD2]',
            '📄': '[PAGE]',
            '🔄': '[RELOAD]',
            '📡': '[SIGNAL]',
            '🏆': '[TROPHY]',
            '🔒': '[LOCKED]',
            '🌎': '[EARTH]',
            '📝': '[WRITE]',
            '🎵': '[MUSIC]',
            '🎮': '[GAME]',
            '🎨': '[ART]',
            '🔬': '[SCIENCE]',
            '🏢': '[BUILDING]',
            '🌈': '[RAINBOW]',
            '⭐': '[STAR2]',
            '🎭': '[MASK]',
            '🎪': '[TENT]',
            '🎲': '[DICE]',
            '🎸': '[GUITAR]',
            '🎺': '[TRUMPET]',
            '🥁': '[DRUM]',
            '🎻': '[VIOLIN]',
            '🎹': '[PIANO]',
            '🎤': '[MIC2]',
            '🎧': '[HEADPHONES]',
            '📻': '[RADIO]',
            '📺': '[TV]',
            '📷': '[CAMERA]',
            '📹': '[VIDEO2]',
            '📼': '[TAPE]',
            '💿': '[CD]',
            '💾': '[DISK]',
            '💽': '[DISK2]',
            '🖥️': '[COMPUTER]',
            '⌨️': '[KEYBOARD]',
            '🖱️': '[MOUSE]',
            '🖨️': '[PRINTER]',
            '📠': '[FAX]',
            '☎️': '[PHONE]',
            '📲': '[PHONE3]',
            '⌚': '[WATCH]',
            '⏰': '[CLOCK]',
            '⏳': '[HOURGLASS]',
            '📅': '[CALENDAR]',
            '📆': '[CALENDAR2]',
            '🗓️': '[CALENDAR3]',
            '📍': '[PIN]',
            '🚩': '[FLAG]',
            '🏁': '[FINISH]',
            '🎌': '[FLAGS]',
            '🎏': '[FLAG2]',
            '🏳️': '[FLAG3]',
            '🏴': '[FLAG4]',
            '🏳️‍🌈': '[FLAG5]',
            '🏴‍☠️': '[FLAG6]',
            '🎪': '[TENT2]',
        }
        
        # Aplicar correcciones
        for emoji, replacement in emoji_fixes.items():
            content = content.replace(emoji, replacement)
        
        # Guardar corregido
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ WhatsApp service corregido")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo WhatsApp: {e}")
        return False

def create_rauli_logo():
    """Crear logo RAULI"""
    print("🎨 Creando logo RAULI...")
    
    # Logo ASCII
    logo_ascii = """
    ████████╗ ██████╗ ███████╗██╗  ██╗███████╗██████╗ ██████╗ 
    ╚══██╔══╝██╔═══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔═══██╗
       ██║   ██║   ██║███████╗███████║█████╗  ██████╔╝██║   ██║
       ██║   ██║   ██║╚════██║██╔══██║██╔══╝  ██╔══██╗██║   ██║
       ██║   ╚██████╔╝███████║██║  ██║███████╗██║  ██║╚██████╔╝
       ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
                                                               
    ███████╗ ██████╗ ██╗   ██╗███████╗████████╗ ██████╗ ███╗   ███╗
    ██╔════╝██╔═══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗████╗ ████║
    ███████╗██║   ██║██║   ██║█████╗     ██║   ██║   ██║██╔████╔██║
    ╚════██║██║   ██║╚██╗ ██╔╝██╔══╝     ██║   ██║   ██║██║╚██╔╝██║
    ███████║╚██████╔╝ ╚████╔╝ ███████╗   ██║   ╚██████╔╝██║ ╚═╝ ██║
    ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
    """
    
    # Guardar logo en archivo
    logo_path = Path("C:/RAULI_CORE/rauli_logo.txt")
    with open(logo_path, 'w', encoding='utf-8') as f:
        f.write(logo_ascii)
    
    print("✅ Logo RAULI creado en:", logo_path)
    return logo_path

def create_desktop_shortcut():
    """Crear acceso directo en el escritorio"""
    print("🔗 Creando acceso directo en escritorio...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        # Obtener escritorio
        desktop = winshell.desktop()
        path = os.path.join(desktop, "RAULI System.lnk")
        
        # Rutas
        target = os.path.join(os.getcwd(), "rauli_boot.bat")
        wDir = os.getcwd()
        icon = target
        
        # Crear acceso directo
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.Description = "RAULI System - Sistema IA Híbrido"
        shortcut.save()
        
        print("✅ Acceso directo creado en escritorio")
        return True
        
    except ImportError:
        print("⚠️ Instalando winshell...")
        subprocess.run([sys.executable, "-m", "pip", "install", "winshell", "pywin32"])
        
        # Reintentar
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "RAULI System.lnk")
            target = os.path.join(os.getcwd(), "rauli_boot.bat")
            wDir = os.getcwd()
            icon = target
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.Description = "RAULI System - Sistema IA Híbrido"
            shortcut.save()
            
            print("✅ Acceso directo creado (reintentado)")
            return True
            
        except Exception as e:
            print(f"❌ Error creando acceso directo: {e}")
            return False
    
    except Exception as e:
        print(f"❌ Error creando acceso directo: {e}")
        return False

def create_dashboard_shortcut():
    """Crear acceso directo en el dashboard"""
    print("🔗 Creando acceso directo en dashboard...")
    
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    
    # Crear acceso directo para arrancar dashboard
    shortcut_content = """@echo off
echo.
echo ========================================
echo 🚀 RAULI DASHBOARD
echo ========================================
echo.

cd /d C:\\dev\\RAULI-VISION\\dashboard
npm run preview

pause
"""
    
    shortcut_path = dashboard_dir / "start_dashboard.bat"
    with open(shortcut_path, 'w', encoding='utf-8') as f:
        f.write(shortcut_content)
    
    print("✅ Acceso directo del dashboard creado:", shortcut_path)
    return shortcut_path

def update_boot_config():
    """Actualizar configuración de arranque"""
    print("⚙️ Actualizando configuración de arranque...")
    
    config_path = Path("C:/RAULI_CORE/boot_config.json")
    
    # Configuración actualizada
    updated_config = {
        "auto_start": True,
        "boot_delay": 2,
        "health_check_interval": 10,
        "max_retries": 3,
        "open_browser": True,
        "log_level": "INFO",
        "services": {
            "ollama": {"enabled": True, "timeout": 30},
            "dashboard": {"enabled": True, "timeout": 15},
            "whatsapp": {"enabled": True, "timeout": 10},
            "hybrid_system": {"enabled": True, "timeout": 15},
            "cloud_architecture": {"enabled": True, "timeout": 20}
        },
        "shortcuts": {
            "desktop": True,
            "dashboard": True,
            "startup": False
        }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(updated_config, f, indent=2)
    
    print("✅ Configuración de arranque actualizada")
    return True

def main():
    """Función principal"""
    print("🔧 RAULI Services Fix - Corrección completa")
    print("=" * 60)
    
    # 1. Corregir servicios
    dashboard_ok = fix_dashboard_service()
    whatsapp_ok = fix_whatsapp_service()
    
    # 2. Crear logo
    logo_path = create_rauli_logo()
    
    # 3. Crear accesos directos
    desktop_shortcut = create_desktop_shortcut()
    dashboard_shortcut = create_dashboard_shortcut()
    
    # 4. Actualizar configuración
    config_ok = update_boot_config()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CORRECCIONES")
    print("=" * 60)
    print(f"🔧 Dashboard: {'✅' if dashboard_ok else '❌'}")
    print(f"💬 WhatsApp: {'✅' if whatsapp_ok else '❌'}")
    print(f"🎨 Logo: {'✅' if logo_path else '❌'}")
    print(f"🔗 Acceso directo escritorio: {'✅' if desktop_shortcut else '❌'}")
    print(f"🔗 Acceso directo dashboard: {'✅' if dashboard_shortcut else '❌'}")
    print(f"⚙️ Configuración: {'✅' if config_ok else '❌'}")
    
    print("\n🚀 Ahora intenta arrancar el sistema:")
    print("   python rauli_boot_manager.py boot")
    print("\n🎯 O usa el acceso directo del escritorio")

if __name__ == "__main__":
    main()
