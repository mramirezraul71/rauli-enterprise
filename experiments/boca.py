#!/usr/bin/env python3
"""
🗣️ BOCA.RAULI - Módulo de síntesis de voz para RAULI-BOT
Comunicación verbal natural y permanente
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def hablar(texto, voz="Sabina"):
    """
    Convierte texto a voz usando sistema Windows
    """
    try:
        import win32com.client
        
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        
        # Configurar voz en español si está disponible
        voices = speaker.GetVoices()
        for voice in voices:
            if "Spanish" in voice.GetDescription() or "Sabina" in voice.GetDescription():
                speaker.Voice = voice
                break
        
        speaker.Speak(texto)
        return True
        
    except ImportError:
        # Fallback a PowerShell si no hay win32com
        try:
            ps_script = f'''
            Add-Type -AssemblyName System.Speech
            $synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $synthesizer.Speak("{texto}")
            '''
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error en síntesis de voz: {e}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python boca.py \"texto a hablar\"")
        sys.exit(1)
    
    texto = " ".join(sys.argv[1:])
    print(f"🗣️ RAULI-BOT dice: {texto}")
    
    if hablar(texto):
        print("✅ Voz generada exitosamente")
    else:
        print("❌ Error generando voz")
        sys.exit(1)

if __name__ == "__main__":
    main()
