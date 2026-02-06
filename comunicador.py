#!/usr/bin/env python3
"""
📢 COMUNICADOR.RAULI - Módulo de comunicación central para RAULI-BOT
Sistema de notificaciones y logging
"""

import os
import sys
import time
from datetime import datetime
import json

class ComunicadorRAULI:
    def __init__(self):
        self.log_file = os.path.join(os.path.dirname(__file__), "rauli_log.json")
        self.cargar_historial()
    
    def cargar_historial(self):
        """Carga historial de comunicaciones"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.historial = json.load(f)
            else:
                self.historial = []
        except:
            self.historial = []
    
    def guardar_historial(self):
        """Guarda historial de comunicaciones"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.historial[-100:], f, indent=2, ensure_ascii=False)  # Últimos 100 mensajes
        except Exception as e:
            print(f"❌ Error guardando historial: {e}")
    
    def informar(self, mensaje, nivel="INFO"):
        """
        Envía mensaje de información
        """
        timestamp = datetime.now().isoformat()
        
        entrada = {
            "timestamp": timestamp,
            "nivel": nivel,
            "mensaje": mensaje,
            "modulo": "COMUNICADOR"
        }
        
        self.historial.append(entrada)
        self.guardar_historial()
        
        # Formato de salida
        iconos = {
            "INFO": "📢",
            "EXITO": "✅",
            "ADVERTENCIA": "⚠️",
            "ERROR": "❌",
            "CRITICO": "🚨"
        }
        
        icono = iconos.get(nivel, "📢")
        print(f"{icono} RAULI-BOT [{timestamp[:19]}]: {mensaje}")
        
        # Si es crítico, también usa voz
        if nivel == "CRITICO":
            self.hablar_critical(mensaje)
        
        return entrada
    
    def hablar_critical(self, mensaje):
        """Usa boca.py para mensajes críticos"""
        try:
            subprocess.run([
                sys.executable, 
                os.path.join(os.path.dirname(__file__), "boca.py"),
                f"Mensaje crítico: {mensaje}"
            ], capture_output=True, timeout=30)
        except:
            pass  # Silencioso para evitar loops
    
    def mostrar_estado(self):
        """Muestra estado actual del sistema"""
        self.informar("SISTEMA RAULI-BOT ACTIVO", "EXITO")
        
        # Verificar módulos
        modulos = {
            "boca.py": "Síntesis de voz",
            "ojos.py": "Visión por computadora", 
            "manos.py": "Control de mouse",
            "comunicador.py": "Comunicación central"
        }
        
        for modulo, descripcion in modulos.items():
            ruta = os.path.join(os.path.dirname(__file__), modulo)
            if os.path.exists(ruta):
                self.informar(f"✅ {modulo} - {descripcion}: ACTIVO", "EXITO")
            else:
                self.informar(f"❌ {modulo} - {descripcion}: INACTIVO", "ERROR")
    
    def obtener_ultimos_mensajes(self, cantidad=10):
        """Obtiene los últimos mensajes del historial"""
        return self.historial[-cantidad:]

def main():
    if len(sys.argv) < 2:
        print("Uso: python comunicador.py \"mensaje\" [nivel]")
        print("Niveles: INFO, EXITO, ADVERTENCIA, ERROR, CRITICO")
        sys.exit(1)
    
    # Determinar si el último argumento es un nivel
    posible_nivel = sys.argv[-1] if len(sys.argv) > 1 else ""
    if len(sys.argv) > 2 and posible_nivel in ["INFO", "EXITO", "ADVERTENCIA", "ERROR", "CRITICO"]:
        mensaje = " ".join(sys.argv[1:-1])
        nivel = posible_nivel
    else:
        mensaje = " ".join(sys.argv[1:])
        nivel = "INFO"
    
    comunicador = ComunicadorRAULI()
    
    if mensaje == "--estado":
        comunicador.mostrar_estado()
    elif mensaje == "--historial":
        mensajes = comunicador.obtener_ultimos_mensajes()
        for msg in mensajes:
            print(f"[{msg['timestamp'][:19]}] {msg['nivel']}: {msg['mensaje']}")
    else:
        comunicador.informar(mensaje, nivel)

if __name__ == "__main__":
    main()
