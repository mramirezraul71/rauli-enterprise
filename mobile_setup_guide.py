#!/usr/bin/env python3
"""
📱 RAULI MOBILE SETUP GUIDE
Guía paso a paso para configurar desarrollo móvil
"""

import os
from pathlib import Path
from datetime import datetime

def create_mobile_setup_guide():
    """Crear guía completa de setup móvil"""
    
    guide_content = """# 📱 GUÍA COMPLETA DE SETUP MÓVIL RAULI

## 🎯 OBJETIVO
Configurar entorno completo para desarrollo cross-platform de la app móvil RAULI

## 📋 REQUISITOS PREVIOS

### 💻 Sistema Operativo
- ✅ Windows 10/11 (recomendado)
- ✅ macOS 10.15+ (para iOS)
- ✅ Linux Ubuntu 18.04+ (alternativa)

### 🔐 Privilegios
- 👑 Acceso como Administrador
- 💾 Espacio en disco: 10GB libres
- 🌐 Conexión a internet estable

---

## ☕ PASO 1: INSTALAR JAVA JDK

### Opción A: Descarga Manual (Recomendado)
1. 📥 Visitar: https://www.oracle.com/java/technologies/downloads/
2. 🔽 Descargar: **JDK 17** (Windows x64 Installer)
3. 📁 Ejecutar el instalador
4. ✅ Seguir instrucciones del instalador

### Opción B: Via Package Manager
```bash
# Windows (Chocolatey)
choco install openjdk --version=17

# macOS (Homebrew)
brew install openjdk@17

# Linux (Ubuntu)
sudo apt update
sudo apt install openjdk-17-jdk
```

### 🔧 Verificar Instalación
```bash
java -version
javac -version
```

**Resultado esperado:** `java version "17.x.x"`

---

## 📱 PASO 2: INSTALAR ANDROID SDK

### Opción A: Android Studio (Recomendado)
1. 📥 Descargar: https://developer.android.com/studio
2. 📁 Instalar Android Studio
3. 🛠️ En Android Studio:
   - Tools → SDK Manager
   - Instalar: **Android 12 (API 31)**
   - Instalar: **Android SDK Build-Tools 31.0.0**
   - Instalar: **Android SDK Command-line Tools**
   - Instalar: **Android NDK (Side by side)**

### Opción B: Command Line Tools Only
1. 📥 Descargar: https://developer.android.com/studio#command-tools
2. 📦 Extraer en: `C:\\Android\\Sdk`
3. 🔧 Configurar variables de entorno

### 🔧 Variables de Entorno
```bash
# Windows (System Properties → Environment Variables)
ANDROID_HOME=C:\\Users\\[USERNAME]\\AppData\\Local\\Android\\Sdk
ANDROID_SDK_ROOT=C:\\Users\\[USERNAME]\\AppData\\Local\\Android\\Sdk
JAVA_HOME=C:\\Program Files\\Java\\jdk-17

# Agregar al PATH:
%ANDROID_HOME%\\cmdline-tools\\latest\\bin
%ANDROID_HOME%\\platform-tools
%ANDROID_HOME%\\build-tools\\31.0.0
```

### ✅ Verificar Instalación
```bash
adb version
sdkmanager --list
```

---

## 🐍 PASO 3: INSTALAR PYTHON Y BUILD REQUIREMENTS

### Python (ya debería estar instalado)
```bash
python --version  # Debe ser 3.8+
pip --version
```

### Buildozer
```bash
pip install buildozer
pip install kivy kivymd
pip install plyer pyjnius
```

### Verificar Buildozer
```bash
buildozer --version
```

---

## 📱 PASO 4: CONFIGURAR PROYECTO RAULI MOBILE

### Estructura del Proyecto
```
C:\\RAULI_CORE\\professional_tools\\mobile\\
├── main.py                 # App Kivy principal
├── buildozer.spec          # Configuración Buildozer
├── assets/                 # Recursos (iconos, imágenes)
└── bin/                    # Builds generados
```

### Configurar buildozer.spec
Asegurar que `buildozer.spec` contenga:

```ini
[app]
title = RAULI Mobile Assistant
package.name = rauli_mobile
package.domain = com.rauli.mobile
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

[android]
requirements = python3,kivy,kivymd,requests,opencv-python,numpy,pandas
android.api = 31
android.minapi = 21
android.ndk = 23b
android.permissions = CAMERA, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, INTERNET
```

---

## 🔨 PASO 5: BUILD ANDROID APK

### Preparar Entorno
```bash
cd C:\\RAULI_CORE\\professional_tools\\mobile
```

### Limpiar Build Anterior
```bash
buildozer android clean
```

### Build Debug APK
```bash
buildozer android debug
```

### Build Release APK
```bash
buildozer android release
```

### 📍 Ubicación del APK
```
C:\\RAULI_CORE\\professional_tools\\mobile\\bin\\
├── raulimobile-0.1-armeabi-v7a-debug.apk
└── raulimobile-0.1-armeabi-v7a-release.apk
```

---

## 🍎 PASO 6: CONFIGURAR iOS (Opcional)

### Requisitos iOS
- 🍎 macOS con Xcode 14+
- 📱 Cuenta Apple Developer
- 🔐 Certificado de desarrollo

### Crear Proyecto iOS
```bash
# En macOS
cd C:\\RAULI_CORE\\professional_tools\\mobile
buildozer ios debug
```

### Abrir en Xcode
```
C:\\RAULI_CORE\\professional_tools\\mobile\\ios\\
└── RAULIMobile.xcodeproj
```

---

## 🧪 PASO 7: TESTING Y DEPLOYMENT

### Testing en Android
1. 📱 Conectar dispositivo vía USB
2. 🔓 Habilitar "Depuración USB"
3. 📲 Instalar APK:
   ```bash
   adb install bin/raulimobile-0.1-armeabi-v7a-debug.apk
   ```

### Testing en Emulador
1. 📱 Crear AVD (Android Virtual Device)
2. 🚀 Iniciar emulador
3. 📦 Instalar APK:
   ```bash
   adb install bin/raulimobile-0.1-armeabi-v7a-debug.apk
   ```

### Deployment
- **Google Play:** Subir release APK a Play Console
- **App Store:** Subir IPA a App Store Connect
- **Direct Distribution:** Compartir APK directamente

---

## 🔧 SOLUCIÓN DE PROBLEMAS COMUNES

### Buildozer Issues
```bash
# Limpiar cache
buildozer android clean

# Verbose mode para debugging
buildozer android debug --verbose

# Reinstalar dependencias
pip install --upgrade buildozer kivy kivymd
```

### Android SDK Issues
```bash
# Aceptar licencias
sdkmanager --licenses

# Update SDK
sdkmanager --update

# Reinstalar componentes
sdkmanager --uninstall "platforms;android-31"
sdkmanager --install "platforms;android-31"
```

### Java Issues
```bash
# Verificar JAVA_HOME
echo %JAVA_HOME%

# Verificar PATH
where java
where javac
```

### Permision Issues (Android)
```bash
# En buildozer.spec, agregar permisos:
android.permissions = CAMERA, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE, INTERNET, VIBRATE
```

---

## 📊 CHECKLIST FINAL

### ✅ Verificación Final
- [ ] Java JDK 17 instalado
- [ ] Android SDK configurado
- [ ] Variables de entorno establecidas
- [ ] Buildozer instalado
- [ ] Proyecto configurado
- [ ] APK generado exitosamente
- [ ] App probada en dispositivo/emulador

### 🎯 Resultado Esperado
- 📱 APK funcional en Android
- 🍎 Proyecto iOS listo para Xcode
- 🔧 Entorno de desarrollo configurado
- 📦 Pipeline de build automatizado

---

## 📞 SOPORTE Y RECURSOS

### Documentación Oficial
- 📖 Buildozer: https://buildozer.readthedocs.io/
- 📱 Kivy: https://kivy.org/doc/stable/
- 🎨 KivyMD: https://kivymd.readthedocs.io/

### Comunidad
- 💬 Discord Kivy: https://discord.gg/kivy
- 🐛 Issues: GitHub repository
- 📧 Soporte: RAULI Dashboard

### Tutoriales
- 🎥 Kivy Mobile Development: YouTube
- 📚 Buildozer Tutorial: Medium
- 🔧 Android Setup: Developer Guides

---

## 🚀 NEXT STEPS

### Inmediato
1. 🧪 Probar APK en dispositivo real
2. 📱 Configurar permisos correctamente
3. 🔧 Optimizar rendimiento

### Mediano Plazo
1. 📢 Publicar en stores
2. 🔄 Implementar CI/CD para mobile
3. 📊 Agregar analytics y crash reporting

### Largo Plazo
1. 🌐 Expandir a más plataformas
2. 🤖 Integrar con backend RAULI
3. 📈 Escalabilidad y optimización

---

🤖 **Generado por RAULI Mobile Setup Guide**
📅 **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**
👑 **Sistema Enterprise Ready**

---

## 📝 NOTAS IMPORTANTES

### ⚠️ Consideraciones
- El setup móvil requiere tiempo y paciencia
- Algunos pasos pueden variar según el sistema
- Se recomienda seguir el orden establecido

### 💡 Tips Adicionales
- 🔄 Reiniciar terminal después de configurar variables
- 📱 Usar dispositivo real para testing final
- 🔐 Mantener secure las credenciales y API keys

### 🎯 Éxito
Una vez completado este setup, tendrás un entorno completo para:
- ✅ Desarrollar apps móviles con Python
- ✅ Build APKs para Android
- ✅ Crear proyectos para iOS
- ✅ Deploy en app stores

**¡RAULI Mobile estará listo para conquistar el mundo móvil! 🚀📱**
"""
    
    # Crear directorio para guías
    guides_dir = Path(r'C:\RAULI_CORE\mobile_guides')
    guides_dir.mkdir(exist_ok=True)
    
    # Guardar guía
    guide_file = guides_dir / 'COMPLETE_MOBILE_SETUP_GUIDE.md'
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    return guide_file

