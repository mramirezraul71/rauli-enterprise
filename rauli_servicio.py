#!/usr/bin/env python3
"""
🔄 SERVICIO RAULI-PERMANENTE
Mantiene el sistema activo permanentemente
"""

import sys
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent))
from rauli_permanente import RauliPermanente

class RauliServicio:
    def __init__(self):
        self.rauli = RauliPermanente()
        self.activo = True
        self.bots = {}
        
    def iniciar_bots(self):
        """Inicia todos los bots de RAULI"""
        # Bot de Telegram Audio
        try:
            subprocess.Popen([
                sys.executable,
                str(Path(__file__).parent / "telegram_rauli_audio_bot.py")
            ])
            print("🎤 Bot de Telegram Audio iniciado")
        except Exception as e:
            print(f"❌ Error iniciando bot audio: {e}")
        
        # Bot de Telegram Pro
        try:
            subprocess.Popen([
                sys.executable,
                str(Path(__file__).parent / "telegram_rauli_bot_pro.py")
            ])
            print("🚀 Bot de Telegram Pro iniciado")
        except Exception as e:
            print(f"❌ Error iniciando bot pro: {e}")
    
    def mantencion_automatica(self):
        """Mantención automática del sistema"""
        while self.activo:
            try:
                # Limpiar conversaciones antiguas
                self.rauli.limpiar_conversaciones_antiguas()
                
                # Verificar bots activos
                self.verificar_bots()
                
                # Esperar 1 hora
                time.sleep(3600)
                
            except Exception as e:
                print(f"❌ Error en mantención: {e}")
                time.sleep(300)  # 5 minutos si hay error
    
    def verificar_bots(self):
        """Verifica que los bots estén activos"""
        # Lógica para verificar y reiniciar bots si es necesario
        pass
    
    def run(self):
        """Ejecuta el servicio permanente"""
        print("🔄 Iniciando servicio RAULI-PERMANENTE...")
        
        # Iniciar bots
        self.iniciar_bots()
        
        # Iniciar mantención en background
        mantencion_thread = threading.Thread(target=self.mantencion_automatica, daemon=True)
        mantencion_thread.start()
        
        print("✅ Servicio RAULI-PERMANENTE activo")
        
        # Mantener servicio corriendo
        try:
            while self.activo:
                time.sleep(60)
        except KeyboardInterrupt:
            print("🛑 Deteniendo servicio...")
            self.activo = False

if __name__ == "__main__":
    servicio = RauliServicio()
    servicio.run()
