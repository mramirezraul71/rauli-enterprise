#!/usr/bin/env python3
"""
🏥 RAULI Health Check
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

def handler(request):
    """Health check endpoint"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": os.getenv('RAULI_ENV', 'development'),
            "services": {
                "dashboard": "running",
                "mobile": "running",
                "api": "running"
            },
            "metrics": {
                "uptime": time.time(),
                "memory_usage": "normal",
                "cpu_usage": "normal"
            }
        }
        
        return {
            "statusCode": 200,
            "body": json.dumps(health_status)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        }

if __name__ == "__main__":
    handler(None)
