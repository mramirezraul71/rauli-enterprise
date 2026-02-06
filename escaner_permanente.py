#!/usr/bin/env python3
"""
🔍 ESCÁNER PERMANENTE RAULI - Monitoreo continuo de bots y respuestas instantáneas
Sistema de escaneo constante para respuestas inmediatas
"""

import os
import sys
import time
import json
import threading
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Cargar credenciales RAULI
load_dotenv(r"C:\RAULI_CORE\credenciales.env")

class EscanerPermanente:
    def __init__(self):
        self.core_dir = Path(r"C:\RAULI_CORE")
        self.log_file = self.core_dir / "escaner_permanente.log"
        self.estado_file = self.core_dir / "escaner_estado.json"
        
        # Configuración
        self.intervalo_escaneo = 1  # 1 segundo
        self.intervalo_verificacion = 5  # 5 segundos
        self.timeout_respuesta = 30  # 30 segundos
        
        # Estado
        self.activo = True
        self.bots_activos = {}
        self.ultimo_escaneo = time.time()
        self.mensajes_pendientes = {}
        self.respuestas_enviadas = 0
        
        # Configurar logging
        self.setup_logging()
        
        logger.info("🔍 ESCÁNER PERMANENTE inicializado")
    
    def setup_logging(self):
        """Configura logging especializado"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        global logger
        logger = logging.getLogger('EscanerPermanente')
    
    def cargar_estado(self):
        """Carga estado del escáner"""
        try:
            if self.estado_file.exists():
                with open(self.estado_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    'inicio': datetime.now().isoformat(),
                    'escaneos_totales': 0,
                    'bots_detectados': 0,
                    'respuestas_procesadas': 0
                }
        except Exception as e:
            logger.error(f"❌ Error cargando estado: {e}")
            return {}
    
    def guardar_estado(self, estado):
        """Guarda estado del escáner"""
        try:
            estado['ultima_actualizacion'] = datetime.now().isoformat()
            with open(self.estado_file, 'w', encoding='utf-8') as f:
                json.dump(estado, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ Error guardando estado: {e}")
    
    def escanear_bots_activos(self):
        """Escanea bots activos en el sistema"""
        bots_detectados = {}
        
        # Buscar procesos Python activos
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:  # Omitir encabezado
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            pid = parts[1].strip('"')
                            bots_detectados[f'python_{pid}'] = {
                                'pid': pid,
                                'tipo': 'python_process',
                                'detectado': datetime.now().isoformat()
                            }
        except Exception as e:
            logger.error(f"❌ Error escaneando procesos: {e}")
        
        # Verificar bots específicos por puerto o archivo
        bots_especificos = {
            'telegram_audio': {
                'script': 'telegram_rauli_audio_bot.py',
                'puerto': None,
                'verificacion': self.verificar_bot_audio
            },
            'telegram_pro': {
                'script': 'telegram_rauli_bot_pro.py', 
                'puerto': None,
                'verificacion': self.verificar_bot_pro
            }
        }
        
        for nombre, config in bots_especificos.items():
            if config['verificacion']():
                bots_detectados[nombre] = {
                    'tipo': 'telegram_bot',
                    'script': config['script'],
                    'estado': 'activo',
                    'detectado': datetime.now().isoformat()
                }
        
        return bots_detectados
    
    def verificar_bot_audio(self):
        """Verifica si el bot de audio está activo"""
        try:
            # Verificar si el proceso está corriendo
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'telegram_rauli_audio_bot.py' in result.stdout:
                return True
            return False
        except:
            return False
    
    def verificar_bot_pro(self):
        """Verifica si el bot pro está activo"""
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'telegram_rauli_bot_pro.py' in result.stdout:
                return True
            return False
        except:
            return False
    
    def reiniciar_bot(self, tipo_bot):
        """Reinicia un bot específico"""
        try:
            if tipo_bot == 'audio':
                script_path = self.core_dir / 'telegram_rauli_audio_bot.py'
            elif tipo_bot == 'pro':
                script_path = self.core_dir / 'telegram_rauli_bot_pro.py'
            else:
                return False
            
            # Iniciar bot en background
            subprocess.Popen([
                sys.executable,
                str(script_path)
            ])
            
            logger.info(f"🔄 Bot {tipo_bot} reiniciado")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error reiniciando bot {tipo_bot}: {e}")
            return False
    
    def escanear_mensajes_telegram(self):
        """Escanea mensajes pendientes en Telegram"""
        try:
            # Aquí se implementaría la lógica para verificar mensajes pendientes
            # Por ahora, simulamos detección
            mensajes_pendientes = []
            
            # Verificar si hay actividad reciente en los logs
            log_file = self.core_dir / 'rauli_permanente.log'
            if log_file.exists():
                # Leer últimas líneas del log
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-10:]  # Últimas 10 líneas
                
                for line in lines:
                    if 'mensaje' in line.lower() or 'telegram' in line.lower():
                        mensajes_pendientes.append({
                            'timestamp': datetime.now().isoformat(),
                            'contenido': line.strip(),
                            'estado': 'pendiente'
                        })
            
            return mensajes_pendientes
            
        except Exception as e:
            logger.error(f"❌ Error escaneando mensajes: {e}")
            return []
    
    def procesar_respuesta_inmediata(self, mensaje):
        """Procesa respuesta inmediata a mensaje"""
        try:
            # Extraer información del mensaje
            contenido = mensaje.get('contenido', '')
            
            # Generar respuesta rápida
            respuesta = self.generar_respuesta_rapida(contenido)
            
            # Enviar respuesta (simulado)
            logger.info(f"⚡ Respuesta inmediata: {respuesta}")
            self.respuestas_enviadas += 1
            
            return respuesta
            
        except Exception as e:
            logger.error(f"❌ Error procesando respuesta: {e}")
            return None
    
    def generar_respuesta_rapida(self, contenido):
        """Genera respuesta ultra-rápida"""
        contenido_lower = contenido.lower()
        
        # Respuestas predefinidas para máxima velocidad
        if 'hola' in contenido_lower:
            return "¡Hola! Estoy aquí para ayudarte inmediatamente."
        elif 'cómo estás' in contenido_lower:
            return "Estoy perfecto y escuchándote siempre."
        elif 'ayuda' in contenido_lower:
            return "Puedo ayudarte con programación, código y sistemas técnicos."
        elif 'gracias' in contenido_lower:
            return "De nada siempre es un placer ayudarte."
        else:
            return "Entiendo tu mensaje. Estoy procesando tu solicitud."
    
    def bucle_escaneo_principal(self):
        """Bucle principal de escaneo"""
        estado = self.cargar_estado()
        
        while self.activo:
            try:
                inicio_ciclo = time.time()
                
                # 1. Escanear bots activos
                bots_actuales = self.escanear_bots_activos()
                self.bots_activos = bots_actuales
                
                # 2. Verificar bots críticos
                bots_criticos = ['telegram_audio', 'telegram_pro']
                for bot in bots_criticos:
                    if bot not in bots_actuales:
                        logger.warning(f"⚠️ Bot {bot} no detectado, reiniciando...")
                        self.reiniciar_bot(bot.replace('telegram_', ''))
                
                # 3. Escanear mensajes pendientes
                mensajes = self.escanear_mensajes_telegram()
                for mensaje in mensajes:
                    self.procesar_respuesta_inmediata(mensaje)
                
                # 4. Actualizar estadísticas
                estado['escaneos_totales'] += 1
                estado['bots_detectados'] = len(bots_actuales)
                estado['respuestas_procesadas'] = self.respuestas_enviadas
                estado['ultimo_escaneo'] = datetime.now().isoformat()
                
                # 5. Guardar estado periódicamente
                if estado['escaneos_totales'] % 60 == 0:  # Cada 60 escaneos
                    self.guardar_estado(estado)
                
                # 6. Esperar para próximo ciclo
                tiempo_ciclo = time.time() - inicio_ciclo
                espera = max(0, self.intervalo_escaneo - tiempo_ciclo)
                time.sleep(espera)
                
            except Exception as e:
                logger.error(f"❌ Error en bucle de escaneo: {e}")
                time.sleep(5)  # Esperar 5 segundos si hay error
    
    def bucle_verificacion(self):
        """Bucle de verificación profunda"""
        while self.activo:
            try:
                # Verificación completa cada 5 segundos
                time.sleep(self.intervalo_verificacion)
                
                # Verificar estado de los bots
                bots_actuales = self.escanear_bots_activos()
                
                # Log de estado
                logger.info(f"🔍 Escaneo: {len(bots_actuales)} bots activos, {self.respuestas_enviadas} respuestas")
                
                # Verificación de salud
                if len(bots_actuales) < 2:
                    logger.warning("⚠️ Menos de 2 bots activos")
                
            except Exception as e:
                logger.error(f"❌ Error en verificación: {e}")
    
    def iniciar_escaneo_permanente(self):
        """Inicia el escaneo permanente"""
        logger.info("🚀 Iniciando escaneo permanente...")
        
        # Iniciar bucle principal
        escaneo_thread = threading.Thread(target=self.bucle_escaneo_principal, daemon=True)
        escaneo_thread.start()
        
        # Iniciar bucle de verificación
        verificacion_thread = threading.Thread(target=self.bucle_verificacion, daemon=True)
        verificacion_thread.start()
        
        logger.info("✅ Escaneo permanente activo")
        
        # Mantener corriendo
        try:
            while self.activo:
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("🛑 Deteniendo escaneo permanente...")
            self.activo = False
    
    def obtener_estado_actual(self):
        """Obtiene estado actual del escáner"""
        return {
            'activo': self.activo,
            'bots_activos': len(self.bots_activos),
            'respuestas_enviadas': self.respuestas_enviadas,
            'ultimo_escaneo': datetime.fromtimestamp(self.ultimo_escaneo).isoformat(),
            'uptime': time.time() - self.ultimo_escaneo
        }
    
    def detener(self):
        """Detiene el escaneo permanente"""
        logger.info("🛑 Deteniendo escáner permanente...")
        self.activo = False

# Instancia global
escaner_global = None

def iniciar_escaner_permanente():
    """Inicia el escáner permanente global"""
    global escaner_global
    if escaner_global is None:
        escaner_global = EscanerPermanente()
    
    escaner_thread = threading.Thread(target=escaner_global.iniciar_escaneo_permanente, daemon=True)
    escaner_thread.start()
    
    return escaner_global

def obtener_escaner():
    """Obtiene instancia del escáner"""
    return escaner_global

def main():
    """Función principal"""
    print("🔍 ESCÁNER PERMANENTE RAULI")
    print("=" * 50)
    
    # Iniciar escáner
    escaner = iniciar_escaner_permanente()
    
    print("✅ Escáner permanente iniciado")
    print("🔍 Monitoreando bots y mensajes continuamente...")
    
    try:
        # Mantener corriendo
        while True:
            time.sleep(10)
            estado = escaner.obtener_estado_actual()
            print(f"📊 Estado: {estado['bots_activos']} bots, {estado['respuestas_enviadas']} respuestas")
            
    except KeyboardInterrupt:
        print("🛑 Deteniendo escáner...")
        escaner.detener()

if __name__ == "__main__":
    main()
