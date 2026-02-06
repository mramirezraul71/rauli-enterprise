#!/usr/bin/env python3
"""
🚀 RAULI Dashboard - Vercel API Handler
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
        # Importar el dashboard original
        from dashboard_rauli import main
        
        # Configurar variables de entorno
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
        
        # Ejecutar el dashboard
        return main()
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

if __name__ == "__main__":
    handler(None)
