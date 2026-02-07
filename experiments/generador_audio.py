#!/usr/bin/env python3
"""
🎤 GENERADOR DE AUDIO RAULI - Sistema robusto para generar archivos de audio
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import time

class GeneradorAudio:
    def __init__(self):
        self.temp_dir = Path(r"C:\RAULI_CORE\temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def generar_audio_wav(self, texto):
        """
        Genera archivo WAV usando PowerShell y System.Speech
        """
        timestamp = int(time.time())
        output_path = self.temp_dir / f"audio_{timestamp}.wav"
        
        try:
            # Escapar texto para PowerShell
            texto_escaped = texto.replace('"', '""').replace("'", "''")
            
            # Script PowerShell para generar audio
            ps_script = f'''
            Add-Type -AssemblyName System.Speech
            $synthesizer = New-Object System.Speech.Synthesis.SpeechSynthesizer
            
            # Configurar voz en español si está disponible
            $voices = $synthesizer.GetVoices()
            foreach ($voice in $voices) {{
                if ($voice.Description -like "*Spanish*" -or $voice.Description -like "*Sabina*") {{
                    $synthesizer.Voice = $voice
                    break
                }}
            }}
            
            # Configurar formato de salida
            $synthesizer.SetOutputToWaveFile("{output_path}")
            $synthesizer.Speak("{texto_escaped}")
            $synthesizer.Dispose()
            
            Write-Output "Audio generado: {output_path}"
            '''
            
            # Ejecutar script PowerShell
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.temp_dir)
            )
            
            if result.returncode == 0 and output_path.exists():
                # Verificar que el archivo no esté vacío
                if output_path.stat().st_size > 1024:  # Al menos 1KB
                    print(f"✅ Audio generado: {output_path}")
                    return str(output_path)
                else:
                    print(f"❌ Archivo de audio demasiado pequeño: {output_path.stat().st_size} bytes")
                    if output_path.exists():
                        output_path.unlink()
                    return None
            else:
                print(f"❌ Error PowerShell: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error generando audio: {e}")
            return None
    
    def generar_audio_mp3(self, texto):
        """
        Genera archivo MP3 usando OpenAI TTS si está disponible
        """
        try:
            import openai
            from dotenv import load_dotenv
            
            load_dotenv(r"C:\RAULI_CORE\credenciales.env")
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                return None
            
            client = openai.OpenAI()
            
            timestamp = int(time.time())
            output_path = self.temp_dir / f"audio_{timestamp}.mp3"
            
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",  # Voz neutra que funciona bien
                input=texto
            )
            
            response.stream_to_file(str(output_path))
            
            if output_path.exists() and output_path.stat().st_size > 1024:
                print(f"✅ Audio MP3 generado: {output_path}")
                return str(output_path)
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error generando MP3: {e}")
            return None
    
    def generar_audio_fallback(self, texto):
        """
        Fallback: genera un archivo de audio básico
        """
        timestamp = int(time.time())
        output_path = self.temp_dir / f"audio_{timestamp}.wav"
        
        try:
            # Usar método alternativo con SAPI directamente
            import win32com.client
            
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            
            # Guardar a archivo
            file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
            file_stream.Format.Type = 1  # WAV format
            file_stream.Open(str(output_path), 3, 0)  # SSFMCreateForWrite
            
            speaker.AudioStream = file_stream
            speaker.Speak(texto)
            file_stream.Close()
            
            if output_path.exists() and output_path.stat().st_size > 1024:
                print(f"✅ Audio SAPI generado: {output_path}")
                return str(output_path)
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error fallback: {e}")
            return None
    
    def generar_audio(self, texto, preferencia="wav"):
        """
        Genera audio usando el mejor método disponible
        """
        print(f"🎤 Generando audio: '{texto[:50]}...'")
        
        # Intentar con método preferido
        if preferencia == "mp3":
            audio_path = self.generar_audio_mp3(texto)
            if audio_path:
                return audio_path
        
        # Intentar con WAV (PowerShell)
        audio_path = self.generar_audio_wav(texto)
        if audio_path:
            return audio_path
        
        # Fallback con SAPI directo
        audio_path = self.generar_audio_fallback(texto)
        if audio_path:
            return audio_path
        
        print("❌ No se pudo generar audio")
        return None
    
    def limpiar_temporales(self):
        """
        Limpia archivos temporales antiguos
        """
        try:
            ahora = time.time()
            for archivo in self.temp_dir.glob("audio_*.wav"):
                if ahora - archivo.stat().st_mtime > 300:  # 5 minutos
                    archivo.unlink()
                    print(f"🗑️ Eliminado: {archivo}")
            
            for archivo in self.temp_dir.glob("audio_*.mp3"):
                if ahora - archivo.stat().st_mtime > 300:
                    archivo.unlink()
                    print(f"🗑️ Eliminado: {archivo}")
                    
        except Exception as e:
            print(f"❌ Error limpiando temporales: {e}")

# Instancia global
generador = GeneradorAudio()

def generar_audio_para_texto(texto):
    """
    Función global para generar audio
    """
    return generador.generar_audio(texto)

def main():
    """
    Prueba del generador de audio
    """
    print("🎤 Probando generador de audio...")
    
    pruebas = [
        "Hola, soy Rauli",
        "Esto es una prueba de generación de audio",
        "El sistema está funcionando correctamente"
    ]
    
    for prueba in pruebas:
        audio_path = generar_audio_para_texto(prueba)
        if audio_path:
            print(f"✅ Generado: {audio_path}")
            # Verificar tamaño
            size = Path(audio_path).stat().st_size
            print(f"📊 Tamaño: {size} bytes")
        else:
            print(f"❌ Falló: {prueba}")
    
    # Limpiar
    generador.limpiar_temporales()

if __name__ == "__main__":
    main()
