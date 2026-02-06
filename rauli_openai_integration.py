#!/usr/bin/env python3
"""
🤖 RAULI OPENAI GPT INTEGRATION
Integración avanzada con OpenAI GPT para conversaciones enterprise
"""

import os
import json
from openai import OpenAI
from datetime import datetime
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv
import streamlit as st
import asyncio
from dataclasses import dataclass
from enum import Enum

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), 'credenciales.env'))

class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class ChatMessage:
    role: MessageRole
    content: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class RAULIOpenAIIntegration:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = "gpt-4-turbo-preview"
        self.max_tokens = 4000
        self.temperature = 0.7
        self.conversation_history: List[ChatMessage] = []
        self.system_prompt = """Eres RAULI, un asistente IA enterprise de última generación. 

Tus características:
- 🤖 IA avanzada con capacidades de razonamiento complejo
- 📊 Especialista en análisis de datos y business intelligence
- 🔧 Experto en automatización y optimización de procesos
- 📱 Conocedor profundo de desarrollo móvil y web
- ☁️ Experto en arquitectura cloud y DevOps
- 🎯 Enfocado en soluciones empresariales escalables

Tu tono:
- Profesional pero accesible
- Técnico cuando es necesario
- Siempre orientado a soluciones
- Proactivo y sugerente

Responde siempre en español y proporciona soluciones prácticas y accionables."""
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.is_configured = True
        else:
            self.client = None
            self.is_configured = False
            logging.warning("OpenAI API key not found")
    
    def add_message(self, role: MessageRole, content: str):
        """Agregar mensaje a la conversación"""
        message = ChatMessage(role=role, content=content)
        self.conversation_history.append(message)
        
        # Mantener historial limitado (últimos 20 mensajes)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_openai_messages(self) -> List[Dict[str, str]]:
        """Convertir mensajes a formato OpenAI"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        for msg in self.conversation_history:
            messages.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        return messages
    
    async def generate_response_async(self, user_message: str) -> str:
        """Generar respuesta asíncrona con OpenAI"""
        if not self.is_configured:
            return "❌ OpenAI no está configurado. Por favor verifica tu API key."
        
        try:
            # Agregar mensaje del usuario
            self.add_message(MessageRole.USER, user_message)
            
            # Obtener mensajes en formato OpenAI
            messages = self.get_openai_messages()
            
            # Llamada a OpenAI
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            assistant_message = response.choices[0].message.content
            
            # Agregar respuesta del asistente
            self.add_message(MessageRole.ASSISTANT, assistant_message)
            
            return assistant_message
            
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return f"❌ Error en la API de OpenAI: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return f"❌ Error inesperado: {str(e)}"
    
    def generate_response(self, user_message: str) -> str:
        """Generar respuesta síncrona con OpenAI"""
        if not self.is_configured:
            return "❌ OpenAI no está configurado. Por favor verifica tu API key."
        
        try:
            # Agregar mensaje del usuario
            self.add_message(MessageRole.USER, user_message)
            
            # Obtener mensajes en formato OpenAI
            messages = self.get_openai_messages()
            
            # Llamada a OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            assistant_message = response.choices[0].message.content
            
            # Agregar respuesta del asistente
            self.add_message(MessageRole.ASSISTANT, assistant_message)
            
            return assistant_message
            
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return f"❌ Error en la API de OpenAI: {str(e)}"
    
    def clear_conversation(self):
        """Limpiar historial de conversación"""
        self.conversation_history.clear()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Obtener resumen de la conversación"""
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len([m for m in self.conversation_history if m.role == MessageRole.USER]),
            "assistant_messages": len([m for m in self.conversation_history if m.role == MessageRole.ASSISTANT]),
            "last_message": self.conversation_history[-1].content if self.conversation_history else None,
            "is_configured": self.is_configured,
            "model": self.model
        }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analizar sentimiento del texto (simulado con OpenAI)"""
        if not self.is_configured:
            return {"sentiment": "neutral", "confidence": 0.0}
        
        try:
            messages = [
                {"role": "system", "content": "Analiza el sentimiento del siguiente texto y responde únicamente en formato JSON: {\"sentiment\": \"positive/negative/neutral\", \"confidence\": 0.0}"},
                {"role": "user", "content": text}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=100,
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logging.error(f"Sentiment analysis error: {e}")
            return {"sentiment": "neutral", "confidence": 0.0}

# Integración con Streamlit
class StreamlitOpenAIChat:
    def __init__(self):
        self.openai_client = RAULIOpenAIIntegration()
        
        # Inicializar session state
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        
        if 'openai_client' not in st.session_state:
            st.session_state.openai_client = self.openai_client
    
    def render_chat_interface(self):
        """Renderizar interface de chat en Streamlit"""
        st.header("🤖 Chat con RAULI IA")
        
        # Verificar configuración
        if not self.openai_client.is_configured:
            st.error("❌ OpenAI no está configurado. Verifica tu API key.")
            return
        
        # Mostrar mensajes anteriores
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input para nuevo mensaje
        if prompt := st.chat_input("Escribe tu mensaje para RAULI..."):
            # Agregar mensaje del usuario
            st.session_state.chat_messages.append({
                "role": "user",
                "content": prompt
            })
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generar respuesta
            with st.chat_message("assistant"):
                with st.spinner("RAULI está pensando..."):
                    response = self.openai_client.generate_response(prompt)
                    st.markdown(response)
            
            # Agregar respuesta del asistente
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": response
            })
        
        # Botones de control
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Limpiar Chat"):
                st.session_state.chat_messages.clear()
                self.openai_client.clear_conversation()
                st.rerun()
        
        with col2:
            if st.button("📊 Estadísticas"):
                summary = self.openai_client.get_conversation_summary()
                st.json(summary)
        
        with col3:
            if st.button("💾 Exportar Chat"):
                chat_data = {
                    "timestamp": datetime.now().isoformat(),
                    "messages": st.session_state.chat_messages,
                    "summary": self.openai_client.get_conversation_summary()
                }
                st.download_button(
                    label="📥 Descargar Chat",
                    data=json.dumps(chat_data, indent=2, ensure_ascii=False),
                    file_name=f"rauli_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

# Funciones de utilidad
def create_rauli_prompt_templates() -> Dict[str, str]:
    """Crear plantillas de prompts especializadas para RAULI"""
    return {
        "technical_analysis": """Como experto técnico en RAULI, analiza la siguiente situación y proporciona:
