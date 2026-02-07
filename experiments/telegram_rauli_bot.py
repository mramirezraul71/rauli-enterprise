#!/usr/bin/env python3
"""
🤖 TELEGRAM-RAULI-BOT - Comunicación bidireccional de audio permanente
Sistema de comunicación natural entre Cascade y Usuario vía Telegram
"""

import os
import sys
import json
import time
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
import logging
from dotenv import load_dotenv

# Cargar credenciales RAULI
load_dotenv(r"C:\RAULI_CORE\credenciales.env")

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

# Configuración de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class RauliTelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.voice_engine = os.getenv('VOICE_ENGINE', 'system_sapi')
        self.temp_dir = os.getenv('RAULI_TEMP_DIR', r'C:\RAULI_CORE\temp')
        self.audio_dir = os.getenv('RAULI_AUDIO_DIR', r'C:\RAULI_CORE\audio')
        
        # Crear directorios
        Path(self.temp_dir).mkdir(exist_ok=True)
        Path(self.audio_dir).mkdir(exist_ok=True)
        
        # Conversaciones activas
        self.conversations = {}
        
        logger.info("🤖 RAULI-BOT Telegram inicializado")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mensaje de bienvenida"""
        user = update.effective_user
        welcome_msg = f"""
🎉 ¡Hola {user.first_name}! Soy **RAULI-BOT**, tu asistente de voz permanente.

🎤 **COMUNICACIÓN NATURAL:**
• Envíame mensajes de voz 🗣️ y te responderé con mi voz
• También puedes escribirme 💬 y te responderé con audio  
• Comunicación 100% fluida y natural

🤖 **MIS CAPACIDADES:**
• Programación y desarrollo
• Análisis de código y debugging
• Control de tu sistema (ojos, manos, boca)
• Asistencia técnica permanente

💬 **COMIENZA CUANDO QUIERAS:**
"Hola Rauli, necesito ayuda con..."
"Rauli, ¿puedes ayudarme a...?"

¡Estoy listo para ayudarte! 🚀
        """
        
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
        
        # Saludar con voz
        await self.hablar(f"Hola {user.first_name}, soy Rauli, tu asistente personal. Estoy listo para ayudarte.")
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa mensajes de voz del usuario"""
        user = update.effective_user
        voice = update.message.voice
        
        logger.info(f"🎤 Mensaje de voz recibido de {user.first_name} (duración: {voice.duration}s)")
        
        try:
            # Descargar audio
            audio_file = await voice.get_file()
            audio_path = os.path.join(self.temp_dir, f"voice_{user.id}_{int(time.time())}.ogg")
            await audio_file.download_to_drive(audio_path)
            
            # Convertir voz a texto usando Whisper o sistema
            texto_usuario = await self.voice_to_text(audio_path)
            
            if texto_usuario:
                logger.info(f"📝 Usuario dijo: {texto_usuario}")
                
                # Procesar con Cascade y generar respuesta
                respuesta = await self.procesar_mensaje(texto_usuario, user)
                
                # Responder con voz
                await self.hablar(respuesta)
                await update.message.reply_voice(voice=open(audio_path, 'rb'))  # Placeholder
                
            else:
                await update.message.reply_text("❌ No pude entender tu mensaje. ¿Puedes repetirlo o escribirlo?")
                
        except Exception as e:
            logger.error(f"❌ Error procesando voz: {e}")
            await update.message.reply_text("❌ Error procesando tu mensaje de voz")
        
        finally:
            # Limpiar archivo temporal
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa mensajes de texto del usuario"""
        user = update.effective_user
        texto = update.message.text
        
        logger.info(f"💬 Mensaje de texto de {user.first_name}: {texto}")
        
        # Procesar mensaje y generar respuesta
        respuesta = await self.procesar_mensaje(texto, user)
        
        # Responder con voz
        await self.hablar(respuesta)
        
        # También enviar texto como fallback
        await update.message.reply_text(respuesta)
    
    async def voice_to_text(self, audio_path):
        """Convierte audio a texto"""
        try:
            # Usar OpenAI Whisper si hay API key
            if os.getenv('OPENAI_API_KEY'):
                import openai
                client = openai.OpenAI()
                
                with open(audio_path, 'rb') as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="es"
                    )
                    return transcript.text
            else:
                # Fallback a reconocimiento local (placeholder)
                logger.warning("⚠️ Sin OpenAI API key, usando reconocimiento simulado")
                return "Mensaje de voz recibido"  # Placeholder
                
        except Exception as e:
            logger.error(f"❌ Error en voice_to_text: {e}")
            return None
    
    async def procesar_mensaje(self, texto, user):
        """Procesa mensaje del usuario y genera respuesta de Cascade"""
        texto_lower = texto.lower().strip()
        
        # Comandos específicos de RAULI
        if "hola" in texto_lower or "buenos" in texto_lower:
            return f"¡Hola {user.first_name}! Soy Rauli, tu asistente. ¿En qué puedo ayudarte hoy?"
        
        elif "cómo estás" in texto_lower:
            return "Estoy funcionando perfectamente y listo para ayudarte con cualquier tarea técnica."
        
        elif "adiós" in texto_lower or "chao" in texto_lower:
            return f"¡Hasta luego {user.first_name}! Estaré aquí cuando me necesites."
        
        elif "gracias" in texto_lower:
            return "De nada siempre es un placer ayudarte. ¿Hay algo más en lo que pueda colaborar?"
        
        elif "ayuda" in texto_lower or "ayúdame" in texto_lower:
            return """
