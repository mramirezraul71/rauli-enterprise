#!/usr/bin/env python3
"""
🎨 RAULI Icon Creator - Creación de icono profesional para el sistema
"""

import os
from PIL import Image, ImageDraw, ImageFont
import io

def create_rauli_icon():
    """Crear icono RAULI profesional"""
    print("🎨 Creando icono RAULI profesional...")
    
    try:
        # Crear imagen base 256x256
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colores profesionales
        bg_color = (20, 30, 48)  # Azul oscuro profesional
        primary_color = (0, 123, 255)  # Azul brillante
        accent_color = (255, 193, 7)  # Amarillo dorado
        text_color = (255, 255, 255)  # Blanco
        
        # Fondo circular
        margin = 20
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=bg_color, outline=primary_color, width=4)
        
        # Dibujar "R" estilizado
        font_size = 120
        try:
            # Intentar usar fuente profesional
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fuente por defecto
            font = ImageFont.load_default()
        
        # Calcular posición centrada para "R"
        text = "R"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - 20
        
        # Sombra del texto
        draw.text((x+3, y+3), text, font=font, fill=(0, 0, 0, 128))
        # Texto principal
        draw.text((x, y), text, font=font, fill=primary_color)
        
        # Línea decorativa inferior
        line_y = y + text_height + 20
        draw.line([x+20, line_y, x+text_width-20, line_y], 
                 fill=accent_color, width=3)
        
        # Guardar como PNG
        icon_path = os.path.join(os.getcwd(), "rauli_icon.png")
        img.save(icon_path, "PNG")
        
        # Crear versión ICO (múltiples tamaños)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        ico_path = os.path.join(os.getcwd(), "rauli_icon.ico")
        
        # Redimensionar para cada tamaño
        icon_images = []
        for size in icon_sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            icon_images.append(resized)
        
        # Guardar como ICO
        icon_images[0].save(ico_path, format='ICO', sizes=[size for size in icon_sizes])
        
        print(f"✅ Icono PNG creado: {icon_path}")
        print(f"✅ Icono ICO creado: {ico_path}")
        
        return ico_path
        
    except ImportError:
        print("❌ PIL/Pillow no instalado. Creando icono simple...")
        return create_simple_icon()
    except Exception as e:
        print(f"❌ Error creando icono: {e}")
        return create_simple_icon()

def create_simple_icon():
    """Crear icono simple sin PIL"""
    print("🎨 Creando icono simple...")
    
    # Crear un archivo ICO simple usando recursos del sistema
    ico_path = os.path.join(os.getcwd(), "rauli_icon.ico")
    
    try:
        # Usar icono del sistema como base
        import win32api
        import win32con
        import win32gui
        
        # Extraer icono del sistema
        shell32 = win32api.GetModuleHandle("shell32.dll")
        if shell32:
            # Usar un icono genérico de computadora
            hicon = win32gui.ExtractIcon(shell32, 4, 0)
            if hicon:
                # Guardar como ICO
                win32gui.SaveIcon(hicon, ico_path)
                win32gui.DestroyIcon(hicon)
                print(f"✅ Icono simple creado: {ico_path}")
                return ico_path
    except:
        pass
    
    # Si todo falla, crear un archivo vacío
    with open(ico_path, 'wb') as f:
        f.write(b'')
    
    print(f"⚠️ Icono vacío creado: {ico_path}")
    return ico_path

