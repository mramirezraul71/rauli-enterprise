#!/usr/bin/env python3
"""
🌐 RAULI Dashboard Simple Server
"""

import http.server
import socketserver
import os
from pathlib import Path

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dist", **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    port = 4173
    dashboard_dir = Path("C:/dev/RAULI-VISION/dashboard")
    
    if not dashboard_dir.exists():
        print("❌ Directorio del dashboard no encontrado")
        return
    
    # Cambiar al directorio del dashboard
    os.chdir(dashboard_dir)
    
    if not Path("dist").exists():
        print("❌ Build no encontrado - Ejecuta 'npm run build' primero")
        return
    
    print(f"🌐 Iniciando servidor en http://localhost:{port}")
    print("📱 Dashboard RAULI disponible")
    print("🛑 Presiona Ctrl+C para detener")
    
    with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido")

if __name__ == "__main__":
    main()
