#!/usr/bin/env python3
"""
🔑 CONFIGURADOR DE TOKEN TELEGRAM - RAULI-BOT
"""

import os
from pathlib import Path

def configurar_token():
    print("🔑 CONFIGURADOR DE TOKEN TELEGRAM")
    print("=" * 40)
    print("1. Abre Telegram y busca @BotFather")
    print("2. Envía: /newbot")
    print("3. Nombre: RAULI Pro Bot")
    print("4. Username: rauli_pro_bot")
    print("5. Copia el token que te da BotFather")
    print("=" * 40)
    
    token = input("\n🔑 Pega tu token de Telegram aquí: ").strip()
    
    if not token:
        print("❌ No ingresaste token")
        return
    
    # Leer archivo de credenciales
    cred_file = Path(r"C:\RAULI_CORE\credenciales.env")
    
    if not cred_file.exists():
        print("❌ Archivo de credenciales no encontrado")
        return
    
    with open(cred_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Reemplazar línea del token
    for i, line in enumerate(lines):
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            lines[i] = f'TELEGRAM_BOT_TOKEN={token}\n'
            break
    
    # Guardar archivo
    with open(cred_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ Token configurado: {token[:10]}...")
    print("🚀 Ahora ejecuta: python C:\\RAULI_CORE\\telegram_rauli_bot_pro.py")

if __name__ == "__main__":
    configurar_token()
