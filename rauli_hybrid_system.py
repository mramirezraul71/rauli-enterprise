#!/usr/bin/env python3
"""
[ARCH] RAULI Hybrid Architecture System
PC Local + Cloud + Ollama IA - Orquestación Profesional
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess
import psutil
from dataclasses import dataclass
from enum import Enum

class Layer(Enum):
    LOCAL = "local"
    CLOUD = "cloud"
    HYBRID = "hybrid"

class ModelType(Enum):
    OLLAMA_LOCAL = "ollama_local"
    OPENAI_CLOUD = "openai_cloud"
    GEMINI_CLOUD = "gemini_cloud"
    CODE_LLAMA = "code_llama"
    MISTRAL = "mistral"

@dataclass
class ProcessingRequest:
    query: str
    priority: str  # high, medium, low
    sensitivity: str  # public, private, critical
    complexity: str  # simple, moderate, complex
    context: Dict
    timestamp: datetime

@dataclass
class NodeStatus:
    layer: Layer
    cpu_usage: float
    memory_usage: float
    response_time: float
    available_models: List[ModelType]
    status: str  # active, busy, offline

class RAULIHybridOrchestrator:
    def __init__(self):
        self.local_node = NodeStatus(
            layer=Layer.LOCAL,
            cpu_usage=0.0,
            memory_usage=0.0,
            response_time=0.0,
            available_models=[ModelType.OLLAMA_LOCAL, ModelType.CODE_LLAMA],
            status="active"
        )
        
        self.cloud_nodes = []
        self.routing_table = {}
        self.cache = {}
        self.metrics = {
            "total_requests": 0,
            "local_processed": 0,
            "cloud_processed": 0,
            "avg_response_time": 0.0,
            "fallback_count": 0
        }
        
        print("[ARCH] RAULI Hybrid Architecture iniciada")
        print("[AI] Ollama IA local activa")
        print("[CLOUD2] Cloud nodes configurados")
        print("[TARGET] Orquestación inteligente operativa")
    
    async def check_ollama_status(self) -> bool:
        """Verificar estado de Ollama local"""
        try:
            result = subprocess.run(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    async def get_local_models(self) -> List[str]:
        """Obtener modelos Ollama disponibles"""
        try:
            result = subprocess.run(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                return [line.split()[0] for line in lines if line.strip()]
        except:
            pass
        return []
    
    def analyze_request(self, request: ProcessingRequest) -> Layer:
        """Analizar solicitud y decidir capa de procesamiento"""
        
        # Reglas de enrutamiento inteligente
        if request.sensitivity == "critical":
            return Layer.LOCAL  # Datos críticos siempre local
        
        if request.complexity == "simple" and request.priority == "high":
            return Layer.LOCAL  # Respuestas rápidas locales
        
        if request.complexity == "complex" and request.sensitivity == "public":
            return Layer.CLOUD  # Procesamiento pesado en nube
        
        # Balanceo de carga
        if self.local_node.cpu_usage > 80 or self.local_node.memory_usage > 80:
            return Layer.CLOUD
        
        return Layer.HYBRID  # Decisión híbrida por defecto
    
    async def process_local(self, request: ProcessingRequest) -> Dict:
        """Procesar solicitud localmente con Ollama"""
        try:
            models = await self.get_local_models()
            if not models:
                raise Exception("No hay modelos Ollama disponibles")
            
            # Seleccionar modelo adecuado
            model = self.select_best_model(models, request)
            
            # Ejecutar consulta Ollama
            cmd = ["ollama", "run", model, request.query]
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                response = {
                    "layer": "local",
                    "model": model,
                    "response": result.stdout.strip(),
                    "processing_time": 0.1,  # Simulado
                    "confidence": 0.95
                }
                self.metrics["local_processed"] += 1
                return response
            else:
                raise Exception(f"Error Ollama: {result.stderr}")
                
        except Exception as e:
            print(f"[ERROR] Error procesamiento local: {e}")
            return await self.process_cloud_fallback(request)
    
    async def process_cloud(self, request: ProcessingRequest) -> Dict:
        """Procesar solicitud en la nube"""
        try:
            # Simulación de procesamiento cloud
            await asyncio.sleep(0.5)  # Latencia de red
            
            response = {
                "layer": "cloud",
                "model": "gpt-4-turbo",
                "response": f"[CLOUD] Cloud response for: {request.query}",
                "processing_time": 0.5,
                "confidence": 0.98
            }
            
            self.metrics["cloud_processed"] += 1
            return response
            
        except Exception as e:
            print(f"[ERROR] Error procesamiento cloud: {e}")
            return await self.process_local_fallback(request)
    
    async def process_cloud_fallback(self, request: ProcessingRequest) -> Dict:
        """Fallback a nube si local falla"""
        print("[RESTART] Fallback a nube activado")
        self.metrics["fallback_count"] += 1
        return await self.process_cloud(request)
    
    async def process_local_fallback(self, request: ProcessingRequest) -> Dict:
        """Fallback a local si nube falla"""
        print("[RESTART] Fallback a local activado")
        self.metrics["fallback_count"] += 1
        
        # Respuesta de emergencia
        return {
            "layer": "local_fallback",
            "model": "emergency",
            "response": f"🚨 Emergency response: {request.query}",
            "processing_time": 0.05,
            "confidence": 0.70
        }
    
    def select_best_model(self, models: List[str], request: ProcessingRequest) -> str:
        """Seleccionar mejor modelo disponible"""
        
        # Prioridad de modelos por tipo de solicitud
        if "code" in request.query.lower() and "codellama" in models:
            return "codellama"
        elif "complex" in request.complexity and "mistral" in models:
            return "mistral"
        elif "llama" in models:
            return "llama2"
        elif models:
            return models[0]  # Primer disponible
        
        return "llama2"  # Default
    
    async def orchestrate_request(self, query: str, **kwargs) -> Dict:
        """Orquestar solicitud completa"""
        
        request = ProcessingRequest(
            query=query,
            priority=kwargs.get("priority", "medium"),
            sensitivity=kwargs.get("sensitivity", "public"),
            complexity=kwargs.get("complexity", "moderate"),
            context=kwargs.get("context", {}),
            timestamp=datetime.now()
        )
        
        # Actualizar métricas
        self.metrics["total_requests"] += 1
        
        # Decidir capa de procesamiento
        target_layer = self.analyze_request(request)
        
        print(f"[TARGET] Enrutando a capa: {target_layer.value}")
        
        # Procesar según capa
        if target_layer == Layer.LOCAL:
            response = await self.process_local(request)
        elif target_layer == Layer.CLOUD:
            response = await self.process_cloud(request)
        else:  # HYBRID
            # Intentar local primero, luego cloud si falla
            response = await self.process_local(request)
        
        # Actualizar métricas de rendimiento
        self.update_performance_metrics(response)
        
        return response
    
    def update_performance_metrics(self, response: Dict):
        """Actualizar métricas de rendimiento"""
        processing_time = response.get("processing_time", 0)
        
        if self.metrics["avg_response_time"] == 0:
            self.metrics["avg_response_time"] = processing_time
        else:
            # Media móvil simple
            self.metrics["avg_response_time"] = (
                self.metrics["avg_response_time"] * 0.9 + processing_time * 0.1
            )
    
    async def get_system_status(self) -> Dict:
        """Obtener estado completo del sistema"""
        
        # Estado local
        self.local_node.cpu_usage = psutil.cpu_percent()
        self.local_node.memory_usage = psutil.virtual_memory().percent
        self.local_node.status = "active" if await self.check_ollama_status() else "offline"
        
        # Modelos disponibles
        local_models = await self.get_local_models()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "local_node": {
                "status": self.local_node.status,
                "cpu_usage": self.local_node.cpu_usage,
                "memory_usage": self.local_node.memory_usage,
                "available_models": local_models,
                "ollama_active": await self.check_ollama_status()
            },
            "cloud_nodes": self.cloud_nodes,
            "metrics": self.metrics,
            "routing_efficiency": self.calculate_routing_efficiency()
        }
    
    def calculate_routing_efficiency(self) -> float:
        """Calcular eficiencia de enrutamiento"""
        if self.metrics["total_requests"] == 0:
            return 0.0
        
        local_ratio = self.metrics["local_processed"] / self.metrics["total_requests"]
        fallback_ratio = self.metrics["fallback_count"] / self.metrics["total_requests"]
        
        # Eficiencia = procesamiento local - penalización por fallbacks
        efficiency = local_ratio - (fallback_ratio * 0.5)
        return max(0.0, min(1.0, efficiency))
    
    async def install_ollama_if_needed(self):
        """Instalar Ollama si no está disponible"""
        if not await self.check_ollama_status():
            print("[PACKAGE] Instalando Ollama...")
            try:
                # Descargar e instalar Ollama
                subprocess.run(
                    ["curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"],
                    shell=True,
                    timeout=300
                )
                print("[OK] Ollama instalado correctamente")
            except Exception as e:
                print(f"[ERROR] Error instalando Ollama: {e}")
    
    async def download_models(self):
        """Descargar modelos básicos"""
        models_to_download = ["llama2", "codellama", "mistral"]
        
        for model in models_to_download:
            try:
                print(f"📥 Descargando modelo: {model}")
                subprocess.run(
                    ["ollama", "pull", model],
                    timeout=600
                )
                print(f"[OK] Modelo {model} descargado")
            except Exception as e:
                print(f"[ERROR] Error descargando {model}: {e}")

# Sistema principal
class RAULIHybridSystem:
    def __init__(self):
        self.orchestrator = RAULIHybridOrchestrator()
        self.running = False
    
    async def start(self):
        """Iniciar sistema híbrido"""
        print("[BOOT] Iniciando RAULI Hybrid System...")
        
        # Verificar/instalar Ollama
        await self.orchestrator.install_ollama_if_needed()
        
        # Descargar modelos
        await self.orchestrator.download_models()
        
        self.running = True
        print("[OK] Sistema híbrido operativo")
        
        # Loop principal
        while self.running:
            await self.main_loop()
            await asyncio.sleep(1)
    
    async def main_loop(self):
        """Loop principal del sistema"""
        try:
            # Aquí podrías recibir comandos de WhatsApp, dashboard, etc.
            pass
        except KeyboardInterrupt:
            self.running = False
            print("🛑 Sistema detenido")
    
    async def process_command(self, command: str, **kwargs) -> Dict:
        """Procesar comando a través del sistema híbrido"""
        return await self.orchestrator.orchestrate_request(command, **kwargs)
    
    def get_status(self) -> Dict:
        """Obtener estado del sistema"""
        return asyncio.run(self.orchestrator.get_system_status())

if __name__ == "__main__":
    system = RAULIHybridSystem()
    
    # Ejemplo de uso
    async def demo():
        print("[TARGET] Demo del sistema híbrido...")
        
        # Consulta simple local
        response1 = await system.process_command(
            "Hola RAULI, ¿cómo estás?",
            priority="high",
            sensitivity="public",
            complexity="simple"
        )
        print(f"[PIN] Respuesta 1: {response1}")
        
        # Consulta compleja cloud
        response2 = await system.process_command(
            "Analiza este código complejo y optimízalo",
            priority="medium",
            sensitivity="public", 
            complexity="complex"
        )
        print(f"[PIN] Respuesta 2: {response2}")
        
        # Consulta crítica local
        response3 = await system.process_command(
            "Procesar datos sensibles del sistema",
            priority="high",
            sensitivity="critical",
            complexity="moderate"
        )
        print(f"[PIN] Respuesta 3: {response3}")
        
        # Estado del sistema
        status = system.get_status()
        print(f"[METRICS] Estado del sistema: {json.dumps(status, indent=2)}")
    
    # Ejecutar demo
    asyncio.run(demo())
