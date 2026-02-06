#!/usr/bin/env python3
"""
🔄 Sincronizador de Credenciales RAULI
Mantiene actualizado credenciales.env desde la fuente principal
"""

import os
import shutil
from datetime import datetime

def sincronizar_credenciales():
    """Sincroniza credenciales desde C:\dev\credenciales.txt a C:\RAULI_CORE\credenciales.env"""
    
    origen = r"C:\dev\credenciales.txt"
    destino = r"C:\RAULI_CORE\credenciales.env"
    
    try:
        # Verificar que existe archivo origen
        if not os.path.exists(origen):
            print(f"❌ Archivo origen no encontrado: {origen}")
            return False
            
        # Leer contenido origen
        with open(origen, 'r', encoding='utf-8') as f:
            contenido_origen = f.read()
            
        # Crear backup del actual
        if os.path.exists(destino):
            backup = f"{destino}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(destino, backup)
            print(f"📋 Backup creado: {backup}")
            
        # Escribir nuevo contenido con formato RAULI
        with open(destino, 'w', encoding='utf-8') as f:
            f.write("# 🔐 CREDENCIALES RAULI-BOT - SISTEMA CENTRAL ACTUALIZADO\n")
            f.write(f"# Última sincronización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Fuente: C:\\dev\\credenciales.txt\n\n")
            f.write(contenido_origen)
            
        print(f"✅ Credenciales sincronizadas exitosamente")
        print(f"📁 Origen: {origen}")
        print(f"📁 Destino: {destino}")
        return True
        
    except Exception as e:
        print(f"❌ Error en sincronización: {e}")
        return False

if __name__ == "__main__":
    sincronizar_credenciales()
