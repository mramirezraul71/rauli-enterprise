#!/usr/bin/env python3
"""
🎤 TELEGRAM-RAULI-AUDIO - Bot especializado en respuestas de audio
TODAS las respuestas son mensajes de audio - comunicación 100% auditiva
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

# Importar generador de audio
sys.path.append(r"C:\RAULI_CORE")
from generador_audio import generar_audio_para_texto

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
    level=logging.WARNING
)
logger = logging.getLogger(__name__)

class RauliAudioBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.voice_engine = os.getenv('VOICE_ENGINE', 'system_sapi')
        self.temp_dir = os.getenv('RAULI_TEMP_DIR', r'C:\RAULI_CORE\temp')
        self.audio_dir = os.getenv('RAULI_AUDIO_DIR', r'C:\RAULI_CORE\audio')
        
        # Crear directorios
        Path(self.temp_dir).mkdir(exist_ok=True)
        Path(self.audio_dir).mkdir(exist_ok=True)
        
        # Estado del bot
        self.is_processing = {}
        self.audio_cache = {}
        self.conversations = {}
        
        logger.info("🎤 RAULI-AUDIO Bot inicializado - Respuestas 100% de audio")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bienvenida con audio"""
        user = update.effective_user
        user_id = user.id
        
        # Inicializar contexto
        self.conversations[user_id] = {
            'name': user.first_name,
            'context': [],
            'last_interaction': time.time(),
            'language': user.language_code or 'es'
        }
        
        # Mensaje de texto inicial
        welcome_text = f"🎤 ¡Hola {user.first_name}! Soy **RAULI-AUDIO**.\n\n🗣️ **TODAS mis respuestas son de AUDIO**\n🎤 Habla o escribe → Te responderé con mi voz\n⚡ Comunicación 100% auditiva y natural\n\n¡Prueba enviando cualquier mensaje!"
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        
        # Respuesta de voz inmediata
        await self.responder_con_audio(f"Hola {user.first_name}, soy Rauli Audio. Todas mis respuestas serán mensajes de audio. Habla cuando quieras.", update)
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa voz del usuario y responde con audio"""
        user = update.effective_user
        user_id = user.id
        voice = update.message.voice
        
        if user_id in self.is_processing:
            return
        self.is_processing[user_id] = True
        
        try:
            if user_id not in self.conversations:
                await self.start(update, context)
            
            self.conversations[user_id]['last_interaction'] = time.time()
            
            logger.info(f"🎤 Voz de {user.first_name} - Respuesta de audio")
            
            # Descargar audio
            audio_file = await voice.get_file()
            audio_path = os.path.join(self.temp_dir, f"voice_{user_id}_{int(time.time())}.ogg")
            await audio_file.download_to_drive(audio_path)
            
            # Convertir voz a texto
            texto_usuario = await self.voice_to_text(audio_path)
            
            if texto_usuario:
                logger.info(f"📝 {user.first_name}: {texto_usuario}")
                
                # Agregar al contexto
                self.conversations[user_id]['context'].append(f"Usuario: {texto_usuario}")
                if len(self.conversations[user_id]['context']) > 10:
                    self.conversations[user_id]['context'].pop(0)
                
                # Generar respuesta
                respuesta = await self.generar_respuesta_audio(texto_usuario, user_id)
                
                # Agregar respuesta al contexto
                self.conversations[user_id]['context'].append(f"Rauli: {respuesta}")
                
                # Responder ÚNICAMENTE con audio
                await self.responder_con_audio(respuesta, update)
                
            else:
                await self.responder_con_audio("No te entendí bien. ¿Puedes repetirlo o escribirlo?", update)
                
        except Exception as e:
            logger.error(f"❌ Error en voz: {e}")
            await self.responder_con_audio("Error procesando tu mensaje de audio", update)
        
        finally:
            if user_id in self.is_processing:
                del self.is_processing[user_id]
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa texto del usuario y responde con audio"""
        user = update.effective_user
        user_id = user.id
        texto = update.message.text
        
        if user_id in self.is_processing:
            return
        self.is_processing[user_id] = True
        
        try:
            if user_id not in self.conversations:
                await self.start(update, context)
            
            self.conversations[user_id]['last_interaction'] = time.time()
            
            logger.info(f"💬 Texto de {user.first_name}: {texto}")
            
            # Agregar al contexto
            self.conversations[user_id]['context'].append(f"Usuario: {texto}")
            if len(self.conversations[user_id]['context']) > 10:
                self.conversations[user_id]['context'].pop(0)
            
            # Generar respuesta
            respuesta = await self.generar_respuesta_audio(texto, user_id)
            
            # Agregar respuesta al contexto
            self.conversations[user_id]['context'].append(f"Rauli: {respuesta}")
            
            # Responder ÚNICAMENTE con audio
            await self.responder_con_audio(respuesta, update)
            
        except Exception as e:
            logger.error(f"❌ Error en texto: {e}")
            await self.responder_con_audio("Error procesando tu mensaje", update)
        
        finally:
            if user_id in self.is_processing:
                del self.is_processing[user_id]
    
    async def voice_to_text(self, audio_path):
        """Convierte audio a texto"""
        try:
            if os.getenv('OPENAI_API_KEY'):
                import openai
                client = openai.OpenAI()
                
                with open(audio_path, 'rb') as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="es",
                        temperature=0.1
                    )
                    return transcript.text.strip()
            else:
                return "Mensaje de voz recibido"
                
        except Exception as e:
            logger.error(f"❌ Error voice_to_text: {e}")
            return None
    
    async def generar_respuesta_audio(self, texto, user_id):
        """Genera respuesta optimizada para audio"""
        texto_lower = texto.lower().strip()
        user_context = self.conversations.get(user_id, {})
        user_name = user_context.get('name', 'amigo')
        
        # Respuestas naturales y conversacionales
        if any(saludo in texto_lower for saludo in ['hola', 'buenos días', 'buenas tardes', 'hey']):
            return f"Hola {user_name}. Soy Rauli y te responderé siempre con voz. ¿En qué te ayudo?"
        
        elif any(estado in texto_lower for estado in ['cómo estás', 'qué tal']):
            return "Estoy excelente y listo para ayudarte. Todas mis respuestas serán de audio para una comunicación más natural."
        
        elif any(despedida in texto_lower for despedida in ['adiós', 'chao', 'hasta luego']):
            return f"Hasta luego {user_name}. Estaré aquí cuando quieras hablar conmigo por audio."
        
        elif any(gracias in texto_lower for gracias in ['gracias', 'thank']):
            return "De nada siempre es un placer ayudarte. ¿Hay algo más en lo que pueda colaborar contigo?"
        
        elif any(ayuda in texto_lower for ayuda in ['ayuda', 'ayúdame', 'necesito ayuda']):
            return "Entiendo que necesitas ayuda. Puedo asistirte con programación, código, errores, análisis de sistemas y mucho más. Todo te lo responderé con voz. ¿Cuál es tu problema?"
        
        elif any(capacidad in texto_lower for capacidad in ['qué puedes hacer', 'capacidades']):
            return "Soy Rauli, especialista en asistencia técnica. Puedo ayudarte con desarrollo de software, debugging, arquitectura, bases de datos, APIs y automatización. Todas mis respuestas serán mensajes de audio para una comunicación fluida."
        
        # Comandos del sistema RAULI
        elif 'mira' in texto_lower or 'ojos' in texto_lower:
            threading.Thread(target=self.ejecutar_comando_async, args=('ojos',)).start()
            return "Activando mi sistema de visión. Analizando el entorno visual ahora mismo."
        
        elif 'mueve' in texto_lower or 'manos' in texto_lower:
            threading.Thread(target=self.ejecutar_comando_async, args=('manos',)).start()
            return "Activando sistema de control. Listo para mover el mouse o interactuar con la interfaz."
        
        elif 'habla' in texto_lower or 'di' in texto_lower:
            frase = texto.replace('habla', '').replace('di', '').strip()
            if frase:
                await self.hablar_directo(frase)
                return f"Acabo de decir: {frase}"
            else:
                return "¿Qué quieres que diga con mi voz?"
        
        # Detección de intenciones técnicas
        elif any(tech in texto_lower for tech in ['error', 'bug', 'problema', 'fallo']):
            return "Detecto que tienes un problema técnico. Describe el error específico y te ayudaré a solucionarlo paso a paso."
        
        elif any(tech in texto_lower for tech in ['código', 'programar', 'desarrollo']):
            return "Necesitas ayuda con programación. Puedo asistirte con múltiples lenguajes, debugging, optimización y mejores prácticas. Cuéntame más detalles."
        
        elif any(tech in texto_lower for tech in ['api', 'endpoint', 'servicio']):
            return "Las APIs son mi especialidad. Puedo ayudarte a crear, consumir, depurar o optimizar servicios web. ¿Qué tipo de API necesitas?"
        
        elif any(tech in texto_lower for tech in ['base de datos', 'database', 'sql']):
            return "Puedo ayudarte con diseño de bases de datos, consultas SQL, optimización, migración o cualquier tema relacionado con almacenamiento de datos."
        
        # Respuesta contextual inteligente
        elif len(user_context.get('context', [])) > 2:
            return "Entiendo tu consulta. Basándome en nuestra conversación, estoy listo para ayudarte. ¿Podrías darme más detalles sobre lo que necesitas?"
        
        # Respuesta por defecto natural
        else:
            return f"Entiendo que me consultas sobre {texto}. Como tu asistente de voz, estoy aquí para ayudarte con cualquier tarea técnica. ¿En qué puedo ser útil para ti?"
    
    async def responder_con_audio(self, texto, update):
        """Genera y envía respuesta de audio"""
        try:
            # Generar archivo de audio
            audio_path = await self.generar_audio_archivo(texto)
            
            if audio_path and os.path.exists(audio_path):
                # Enviar archivo de audio a Telegram
                with open(audio_path, 'rb') as audio_file:
                    await update.message.reply_voice(
                        voice=audio_file,
                        caption=None  # Sin texto, solo audio
                    )
                
                # Limpiar archivo temporal
                os.remove(audio_path)
                logger.info(f"🎤 Audio enviado: {texto[:50]}...")
                return True
            else:
                # Fallback: enviar texto si falla el audio
                await update.message.reply_text(f"🎤 {texto}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error enviando audio: {e}")
            await update.message.reply_text(f"🎤 {texto}")
            return False
    
    async def generar_audio_archivo(self, texto):
        """Genera archivo de audio usando el nuevo generador"""
        try:
            # Usar el generador de audio robusto
            audio_path = generar_audio_para_texto(texto)
            
            if audio_path and os.path.exists(audio_path):
                # Verificar tamaño del archivo
                size = os.path.getsize(audio_path)
                if size > 1024:  # Al menos 1KB
                    logger.info(f"✅ Audio generado: {audio_path} ({size} bytes)")
                    return audio_path
                else:
                    logger.error(f"❌ Audio demasiado pequeño: {size} bytes")
                    return None
            else:
                logger.error("❌ No se pudo generar audio")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error generando audio: {e}")
            return None
    
    async def hablar_directo(self, texto):
        """Habla directamente sin archivo"""
        def hablar_bg():
            try:
                subprocess.run([
                    sys.executable,
                    r"C:\RAULI_CORE\boca.py",
                    texto
                ], capture_output=True, text=True, timeout=10)
            except:
                pass
        
        threading.Thread(target=hablar_bg, daemon=True).start()
    
    def ejecutar_comando_async(self, comando):
        """Ejecuta comandos RAULI en background"""
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
        """Inicia el bot de audio"""
        if not self.token:
            print("❌ TELEGRAM_BOT_TOKEN no configurado")
            return
        
        application = Application.builder().token(self.token).build()
        
        # Handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        print("🎤 RAULI-AUDIO Bot iniciado - Todas las respuestas serán de audio")
        
        # Iniciar bot
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

def main():
    """Inicio principal"""
    print("🎤 INICIANDO RAULI-AUDIO - RESPUESTAS 100% DE AUDIO")
    
    if not os.path.exists(r"C:\RAULI_CORE\credenciales.env"):
        print("❌ Archivo de credenciales no encontrado")
        return
    
    bot = RauliAudioBot()
    bot.run()

if __name__ == "__main__":
    main()
