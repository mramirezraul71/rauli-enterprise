#!/usr/bin/env python3
"""
👁️ OJOS.RAULI - Módulo de visión para RAULI-BOT
Captura y análisis visual del entorno
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import time
from datetime import datetime

def capturar_pantalla():
    """
    Captura la pantalla actual
    """
    try:
        import pyautogui
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captura_{timestamp}.png"
        filepath = os.path.join(tempfile.gettempdir(), filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        print(f"📸 Captura guardada: {filepath}")
        return filepath
        
    except ImportError:
        # Fallback a PowerShell si no hay pyautogui
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captura_{timestamp}.png"
            filepath = os.path.join(tempfile.gettempdir(), filename)
            
            ps_script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            
            $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap $bounds.width, $bounds.height
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.size)
            $bitmap.Save("{filepath}", [System.Drawing.Imaging.ImageFormat]::Png)
            $graphics.Dispose()
            $bitmap.Dispose()
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"📸 Captura guardada: {filepath}")
                return filepath
            else:
                print(f"❌ Error capturando pantalla: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error en captura de pantalla: {e}")
            return None

def analizar_entorno():
    """
    Analiza el entorno visual actual
    """
    print("👁️ RAULI-BOT analizando entorno visual...")
    
    filepath = capturar_pantalla()
    if filepath:
        print(f"✅ Análisis visual completado")
        print(f"📍 Archivo: {filepath}")
        return filepath
    else:
        print("❌ Error en análisis visual")
        return None

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--captura":
        capturar_pantalla()
    else:
        analizar_entorno()

if __name__ == "__main__":
    main()
