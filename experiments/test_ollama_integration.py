#!/usr/bin/env python3
"""
🧠 Test Ollama Integration - RAULI Hybrid System
"""

import subprocess
import asyncio
from datetime import datetime

async def test_ollama_integration():
    """Probar integración con Ollama"""
    
    print("🧠 Probando integración Ollama con RAULI...")
    
    # Lista de modelos disponibles
    try:
        result = subprocess.run(
            ["ollama", "list"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Ollama conectado correctamente")
            print("📋 Modelos disponibles:")
            print(result.stdout)
        else:
            print("❌ Error conectando con Ollama")
            return
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Probar modelo llama2
    print("\n🎯 Probando modelo LLaMA2...")
    try:
        cmd = ["ollama", "run", "llama2", "Hola RAULI, ¿cómo estás?"]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("✅ LLaMA2 respondió:")
            print(result.stdout)
        else:
            print(f"❌ Error LLaMA2: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error ejecutando LLaMA2: {e}")
    
    # Probar modelo CodeLlama
    print("\n💻 Probando modelo CodeLlama...")
    try:
        cmd = ["ollama", "run", "codellama", "Escribe una función Python para sumar dos números"]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("✅ CodeLlama respondió:")
            print(result.stdout)
        else:
            print(f"❌ Error CodeLlama: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error ejecutando CodeLlama: {e}")
    
    print("\n🎉 Prueba completada")

if __name__ == "__main__":
    asyncio.run(test_ollama_integration())
