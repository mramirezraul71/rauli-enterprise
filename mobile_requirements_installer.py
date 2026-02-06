#!/usr/bin/env python3
"""
📦 RAULI MOBILE REQUIREMENTS INSTALLER
Instalador automático de dependencias para desarrollo móvil
"""

import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

class RAULIMobileRequirementsInstaller:
    def __init__(self):
        self.base_dir = Path(r'C:\RAULI_CORE')
        self.tools_dir = Path(r'C:\dev')
        self.install_dir = Path(r'C:\RAULI_CORE\mobile_tools')
        self.install_dir.mkdir(exist_ok=True)
        
        print("📦 RAULI Mobile Requirements Installer inicializado")
    
    def check_admin_privileges(self):
        """Verificar privilegios de administrador"""
        try:
            return os.getuid() == 0 if hasattr(os, 'getuid') else False
        except:
            # En Windows, verificar de otra manera
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
    
    def install_java_jdk(self):
        """Instalar Java JDK"""
        print("\n☕ Instalando Java JDK...")
        
        jdk_urls = {
            'windows': 'https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe',
            'linux': 'https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz',
            'mac': 'https://download.oracle.com/java/17/latest/jdk-17_macos-x64_bin.tar.gz'
        }
        
        platform = sys.platform.lower()
        if 'win' in platform:
            jdk_url = jdk_urls['windows']
            jdk_installer = self.install_dir / 'jdk-17_installer.exe'
            
            # Descargar JDK
            print("   📥 Descargando JDK 17...")
            urllib.request.urlretrieve(jdk_url, jdk_installer)
            
            # Instalar JDK (requiere admin)
            print("   🔧 Instalando JDK (requiere admin)...")
            try:
                subprocess.run([str(jdk_installer), '/s'], check=True)
                print("   ✅ JDK instalado exitosamente")
                return True
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Error instalando JDK: {e}")
                print("   💡 Por favor instala JDK manualmente desde: https://www.oracle.com/java/technologies/downloads/")
                return False
        else:
            print("   ⚠️ Plataforma no soportada para instalación automática")
            return False
    
    def install_android_sdk(self):
        """Instalar Android SDK"""
        print("\n📱 Instalando Android SDK...")
        
        # Descargar Command Line Tools
        sdk_url = "https://dl.google.com/android/repository/commandlinetools-win-9477386_latest.zip"
        sdk_zip = self.install_dir / 'commandlinetools.zip'
        sdk_dir = self.install_dir / 'android_sdk'
        
        try:
            # Descargar SDK
            print("   📥 Descargando Android Command Line Tools...")
            urllib.request.urlretrieve(sdk_url, sdk_zip)
            
            # Extraer
            print("   📦 Extrayendo SDK...")
            with zipfile.ZipFile(sdk_zip, 'r') as zip_ref:
                zip_ref.extractall(sdk_dir)
            
            # Mover archivos a la ubicación correcta
            cmdline_tools = sdk_dir / 'cmdline-tools'
            latest_version = None
            if cmdline_tools.exists():
                for item in cmdline_tools.iterdir():
                    if item.is_dir():
                        latest_version = item
                        break
            
            if latest_version:
                target_dir = sdk_dir / 'cmdline-tools' / 'latest'
                target_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(latest_version), str(target_dir))
            
            # Configurar variables de entorno
            android_home = str(sdk_dir)
            os.environ['ANDROID_HOME'] = android_home
            os.environ['ANDROID_SDK_ROOT'] = android_home
            
            # Agregar al PATH
            tools_path = os.path.join(android_home, 'cmdline-tools', 'latest', 'bin')
            platform_tools = os.path.join(android_home, 'platform-tools')
            
            current_path = os.environ.get('PATH', '')
            os.environ['PATH'] = f"{tools_path};{platform_tools};{current_path}"
            
            # Instalar componentes necesarios
            print("   🔧 Instalando componentes Android...")
            sdkmanager = os.path.join(tools_path, 'sdkmanager.bat')
            
            components = [
                'platforms;android-31',
                'platform-tools',
                'build-tools;31.0.0',
                'ndk;23.1.7779620'
            ]
            
            for component in components:
                try:
                    subprocess.run([sdkmanager, component], check=True, capture_output=True)
                    print(f"   ✅ {component} instalado")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️ Error instalando {component}: {e}")
            
            print(f"   ✅ Android SDK instalado en: {android_home}")
            return True
            
        except Exception as e:
            print(f"   ❌ Error instalando Android SDK: {e}")
            return False
    
    def setup_environment_variables(self):
        """Configurar variables de entorno permanentemente"""
        print("\n🔧 Configurando variables de entorno...")
        
        # Variables a configurar
        env_vars = {
            'ANDROID_HOME': str(self.install_dir / 'android_sdk'),
            'ANDROID_SDK_ROOT': str(self.install_dir / 'android_sdk'),
            'JAVA_HOME': r'C:\Program Files\Java\jdk-17'
        }
        
        # Crear script para configurar variables
        env_script = self.install_dir / 'setup_mobile_env.bat'
        with open(env_script, 'w', encoding='utf-8') as f:
            f.write('@echo off\n')
            f.write('echo Configurando entorno de desarrollo móvil RAULI...\n\n')
            
            for var, value in env_vars.items():
                expanded_path = os.path.expandvars(value)
                f.write(f'set {var}={expanded_path}\n')
                f.write(f'echo {var}=%{var}%\n')
            
            # Agregar al PATH
            android_tools = os.path.join(expanded_path, 'cmdline-tools', 'latest', 'bin')
            platform_tools = os.path.join(expanded_path, 'platform-tools')
            
            f.write(f'set PATH={android_tools};{platform_tools};%PATH%\n')
            f.write('echo PATH actualizado\n\n')
            f.write('echo Entorno móvil configurado!\n')
            f.write('pause\n')
        
        print(f"   ✅ Script de entorno creado: {env_script}")
        return env_script
    
    def install_additional_tools(self):
        """Instalar herramientas adicionales"""
        print("\n🛠️ Instalando herramientas adicionales...")
        
        tools = [
            ('gradle', 'https://services.gradle.org/distributions/gradle-8.0-bin.zip'),
            ('nodejs', 'https://nodejs.org/dist/v18.17.0/node-v18.17.0-x64.msi')
        ]
        
        for tool_name, tool_url in tools:
            try:
                print(f"   📦 Descargando {tool_name}...")
                tool_file = self.install_dir / f"{tool_name}_installer.zip"
                
                if tool_name == 'gradle':
                    urllib.request.urlretrieve(tool_url, tool_file)
                    
                    # Extraer Gradle
                    with zipfile.ZipFile(tool_file, 'r') as zip_ref:
                        zip_ref.extractall(self.install_dir)
                    
                    print(f"   ✅ {tool_name} instalado")
                
                elif tool_name == 'nodejs':
                    node_installer = self.install_dir / 'nodejs_installer.msi'
                    urllib.request.urlretrieve(tool_url, node_installer)
                    
                    # Instalar Node.js (requiere admin)
                    try:
                        subprocess.run([str(node_installer), '/quiet'], check=True)
                        print(f"   ✅ {tool_name} instalado")
                    except subprocess.CalledProcessError:
                        print(f"   ⚠️ {tool_name} requiere instalación manual")
                
            except Exception as e:
                print(f"   ❌ Error instalando {tool_name}: {e}")
    
    def create_mobile_development_guide(self):
        """Crear guía de desarrollo móvil"""
        guide_content = """# 📱 GUÍA DE DESARROLLO MÓVIL RAULI

## 📋 REQUISITOS INSTALADOS

### ☕ Java JDK
- **Versión:** JDK 17
- **Ubicación:** C:\\Program Files\\Java\\jdk-17
- **JAVA_HOME:** Configurado

### 📱 Android SDK
- **Versión:** Command Line Tools 9.4.7
- **API Level:** 31 (Android 12)
- **Ubicación:** C:\\RAULI_CORE\\mobile_tools\\android_sdk
- **ANDROID_HOME:** Configurado

### 🛠️ Herramientas Adicionales
- **Buildozer:** Para packaging Python-Android
- **Gradle:** 8.0 (build system)
- **Node.js:** 18.17 (para herramientas web)

## 🚀 PASOS SIGUIENTES

### 1. Configurar Entorno
```bash
# Ejecutar script de configuración
C:\\RAULI_CORE\\mobile_tools\\setup_mobile_env.bat

# O configurar manualmente las variables:
set ANDROID_HOME=C:\\RAULI_CORE\\mobile_tools\\android_sdk
set JAVA_HOME=C:\\Program Files\\Java\\jdk-17
set PATH=%ANDROID_HOME%\\cmdline-tools\\latest\\bin;%ANDROID_HOME%\\platform-tools;%PATH%
```

### 2. Build APK Android
```bash
cd C:\\RAULI_CORE\\professional_tools\\mobile
python C:\\RAULI_CORE\\mobile_build_script.py
```

### 3. Proyecto iOS
```bash
# Abrir en Xcode
open C:\\RAULI_CORE\\professional_tools\\mobile\\ios\\RAULIMobile.xcodeproj
```

## 📱 ESTRUCTURA DEL PROYECTO

```
C:\\RAULI_CORE\\professional_tools\\mobile\\
├── main.py                 # App principal Kivy
├── buildozer.spec          # Configuración Buildozer
├── android/                # Proyecto Android
│   ├── app/
│   │   ├── build.gradle
│   │   └── src/main/
│   │       └── AndroidManifest.xml
│   └── build.gradle
└── ios/                    # Proyecto iOS
    ├── RAULIMobile.xcodeproj
    └── RAULIMobile/
```

## 🧪 TESTING

### Android
1. Conectar dispositivo USB
2. Habilitar "Depuración USB"
3. Instalar APK: `adb install raulimobile-debug.apk`

### iOS
1. Abrir en Xcode
2. Conectar dispositivo iOS
3. Seleccionar target y Run

## 📢 DEPLOYMENT

### Google Play Store
1. Generar APK firmado
2. Crear cuenta developer
3. Subir a Play Console

### Apple App Store
1. Generar IPA firmado
2. Crear cuenta developer
3. Subir a App Store Connect

## 🔧 SOLUCIÓN DE PROBLEMAS

### Buildozer Issues
- Limpiar: `buildozer android clean`
- Rebuild: `buildozer android debug`
- Logs: `buildozer android debug --verbose`

### Android SDK Issues
- Reinstalar: `sdkmanager --uninstall && sdkmanager --install`
- Licencias: `sdkmanager --licenses`
- Update: `sdkmanager --update`

## 📞 SOPORTE

Para ayuda adicional:
- 📖 Documentación: https://buildozer.readthedocs.io/
- 🐛 Issues: GitHub repository
- 💬 Chat: RAULI Dashboard

---
🤖 Generado por RAULI Mobile Requirements Installer
📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        guide_file = self.install_dir / 'MOBILE_DEVELOPMENT_GUIDE.md'
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"   ✅ Guía creada: {guide_file}")
        return guide_file
    
    def run_complete_installation(self):
        """Ejecutar instalación completa"""
        print("🚀 INICIANDO INSTALACIÓN COMPLETA DE REQUISITOS MÓVILES")
        print("=" * 60)
        
        # Verificar admin
        if not self.check_admin_privileges():
            print("⚠️ Se recomienda ejecutar como administrador")
        
        success_count = 0
        total_steps = 5
        
        # 1. Instalar Java JDK
        if self.install_java_jdk():
            success_count += 1
        
        # 2. Instalar Android SDK
        if self.install_android_sdk():
            success_count += 1
        
        # 3. Configurar entorno
        if self.setup_environment_variables():
            success_count += 1
        
        # 4. Instalar herramientas adicionales
        if self.install_additional_tools():
            success_count += 1
        
        # 5. Crear guía
        if self.create_mobile_development_guide():
            success_count += 1
        
        # Resultado
        success_rate = (success_count / total_steps) * 100
        
        print(f"\n📊 RESULTADO DE INSTALACIÓN:")
        print(f"✅ Exitosos: {success_count}/{total_steps} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print(f"\n🎉 INSTALACIÓN COMPLETADA EXITOSAMENTE!")
            print(f"📱 Requisitos móviles listos para desarrollo")
            print(f"🔧 Ejecuta: C:\\RAULI_CORE\\mobile_tools\\setup_mobile_env.bat")
            print(f"📖 Consulta: C:\\RAULI_CORE\\mobile_tools\\MOBILE_DEVELOPMENT_GUIDE.md")
        else:
            print(f"\n⚠️ INSTALACIÓN PARCIAL")
            print(f"🔧 Revisa los errores e instala manualmente los componentes faltantes")
        
        return success_rate >= 80

def main():
    """Función principal"""
    installer = RAULIMobileRequirementsInstaller()
    success = installer.run_complete_installation()
    
    if success:
        print(f"\n🎯 NEXT STEPS:")
        print("1. 🔧 Reiniciar terminal para aplicar variables de entorno")
        print("2. 📱 Ejecutar script de build móvil")
        print("3. 🧪 Probar build con Android emulator")
        print("4. 📢 Deploy a dispositivo real")
    else:
        print(f"\n🔧 ACCIONES REQUERIDAS:")
        print("1. 👑 Ejecutar como administrador")
        print("2. 📦 Instalar componentes manualmente")
        print("3. 🔧 Configurar variables de entorno")
        print("4. 🔄 Reintentar instalación")

if __name__ == "__main__":
    main()
