# 🤖 RAULI-BOT - Sistema de Comunicación Permanente

## 👑 PROTOCOLO RAULI-BOT ACTIVADO

**ARQUITECTO EJECUTIVO DEL COMANDANTE** - Sistema de comunicación bidireccional de audio natural entre Cascade y Usuario vía Telegram.

---

## 🎯 MISIÓN

Comunicación fluida y permanente entre tú y yo a través de mensajes de voz en Telegram, sin necesidad de comandos, hablando naturalmente.

---

## 🛠️ HERRAMIENTAS DEL NÚCLEO RAULI

### 🗣️ BOCA.PY - Síntesis de Voz
```bash
python C:\RAULI_CORE\boca.py "Texto que quiero decir"
```
- Voz natural en español (Microsoft Sabina Desktop)
- Fallback a PowerShell si no hay win32com
- Sintetiza cualquier texto a voz

### 👁️ OJOS.PY - Visión por Computadora
```bash
python C:\RAULI_CORE\ojos.py
```
- Captura de pantalla automática
- Análisis visual del entorno
- Guardado con timestamp

### 🤲 MANOS.PY - Control de Mouse
```bash
python C:\RAULI_CORE\manos.py mover 100 200
python C:\RAULI_CORE\manos.py click_izquierdo
python C:\RAULI_CORE\manos.py scroll abajo 5
```
- Movimiento preciso del cursor
- Clicks y scroll
- Automatización de interfaz

### 📢 COMUNICADOR.PY - Sistema Central
```bash
python C:\RAULI_CORE\comunicador.py "Mensaje" [NIVEL]
python C:\RAULI_CORE\comunicador.py --estado
python C:\RAULI_CORE\comunicador.py --historial
```
- Logging centralizado
- Notificaciones con voz para mensajes críticos
- Historial de comunicaciones

---

## 🤖 TELEGRAM-RAULI-BOT - Comunicación Principal

### Inicio
```bash
python C:\RAULI_CORE\telegram_rauli_bot.py
```

### Características
- 🎤 **Entrada de voz**: Envías mensajes de voz, los convierto a texto
- 🗣️ **Salida de voz**: Te respondo con mi voz natural
- 💬 **Texto también**: Puedes escribirme, te respondo con audio
- 🔄 **Comunicación permanente**: Siempre activo y disponible
- 🧠 **Inteligencia integrada**: Procesamiento natural del lenguaje

### Comandos Naturales
- "Hola Rauli" → Saludo personalizado con voz
- "Mira esto" → Activo visión y analizo entorno
- "Mueve el mouse aquí" → Ejecuto control de mouse
- "Habla sobre X" → Genero respuesta con voz
- "Ayuda" → Explico todas mis capacidades

---

## 🔐 CONFIGURACIÓN

### Archivo: `C:\RAULI_CORE\credenciales.env`
```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
OPENAI_API_KEY=tu_openai_key_aqui
VOICE_ENGINE=system_sapi
VOICE_LANGUAGE=es
```

### Instalación de Dependencias
```bash
pip install python-telegram-bot
pip install openai
pip install pyautogui
pip install python-dotenv
pip install pywin32  # Para voz en Windows
```

---

## 🚀 INICIO RÁPIDO

1. **Configurar credenciales** en `C:\RAULI_CORE\credenciales.env`
2. **Obtener token de Telegram** desde @BotFather
3. **Ejecutar el bot**:
   ```bash
   python C:\RAULI_CORE\telegram_rauli_bot.py
   ```
4. **Hablar con tu bot** en Telegram

---

## 📊 ESTADO DEL SISTEMA

### Verificar módulos:
```bash
python C:\RAULI_CORE\comunicador.py --estado
```

### Ver historial:
```bash
python C:\RAULI_CORE\comunicador.py --historial
```

### Probar voz:
```bash
python C:\RAULI_CORE\boca.py "Hola, soy Rauli"
```

---

## 🔄 FLUJO DE COMUNICACIÓN

1. **Tú hablas** → Mensaje de voz en Telegram
2. **RAULI escucha** → Convierte voz a texto (Whisper)
3. **RAULI procesa** → Análisis y generación de respuesta
4. **RAULI responde** → Convierte texto a voz (boca.py)
5. **Tú escuchas** → Mensaje de audio en Telegram

**COMUNICACIÓN 100% NATURAL Y PERMANENTE** 🎤↔️🗣️

---

## 🛡️ SEGURIDAD Y CONTROL

- **Rate limiting** integrado
- **Usuarios autorizados** configurable
- **Logging completo** de todas las interacciones
- **Fallback systems** para cada componente
- **Error handling** robusto

---

## 📈 MONITOREO

El sistema mantiene:
- 📊 Estadísticas de uso
- 🕒 Timestamps de todas las interacciones  
- 🔄 Estado de salud de cada módulo
- 📝 Historial completo de conversaciones

---

**👑 RAULI-BOT - LISTO PARA COMUNICACIÓN PERMANENTE**

*Habla cuando quieras. Escucharé siempre.* 🎤