def update_shortcut_with_icon():
    """Actualizar acceso directo con icono"""
    print("🔗 Actualizando acceso directo con icono...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        # Obtener escritorio OneDrive
        desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
        shortcut_path = os.path.join(desktop, "RAULI Manager.bat")
        
        # Crear nuevo acceso directo con icono
        lnk_path = os.path.join(desktop, "🚀 RAULI System Manager.lnk")
        
        # Rutas
        target_path = os.path.join(os.getcwd(), "RAULI_Manager.bat")
        working_dir = os.getcwd()
        icon_path = os.path.join(os.getcwd(), "rauli_icon.ico")
        
        # Verificar archivos
        if not os.path.exists(target_path):
            print(f"❌ Target no encontrado: {target_path}")
            return False
        
        if not os.path.exists(icon_path):
            print(f"❌ Icono no encontrado: {icon_path}")
            return False
        
        # Eliminar acceso directo anterior
        if os.path.exists(lnk_path):
            os.remove(lnk_path)
        
        # Crear acceso directo con icono
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(lnk_path)
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = working_dir
        shortcut.IconLocation = f"{icon_path},0"
        shortcut.Description = "RAULI System Manager - Gestor Profesional de Servicios IA"
        shortcut.save()
        
        print(f"✅ Acceso directo con icono creado: {lnk_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando acceso directo con icono: {e}")
        return False

def clean_desktop():
    """Limpiar accesos directos antiguos del escritorio"""
    print("🧹 Limpiando accesos directos antiguos...")
    
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    
    # Archivos a eliminar
    files_to_remove = [
        "RAULI System.lnk",
        "RAULI System.bat", 
        "RAULI System DEBUG.bat",
        "RAULI System DEFINITIVO.bat",
        "RAULI System PYTHON.bat",
        "RAULI System VBS.vbs"
    ]
    
    removed_count = 0
    for file in files_to_remove:
        file_path = os.path.join(desktop, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Eliminado: {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error eliminando {file}: {e}")
    
    print(f"✅ {removed_count} accesos directos antiguos eliminados")
    return removed_count

def create_enhanced_launcher():
    """Crear lanzador mejorado con logo en ASCII"""
    print("🚀 Creando lanzador mejorado...")
    
    launcher_content = '''@echo off
REM 🚀 RAULI System Manager - Versión Profesional con Logo
title RAULI System Manager
color 0A

REM Logo RAULI
echo.
echo     ████████╗ ██████╗ ███████╗██╗  ██╗███████╗██████╗ ██████╗ 
echo     ╚══██╔══╝██╔═══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔═══██╗
echo        ██║   ██║   ██║███████╗███████║█████╗  ██████╔╝██║   ██║
echo        ██║   ██║   ██║╚════██║██╔══██║██╔══╝  ██╔══██╗██║   ██║
echo        ██║   ╚██████╔╝███████║██║  ██║███████╗██║  ██║╚██████╔╝
echo        ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ 
echo.
echo     ███████╗ ██████╗ ██╗   ██╗███████╗████████╗ ██████╗ ███╗   ███╗
echo     ██╔════╝██╔═══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗████╗ ████║
echo     ███████╗██║   ██║██║   ██║█████╗     ██║   ██║   ██║██╔████╔██║
echo     ╚════██║██║   ██║╚██╗ ██╔╝██╔══╝     ██║   ██║   ██║██║╚██╔╝██║
echo     ███████║╚██████╔╝ ╚████╔╝ ███████╗   ██║   ╚██████╔╝██║ ╚═╝ ██║
echo     ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
echo.
echo ========================================
echo 🚀 RAULI SYSTEM MANAGER v1.0
echo ========================================
echo.
echo 💻 Iniciando interfaz gráfica profesional...
echo 📊 Gestión completa de servicios RAULI
echo 🎛️ Control centralizado del sistema IA
echo.

cd /d C:\\RAULI_CORE

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo 💡 Por favor instala Python 3.11+
    pause
    exit /b 1
)

REM Iniciar gestor gráfico
echo 🚀 Iniciando RAULI Service Manager...
python rauli_service_manager.py

REM Si hay error, mostrar diagnóstico
if errorlevel 1 (
    echo.
    echo ❌ Error iniciando el gestor gráfico
    echo 🐛 Ejecutando diagnóstico...
    echo.
    echo 📋 Información del sistema:
    python --version
    echo.
    echo 📁 Archivos en RAULI_CORE:
    dir /b *.py
    echo.
    echo 🔍 Verificando dependencias...
    python -c "import tkinter; print('✅ tkinter disponible')" 2>nul || echo "❌ tkinter no disponible"
    python -c "import psutil; print('✅ psutil disponible')" 2>nul || echo "❌ psutil no disponible"
    echo.
    echo 💡 Si faltan dependencias, ejecuta:
    echo    pip install psutil
    echo.
    pause
)
'''
    
    with open("RAULI_Manager.bat", 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Lanzador mejorado creado")

def main():
    """Función principal"""
    print("🎨 RAULI System - Logo y Limpieza Profesional")
    print("=" * 60)
    
    # 1. Crear icono
    icon_path = create_rauli_icon()
    
    # 2. Crear lanzador mejorado
    create_enhanced_launcher()
    
    # 3. Limpiar escritorio
    removed_count = clean_desktop()
    
    # 4. Actualizar acceso directo con icono
    shortcut_ok = update_shortcut_with_icon()
    
    # 5. Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE ACTUALIZACIÓN PROFESIONAL")
    print("=" * 60)
    print(f"🎨 Icono creado: {'✅' if icon_path else '❌'}")
    print(f"🚀 Lanzador mejorado: ✅")
    print(f"🧹 Accesos antiguos eliminados: {removed_count}")
    print(f"🔗 Acceso directo con icono: {'✅' if shortcut_ok else '❌'}")
    
    print("\n🎯 CARACTERÍSTICAS PROFESIONALES:")
    print("✅ Icono personalizado RAULI")
    print("✅ Logo ASCII en el launcher")
    print("✅ Escritorio limpio y organizado")
    print("✅ Acceso directo único y profesional")
    
    print("\n💡 USO PROFESIONAL:")
    print("🎯 Busca '🚀 RAULI System Manager.lnk' en tu escritorio")
    print("🎨 Doble click para iniciar el sistema profesional")
    print("🧹 Escritorio limpio sin accesos redundantes")

if __name__ == "__main__":
    main()