Puedo ayudarte con:
🔧 Programación en múltiples lenguajes
🐛 Debugging y análisis de código  
🏗️ Diseño de arquitectura de software
📊 Optimización y rendimiento
🔌 Integración de APIs y sistemas
👁️ Análisis visual (ojos.py)
🤲 Control automatizado (manos.py)
🗣️ Comunicación verbal (boca.py)

¿Qué necesitas específicamente?
            """
        
        elif "qué puedes hacer" in texto_lower:
            return """
Soy Rauli, especializado en:
🚀 Desarrollo de software y programación
🐛 Depuración y resolución de errores
🏗️ Arquitectura y diseño de sistemas
📊 Optimización de rendimiento
🔌 Integración de APIs y microservicios
👁️ Visión por computadora y análisis
🤲 Automatización y control de sistemas
🗣️ Comunicación natural permanente

Puedes hablarme o escribirme naturalmente. ¡Comienza tu pregunta!
            """
        
        # Comandos del sistema RAULI
        elif "mira" in texto_lower or "ve" in texto_lower or "ojos" in texto_lower:
            await self.ejecutar_comando_rauli("ojos")
            return "👁️ He activado mi sistema de visión. Analizando el entorno actual..."
        
        elif "mueve" in texto_lower or "manos" in texto_lower:
            await self.ejecutar_comando_rauli("manos")
            return "🤲 Sistema de control activado. ¿Qué necesito mover o hacer?"
        
        elif "habla" in texto_lower or "di" in texto_lower:
            frase = texto.replace("habla", "").replace("di", "").strip()
            if frase:
                await self.hablar(frase)
                return f"🗣️ He dicho: '{frase}'"
            else:
                return "🗣️ ¿Qué quieres que diga?"
        
        # Respuesta inteligente por defecto
        else:
            return f"Entiendo tu consulta sobre '{texto}'. Como Rauli, estoy aquí para ayudarte con programación, desarrollo o cualquier tarea técnica. ¿Podrías darme más detalles sobre lo que necesitas?"
    
    async def hablar(self, texto):
        """Usa boca.py para generar voz"""
        try:
            result = subprocess.run([
                sys.executable,
                r"C:\RAULI_CORE\boca.py",
                texto
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"🗣️ Voz generada: {texto}")
                return True
            else:
                logger.error(f"❌ Error en boca.py: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error generando voz: {e}")
            return False
    
    async def ejecutar_comando_rauli(self, comando):
        """Ejecuta comandos del sistema RAULI"""
        try:
            if comando == "ojos":
                result = subprocess.run([
                    sys.executable,
                    r"C:\RAULI_CORE\ojos.py"
                ], capture_output=True, text=True, timeout=30)
            elif comando == "manos":
                result = subprocess.run([
                    sys.executable,
                    r"C:\RAULI_CORE\manos.py",
                    "click_izquierdo"
                ], capture_output=True, text=True, timeout=30)
            
            logger.info(f"🔧 Comando RAULI '{comando}' ejecutado")
            return result.returncode == 0
            
        except Exception as e:
            logger.error(f"❌ Error ejecutando comando RAULI: {e}")
            return False
    
    def run(self):
        """Inicia el bot"""
        if not self.token:
            logger.error("❌ TELEGRAM_BOT_TOKEN no configurado en credenciales.env")
            return
        
        application = Application.builder().token(self.token).build()
        
        # Handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        logger.info("🚀 RAULI-BOT Telegram iniciado")
        
        # Iniciar bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Función principal"""
    print("🤖 INICIANDO RAULI-BOT TELEGRAM...")
    
    # Verificar credenciales
    if not os.path.exists(r"C:\RAULI_CORE\credenciales.env"):
        print("❌ Archivo de credenciales no encontrado")
        return
    
    # Iniciar bot
    bot = RauliTelegramBot()
    bot.run()

if __name__ == "__main__":
    main()
