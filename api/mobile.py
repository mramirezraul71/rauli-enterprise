#!/usr/bin/env python3
"""
📱 RAULI Mobile Interface - Vercel API Handler
"""

import os
import sys
import json
from pathlib import Path

# Agregar directorio actual al path
sys.path.append(str(Path(__file__).parent.parent))

def handler(request):
    """Handler principal para Vercel"""
    try:
        # Importar la interfaz móvil original
        from mobile_web_interface import app
        
        # Configurar variables de entorno
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
        
        # Ejecutar la app Flask
        return app
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

if __name__ == "__main__":
    handler(None)