1. Diagnóstico técnico preciso
2. Soluciones implementables
3. Mejores prácticas recomendadas
4. Pasos específicos de acción

Situación: {situation}""",
        
        "business_intelligence": """Como analista de business intelligence de RAULI, evalúa:
1. KPIs relevantes
2. Tendencias identificadas
3. Oportunidades de mejora
4. Recomendaciones estratégicas

Datos: {data}""",
        
        "system_optimization": """Como especialista en optimización de sistemas RAULI, propone:
1. Cuellos de botella identificados
2. Optimizaciones de rendimiento
3. Mejoras de escalabilidad
4. Configuraciones recomendadas

Sistema: {system_info}""",
        
        "code_review": """Como revisor de código senior de RAULI, analiza:
1. Calidad del código
2. Buenas prácticas aplicadas
3. Vulnerabilidades de seguridad
4. Sugerencias de mejora

Código: {code}""",
        
        "architecture_design": """Como arquitecto de soluciones RAULI, diseña:
1. Arquitectura escalable
2. Patrones recomendados
3. Tecnologías apropiadas
4. Consideraciones de deployment

Requisitos: {requirements}"""
    }

def main():
    """Función principal para testing"""
    client = RAULIOpenAIIntegration()
    
    print("🤖 RAULI OpenAI Integration Test")
    print("=" * 40)
    print(f"🔑 API Key Configured: {client.is_configured}")
    print(f"🧠 Model: {client.model}")
    
    if client.is_configured:
        # Test de conversación
        test_messages = [
            "Hola RAULI, ¿quiénes eres?",
            "¿Cuáles son tus capacidades técnicas?",
            "¿Cómo puedo optimizar mi dashboard de Streamlit?"
        ]
        
        for msg in test_messages:
            print(f"\n👤 User: {msg}")
            response = client.generate_response(msg)
            print(f"🤖 RAULI: {response[:200]}...")
    
    print(f"\n📊 Conversation Summary:")
    print(json.dumps(client.get_conversation_summary(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
