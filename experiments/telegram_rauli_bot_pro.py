#!/usr/bin/env python3
"""
🚀 TELEGRAM-RAULI-PRO - Sistema de respuesta inmediata y natural
Comunicación fluida sin comandos, respuesta instantánea
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import threading
from pathlib import Path
from datetime import datetime
import logging
from dotenv import load_dotenv
import asyncio
import queue

# Cargar credenciales RAULI
load_dotenv(r"C:\RAULI_CORE\credenciales.env")

# Importar sistema de respuesta inmediata
sys.path.append(r"C:\RAULI_CORE")
from respuesta_inmediata import obtener_respuesta

try:
    import telegram
    from telegram import Update, Bot, Audio, Voice
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("❌ Instalando telegram-bot-python...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot"])
    import telegram
    from telegram import Update, Bot, Audio, Voice
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de logging optimizada
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING  # Reducido para menos ruido
)
logger = logging.getLogger(__name__)

class RauliProBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.voice_engine = os.getenv('VOICE_ENGINE', 'system_sapi')
        self.temp_dir = os.getenv('RAULI_TEMP_DIR', r'C:\RAULI_CORE\temp')
        self.audio_dir = os.getenv('RAULI_AUDIO_DIR', r'C:\RAULI_CORE\audio')
        
        # Crear directorios
        Path(self.temp_dir).mkdir(exist_ok=True)
        Path(self.audio_dir).mkdir(exist_ok=True)
        
        # Estado del bot
        self.is_processing = {}  # Para evitar respuestas duplicadas
        self.response_queue = queue.Queue()
        self.voice_cache = {}
        
        # Contexto de conversación por usuario
        self.conversations = {}
        
        logger.info("🚀 RAULI-PRO Bot inicializado para respuesta inmediata")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bienvenida instantánea"""
        user = update.effective_user
        user_id = user.id
        
        # Inicializar contexto de usuario
        self.conversations[user_id] = {
            'name': user.first_name,
            'context': [],
            'last_interaction': time.time(),
            'language': user.language_code or 'es',
            'preferences': {
                'voice_response': True,
                'quick_mode': True
            }
        }
        
        welcome_msg = f"""
🎉 ¡Hola {user.first_name}! Soy **RAULI-PRO**, tu asistente instantáneo.

🚀 **RESPUESTA INMEDIATA:**
• Habla naturalmente 🎤 → Te respondo al instante
• Escribe normalmente 💬 → Te contesto con voz
• Sin comandos, sin esperas ⚡

🤖 **CAPACIDADES INMEDIATAS:**
• Programación y código al momento
• Análisis y soluciones rápidas
• Control de tu sistema (ojos, manos, boca)
• Conversación natural permanente

💬 **PRUEBA AHORA:**
Di "Hola Rauli" o "Ayúdame con..."

¡Te responderé inmediatamente! ⚡
        """
        
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
        
        # Respuesta de voz instantánea
        await self.hablar_inmediato(f"Hola {user.first_name}, soy Rauli Pro. Te responderé al instante. Habla cuando quieras.")
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejo instantáneo de voz"""
        user = update.effective_user
        user_id = user.id
        voice = update.message.voice
        
        # Evitar procesamiento duplicado
        if user_id in self.is_processing:
            return
        self.is_processing[user_id] = True
        
        try:
            # Actualizar contexto
            if user_id not in self.conversations:
                await self.start(update, context)
            
            self.conversations[user_id]['last_interaction'] = time.time()
            
            logger.info(f"🎤 Voz de {user.first_name} - Procesamiento inmediato")
            
            # Descargar audio en background
            audio_file = await voice.get_file()
            audio_path = os.path.join(self.temp_dir, f"voice_{user_id}_{int(time.time())}.ogg")
            await audio_file.download_to_drive(audio_path)
            
            # Procesamiento asíncrono rápido
            texto_usuario = await self.voice_to_text_rapido(audio_path)
            
            if texto_usuario:
                logger.info(f"📝 {user.first_name}: {texto_usuario}")
                
                # Agregar al contexto
                self.conversations[user_id]['context'].append(f"Usuario: {texto_usuario}")
                if len(self.conversations[user_id]['context']) > 10:
                    self.conversations[user_id]['context'].pop(0)
                
                # Respuesta inmediata
                respuesta = await self.generar_respuesta_inmediata(texto_usuario, user_id)
                
                # Agregar respuesta al contexto
                self.conversations[user_id]['context'].append(f"Rauli: {respuesta}")
                
                # Respuesta de voz instantánea
                await self.hablar_inmediato(respuesta)
                
                # Confirmación visual
                await update.message.reply_text(f"🎤 Escuché: \"{texto_usuario}\"")
                
            else:
                await self.hablar_inmediato("No te entendí bien. ¿Puedes repetirlo o escribirlo?")
                await update.message.reply_text("❌ No pude entender. ¿Puedes repetir?")
                
        except Exception as e:
            logger.error(f"❌ Error en voz: {e}")
            await update.message.reply_text("❌ Error procesando audio")
        
        finally:
            # Liberar procesamiento
            if user_id in self.is_processing:
                del self.is_processing[user_id]
            
            # Limpiar archivo
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejo instantáneo de texto"""
        user = update.effective_user
        user_id = user.id
        texto = update.message.text
        
        # Evitar procesamiento duplicado
        if user_id in self.is_processing:
            return
        self.is_processing[user_id] = True
        
        try:
            # Actualizar contexto
            if user_id not in self.conversations:
                await self.start(update, context)
            
            self.conversations[user_id]['last_interaction'] = time.time()
            
            logger.info(f"💬 Texto de {user.first_name}: {texto}")
            
            # Agregar al contexto
            self.conversations[user_id]['context'].append(f"Usuario: {texto}")
            if len(self.conversations[user_id]['context']) > 10:
                self.conversations[user_id]['context'].pop(0)
            
            # Respuesta inmediata
            respuesta = await self.generar_respuesta_inmediata(texto, user_id)
            
            # Agregar respuesta al contexto
            self.conversations[user_id]['context'].append(f"Rauli: {respuesta}")
            
            # Respuesta de voz instantánea
            await self.hablar_inmediato(respuesta)
            
            # Confirmación visual
            await update.message.reply_text(f"💬 {respuesta}")
            
        except Exception as e:
            logger.error(f"❌ Error en texto: {e}")
            await update.message.reply_text("❌ Error procesando mensaje")
        
        finally:
            # Liberar procesamiento
            if user_id in self.is_processing:
                del self.is_processing[user_id]
    
    async def voice_to_text_rapido(self, audio_path):
        """Conversión rápida de voz a texto"""
        try:
            # Usar caché si existe
            audio_hash = os.path.getsize(audio_path)
            if audio_hash in self.voice_cache:
                return self.voice_cache[audio_hash]
            
            # Intentar con OpenAI Whisper
            if os.getenv('OPENAI_API_KEY'):
                import openai
                client = openai.OpenAI()
                
                with open(audio_path, 'rb') as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="es",
                        temperature=0.1  # Más preciso
                    )
                    
                    resultado = transcript.text.strip()
                    self.voice_cache[audio_hash] = resultado
                    return resultado
            else:
                # Fallback rápido
                logger.warning("⚠️ Sin OpenAI, usando reconocimiento simulado")
                return "Mensaje de voz recibido"
                
        except Exception as e:
            logger.error(f"❌ Error voice_to_text: {e}")
            return None
    
    async def generar_respuesta_inmediata(self, texto, user_id):
        """Generación de respuesta ultra-rápida usando sistema cacheado"""
        user_context = self.conversations.get(user_id, {})
        
        # Usar sistema de respuesta inmediata optimizado
        respuesta = obtener_respuesta(texto, user_context)
        
        return respuesta
    
    async def hablar_inmediato(self, texto):
        """Respuesta de voz instantánea"""
        def hablar_bg():
            try:
                subprocess.run([
                    sys.executable,
                    r"C:\RAULI_CORE\boca.py",
                    texto
                ], capture_output=True, text=True, timeout=15)
            except:
                pass  # Silencioso para no bloquear
        
        # Ejecutar en background para no bloquear
        threading.Thread(target=hablar_bg, daemon=True).start()
        return True
    
    def ejecutar_comando_async(self, comando):
        """Ejecución asíncrona de comandos RAULI"""
        try:
            if comando == "ojos":
                subprocess.run([
                    sys.executable,
                    r"C:\RAULI_CORE\ojos.py"
                ], capture_output=True, text=True, timeout=30)
            elif comando == "manos":
                subprocess.run([
                    sys.executable,
                    r"C:\RAULI_CORE\manos.py",
                    "click_izquierdo"
                ], capture_output=True, text=True, timeout=30)
        except:
            pass
    
    def run(self):
        """Inicio del bot con respuesta inmediata"""
        if not self.token:
            print("❌ TELEGRAM_BOT_TOKEN no configurado")
            return
        
        application = Application.builder().token(self.token).build()
        
        # Handlers optimizados para respuesta rápida
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        print("🚀 RAULI-PRO Bot iniciado - Respuesta inmediata activada")
        
        # Iniciar con polling optimizado
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

def main():
    """Inicio principal"""
    print("🚀 INICIANDO RAULI-PRO - RESPUESTA INMEDIATA")
    
    # Verificar credenciales
    if not os.path.exists(r"C:\RAULI_CORE\credenciales.env"):
        print("❌ Archivo de credenciales no encontrado")
        return
    
    # Iniciar bot pro
    bot = RauliProBot()
    bot.run()

if __name__ == "__main__":
    main()