def create_quick_setup_script():
    """Crear script rápido de setup"""
    
    script_content = """@echo off
echo ====================================
echo 🚀 RAULI MOBILE QUICK SETUP
echo ====================================
echo.

echo 🔍 Verificando requisitos...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Por favor instala Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python encontrado

echo.
echo 📦 Instalando dependencias Python...
pip install buildozer kivy kivymd plyer pyjnius

echo.
echo 🔧 Configurando variables de entorno...
setx ANDROID_HOME "%USERPROFILE%\\AppData\\Local\\Android\\Sdk"
setx ANDROID_SDK_ROOT "%USERPROFILE%\\AppData\\Local\\Android\\Sdk"
setx JAVA_HOME "C:\\Program Files\\Java\\jdk-17"

echo.
echo 📱 Verificando Android SDK...
if exist "%USERPROFILE%\\AppData\\Local\\Android\\Sdk" (
    echo ✅ Android SDK encontrado
) else (
    echo ⚠️ Android SDK no encontrado
    echo Por favor instala Android Studio desde:
    echo https://developer.android.com/studio
    echo.
    echo Luego ejecuta este script nuevamente.
)

echo.
echo 🎯 Setup completado!
echo.
echo NEXT STEPS:
echo 1. Reinicia tu terminal
echo 2. Navega al proyecto: cd C:\\RAULI_CORE\\professional_tools\\mobile
echo 3. Build APK: buildozer android debug
echo.
echo 📖 Para ayuda completa consulta:
echo C:\\RAULI_CORE\\mobile_guides\\COMPLETE_MOBILE_SETUP_GUIDE.md
echo.
pause
"""
    
    script_file = Path(r'C:\RAULI_CORE\mobile_guides\quick_setup.bat')
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return script_file

def main():
    """Función principal"""
    print("📱 CREANDO GUÍAS DE SETUP MÓVIL RAULI")
    print("=" * 50)
    
    # Crear guía completa
    guide_file = create_mobile_setup_guide()
    print(f"✅ Guía completa creada: {guide_file}")
    
    # Crear script rápido
    script_file = create_quick_setup_script()
    print(f"✅ Script rápido creado: {script_file}")
    
    print(f"\n🎯 MOBILE SETUP READY!")
    print(f"📖 Guía completa: {guide_file}")
    print(f"🚀 Script rápido: {script_file}")
    print(f"\n📱 Sigue los pasos de la guía para configurar tu entorno móvil")
    print(f"🔧 Ejecuta el script rápido para setup básico")

if __name__ == "__main__":
    main()
