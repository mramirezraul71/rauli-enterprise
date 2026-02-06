#!/usr/bin/env python3
"""
👑 RAULI-PERMANENTE - Sistema de comunicación permanente
Funciona incluso si cambiamos de chat o cerramos la sesión
"""

import os
import sys
import json
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Cargar credenciales RAULI
load_dotenv(r"C:\RAULI_CORE\credenciales.env")

class RauliPermanente:
    def __init__(self):
        self.core_dir = Path(r"C:\RAULI_CORE")
        self.config_file = self.core_dir / "rauli_permanente.json"
        self.log_file = self.core_dir / "rauli_permanente.log"
        self.state_file = self.core_dir / "rauli_state.json"
        
        # Crear directorios
        self.core_dir.mkdir(exist_ok=True)
        
        # Estado permanente
        self.estado = self.cargar_estado()
        self.conversaciones = self.estado.get('conversaciones', {})
        self.configuracion = self.estado.get('configuracion', {})
        self.sesion_actual = self.estado.get('sesion_actual', {})
        
        # Configurar logging permanente
        self.setup_logging()
        
        logger.info("👑 RAULI-PERMANENTE inicializado")
    
    def setup_logging(self):
        """Configura logging permanente"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        global logger
        logger = logging.getLogger('RauliPermanente')
    
    def cargar_estado(self):
        """Carga estado permanente desde archivo"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.crear_estado_inicial()
        except Exception as e:
            logger.error(f"❌ Error cargando estado: {e}")
            return self.crear_estado_inicial()
    
    def crear_estado_inicial(self):
        """Crea estado inicial"""
        return {
            'conversaciones': {},
            'configuracion': {
                'voz_activa': True,
                'respuestas_audio': True,
                'idioma': 'es',
                'voz_nombre': 'Microsoft Sabina Desktop'
            },
            'sesion_actual': {
                'inicio': datetime.now().isoformat(),
                'chat_actual': None,
                'usuario_actual': None
            },
            'estadisticas': {
                'mensajes_totales': 0,
                'respuestas_audio': 0,
                'sesiones_activas': 0
            }
        }
    
    def guardar_estado(self):
        """Guarda estado permanente"""
        try:
            self.estado['ultima_actualizacion'] = datetime.now().isoformat()
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.estado, f, indent=2, ensure_ascii=False)
            logger.info("✅ Estado guardado")
        except Exception as e:
            logger.error(f"❌ Error guardando estado: {e}")
    
    def registrar_conversacion(self, chat_id, usuario_info):
        """Registra nueva conversación"""
        chat_key = str(chat_id)
        
        if chat_key not in self.conversaciones:
            self.conversaciones[chat_key] = {
                'chat_id': chat_id,
                'usuario': usuario_info,
                'inicio': datetime.now().isoformat(),
                'ultimo_mensaje': datetime.now().isoformat(),
                'mensajes': [],
                'contexto': [],
                'preferencias': {
                    'voz_activa': True,
                    'idioma': 'es'
                }
            }
            logger.info(f"🆕 Nueva conversación: {chat_key}")
        
        # Actualizar sesión actual
        self.sesion_actual['chat_actual'] = chat_key
        self.sesion_actual['usuario_actual'] = usuario_info
        self.sesion_actual['ultimo_cambio'] = datetime.now().isoformat()
        
        self.guardar_estado()
        return self.conversaciones[chat_key]
    
    def agregar_mensaje(self, chat_id, tipo, contenido, metadata=None):
        """Agrega mensaje a la conversación"""
        chat_key = str(chat_id)
        
        if chat_key in self.conversaciones:
            mensaje = {
                'timestamp': datetime.now().isoformat(),
                'tipo': tipo,  # 'usuario_voz', 'usuario_texto', 'rauli_voz', 'rauli_texto'
                'contenido': contenido,
                'metadata': metadata or {}
            }
            
            self.conversaciones[chat_key]['mensajes'].append(mensaje)
            self.conversaciones[chat_key]['ultimo_mensaje'] = datetime.now().isoformat()
            
            # Mantener solo últimos 50 mensajes
            if len(self.conversaciones[chat_key]['mensajes']) > 50:
                self.conversaciones[chat_key]['mensajes'] = self.conversaciones[chat_key]['mensajes'][-50:]
            
            # Actualizar estadísticas
            self.estado['estadisticas']['mensajes_totales'] += 1
            if tipo == 'rauli_voz':
                self.estado['estadisticas']['respuestas_audio'] += 1
            
            self.guardar_estado()
            logger.info(f"💬 Mensaje agregado: {chat_key} - {tipo}")
    
    def obtener_contexto(self, chat_id, cantidad=10):
        """Obtiene contexto de conversación"""
        chat_key = str(chat_id)
        
        if chat_key in self.conversaciones:
            mensajes = self.conversaciones[chat_key]['mensajes']
            return mensajes[-cantidad:] if len(mensajes) > cantidad else mensajes
        return []
    
    def actualizar_preferencias(self, chat_id, preferencias):
        """Actualiza preferencias de usuario"""
        chat_key = str(chat_id)
        
        if chat_key in self.conversaciones:
            self.conversaciones[chat_key]['preferencias'].update(preferencias)
            self.guardar_estado()
            logger.info(f"⚙️ Preferencias actualizadas: {chat_key}")
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas completas"""
        stats = self.estado['estadisticas'].copy()
        stats['conversaciones_activas'] = len(self.conversaciones)
        stats['sesion_actual'] = self.sesion_actual
        
        # Conversaciones recientes (últimas 24 horas)
        ahora = datetime.now()
        recientes = 0
        for conv in self.conversaciones.values():
            ultimo = datetime.fromisoformat(conv['ultimo_mensaje'])
            if ahora - ultimo < timedelta(hours=24):
                recientes += 1
        stats['conversaciones_recientes'] = recientes
        
        return stats
    
    def limpiar_conversaciones_antiguas(self, dias=7):
        """Limpia conversaciones antiguas"""
        ahora = datetime.now()
        limite = ahora - timedelta(days=dias)
        
        antiguas = []
        for chat_key, conv in self.conversaciones.items():
            ultimo = datetime.fromisoformat(conv['ultimo_mensaje'])
            if ultimo < limite:
                antiguas.append(chat_key)
        
        for chat_key in antiguas:
            del self.conversaciones[chat_key]
            logger.info(f"🗑️ Conversación eliminada: {chat_key}")
        
        if antiguas:
            self.guardar_estado()
            logger.info(f"🧹 Limpieza completada: {len(antiguas)} conversaciones")
    
    def crear_servicio_permanente(self):
        """Crea script de servicio permanente"""
        servicio_script = self.core_dir / "rauli_servicio.py"
        
        script_content = '''#!/usr/bin/env python3
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
'''
        
        with open(servicio_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ Servicio permanente creado: {servicio_script}")
        return servicio_script
    
    def crear_acceso_directo(self):
        """Crea acceso directo para inicio automático"""
        try:
            import win32com.client
            
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, "RAULI-PERMANENTE.lnk")
            
            target = str(self.core_dir / "rauli_servicio.py")
            working_dir = str(self.core_dir)
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = working_dir
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print(f"✅ Acceso directo creado: {shortcut_path}")
            return shortcut_path
            
        except Exception as e:
            print(f"❌ Error creando acceso directo: {e}")
            return None
    
    def instalar_permanente(self):
        """Instala el sistema permanentemente"""
        print("🔧 Instalando RAULI-PERMANENTE...")
        
        # Crear servicio
        servicio_script = self.crear_servicio_permanente()
        
        # Crear acceso directo
        acceso_directo = self.crear_acceso_directo()
        
        # Guardar instalación
        self.estado['instalacion'] = {
            'fecha': datetime.now().isoformat(),
            'servicio': str(servicio_script),
            'acceso_directo': str(acceso_directo) if acceso_directo else None,
            'version': '1.0.0'
        }
        
        self.guardar_estado()
        
        print("✅ RAULI-PERMANENTE instalado correctamente")
        print("🚀 Usa el acceso directo en el escritorio para iniciar")

# Instancia global
rauli_permanente = RauliPermanente()

def obtener_rauli_permanente():
    """Obtiene instancia del sistema permanente"""
    return rauli_permanente

def main():
    """Función principal de instalación"""
    print("👑 RAULI-PERMANENTE - Sistema de comunicación permanente")
    print("=" * 60)
    
    rauli = obtener_rauli_permanente()
    
    # Mostrar estado actual
    stats = rauli.obtener_estadisticas()
    print(f"📊 Estadísticas actuales:")
    print(f"   - Conversaciones totales: {stats['conversaciones_activas']}")
    print(f"   - Mensajes totales: {stats['mensajes_totales']}")
    print(f"   - Respuestas de audio: {stats['respuestas_audio']}")
    print(f"   - Conversaciones recientes: {stats['conversaciones_recientes']}")
    
    # Instalar sistema permanente
    if len(sys.argv) > 1 and sys.argv[1] == "--instalar":
        rauli.instalar_permanente()
    
    # Limpiar si se solicita
    elif len(sys.argv) > 1 and sys.argv[1] == "--limpiar":
        rauli.limpiar_conversaciones_antiguas()
    
    else:
        print("\n📋 Opciones disponibles:")
        print("   python rauli_permanente.py --instalar  # Instalar sistema permanente")
        print("   python rauli_permanente.py --limpiar   # Limpiar conversaciones antiguas")

if __name__ == "__main__":
    main()
