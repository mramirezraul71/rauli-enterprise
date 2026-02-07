#!/usr/bin/env python3
"""
🤲 MANOS.RAULI - Módulo de control de mouse para RAULI-BOT
Automatización y control del cursor
"""

import os
import sys
import subprocess
import time
import math

def mover_mouse(x, y, duracion=0.5):
    """
    Mueve el mouse a coordenadas específicas
    """
    try:
        import pyautogui
        
        # Movimiento suave
        pyautogui.moveTo(x, y, duration=duracion)
        print(f"🤲 Mouse movido a ({x}, {y})")
        return True
        
    except ImportError:
        # Fallback a PowerShell si no hay pyautogui
        try:
            ps_script = f'''
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Mouse {{
                [DllImport("user32.dll")]
                public static extern bool SetCursorPos(int x, int y);
            }}
            "@
            [Mouse]::SetCursorPos({x}, {y})
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"🤲 Mouse movido a ({x}, {y})")
                return True
            else:
                print(f"❌ Error moviendo mouse: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error en control de mouse: {e}")
            return False

def click_derecho():
    """
    Realiza click derecho
    """
    try:
        import pyautogui
        pyautogui.rightClick()
        print("🤲 Click derecho realizado")
        return True
    except:
        return False

def click_izquierdo():
    """
    Realiza click izquierdo
    """
    try:
        import pyautogui
        pyautogui.click()
        print("🤲 Click izquierdo realizado")
        return True
    except:
        return False

def scroll(direccion="abajo", cantidad=3):
    """
    Hace scroll en la dirección especificada
    """
    try:
        import pyautogui
        
        if direccion == "abajo":
            pyautogui.scroll(-cantidad)
        else:
            pyautogui.scroll(cantidad)
            
        print(f"🤲 Scroll {direccion} realizado")
        return True
    except:
        return False

def main():
    if len(sys.argv) < 3:
        print("Uso: python manos.py <comando> [parámetros]")
        print("Comandos:")
        print("  mover <x> <y> - Mueve mouse a coordenadas")
        print("  click_izquierdo - Click izquierdo")
        print("  click_derecho - Click derecho")
        print("  scroll <arriba/abajo> [cantidad]")
        sys.exit(1)
    
    comando = sys.argv[1]
    
    if comando == "mover" and len(sys.argv) >= 4:
        x, y = int(sys.argv[2]), int(sys.argv[3])
        mover_mouse(x, y)
    elif comando == "click_izquierdo":
        click_izquierdo()
    elif comando == "click_derecho":
        click_derecho()
    elif comando == "scroll" and len(sys.argv) >= 3:
        direccion = sys.argv[2]
        cantidad = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        scroll(direccion, cantidad)
    else:
        print("❌ Comando no reconocido")
        sys.exit(1)

if __name__ == "__main__":
    main()
