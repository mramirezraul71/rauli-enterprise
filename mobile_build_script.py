#!/usr/bin/env python3
"""
📱 RAULI MOBILE BUILD SCRIPT
Script automatizado para build cross-platform mobile
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

class RAULIMobileBuilder:
    def __init__(self):
        self.mobile_dir = Path(r'C:\RAULI_CORE\professional_tools\mobile')
        self.build_dir = self.mobile_dir / 'build'
        self.dist_dir = self.mobile_dir / 'dist'
        self.android_dir = self.mobile_dir / 'android'
        self.ios_dir = self.mobile_dir / 'ios'
        
        # Crear directorios necesarios
        for dir_path in [self.build_dir, self.dist_dir, self.android_dir, self.ios_dir]:
            dir_path.mkdir(exist_ok=True)
        
        print("📱 RAULI Mobile Builder inicializado")
    
    def check_requirements(self):
        """Verificar requisitos para build"""
        requirements = {
            'python': sys.version_info >= (3, 8),
            'buildozer': shutil.which('buildozer') is not None,
            'android_sdk': self.check_android_sdk(),
            'java': shutil.which('java') is not None,
            'main_py': (self.mobile_dir / 'main.py').exists(),
            'buildozer_spec': (self.mobile_dir / 'buildozer.spec').exists()
        }
        
        print("\n🔍 Verificación de Requisitos:")
        for req, status in requirements.items():
            icon = "✅" if status else "❌"
            print(f"   {icon} {req.replace('_', ' ').title()}: {'OK' if status else 'FALTANTE'}")
        
        return all(requirements.values())
    
    def check_android_sdk(self):
        """Verificar Android SDK"""
        android_sdk_paths = [
            os.environ.get('ANDROID_HOME'),
            os.environ.get('ANDROID_SDK_ROOT'),
            r'C:\Users\%USERNAME%\AppData\Local\Android\Sdk',
            r'C:\Android\Sdk'
        ]
        
        for path in android_sdk_paths:
            if path and os.path.exists(path):
                return True
        
        return False
    
    def setup_android_environment(self):
        """Configurar entorno Android"""
        print("\n🔧 Configurando entorno Android...")
        
        # Variables de entorno
        env_vars = {
            'ANDROID_HOME': r'C:\Users\%USERNAME%\AppData\Local\Android\Sdk',
            'ANDROID_SDK_ROOT': r'C:\Users\%USERNAME%\AppData\Local\Android\Sdk',
            'JAVA_HOME': r'C:\Program Files\Java\jdk-11'
        }
        
        for var, value in env_vars.items():
            expanded_path = os.path.expandvars(value)
            if os.path.exists(expanded_path):
                os.environ[var] = expanded_path
                print(f"   ✅ {var}: {expanded_path}")
            else:
                print(f"   ⚠️ {var}: {value} (no encontrado)")
        
        return True
    
    def create_android_manifest(self):
        """Crear Android Manifest mejorado"""
        manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.rauli.mobile">
    
    <!-- Permisos -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
    
    <!-- Características del hardware -->
    <uses-feature 
        android:name="android.hardware.camera" 
        android:required="false" />
    <uses-feature 
        android:name="android.hardware.microphone" 
        android:required="false" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:theme="@style/Theme.AppCompat.Light.NoActionBar">
            
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            
        </activity>
        
        <!-- Configuración para archivos -->
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
                
        </provider>
        
    </application>
    
</manifest>"""
        
        manifest_dir = self.android_dir / 'app' / 'src' / 'main'
        manifest_dir.mkdir(parents=True, exist_ok=True)
        
        manifest_file = manifest_dir / 'AndroidManifest.xml'
        with open(manifest_file, 'w', encoding='utf-8') as f:
            f.write(manifest_content)
        
        print(f"   ✅ Android Manifest creado: {manifest_file}")
        return manifest_file
    
    def create_gradle_build_files(self):
        """Crear archivos Gradle para Android"""
        # build.gradle (app level)
        app_build_gradle = """apply plugin: 'com.android.application'

android {
    compileSdkVersion 31
    buildToolsVersion "31.0.0"

    defaultConfig {
        applicationId "com.rauli.mobile"
        minSdkVersion 21
        targetSdkVersion 31
        versionCode 1
        versionName "1.0.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        debug {
            minifyEnabled false
            debuggable true
            applicationIdSuffix ".debug"
        }
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    packagingOptions {
        pickFirst '**/libc++_shared.so'
        pickFirst '**/libjsc.so'
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.4.2'
    implementation 'com.google.android.material:material:1.6.1'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    
    // Python para Android
    implementation 'org.python:python-android:3.9.0'
    
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.3'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'
}"""
        
        app_gradle_dir = self.android_dir / 'app'
        app_gradle_dir.mkdir(exist_ok=True)
        
        app_gradle_file = app_gradle_dir / 'build.gradle'
        with open(app_gradle_file, 'w', encoding='utf-8') as f:
            f.write(app_build_gradle)
        
        print(f"   ✅ build.gradle (app) creado: {app_gradle_file}")
        
        # build.gradle (project level)
        project_build_gradle = """buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.2'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}"""
        
        project_gradle_file = self.android_dir / 'build.gradle'
        with open(project_gradle_file, 'w', encoding='utf-8') as f:
            f.write(project_build_gradle)
        
        print(f"   ✅ build.gradle (project) creado: {project_gradle_file}")
        
        return app_gradle_file, project_gradle_file
    
    def create_app_icons(self):
        """Crear iconos de la app"""
        icons = {
            'ic_launcher.png': '🤖',  # Icono principal
            'ic_launcher_foreground.png': '👑',  # Icono foreground
            'ic_launcher_background.png': '🔷',  # Icono background
        }
        
        # Crear directorios para diferentes densidades
        densities = ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']
        
        for density in densities:
            icon_dir = self.android_dir / 'app' / 'src' / 'main' / 'res' / f'mipmap-{density}'
            icon_dir.mkdir(parents=True, exist_ok=True)
            
            # Aquí irían los archivos de iconos reales
            # Por ahora creamos placeholders
            for icon_name in icons:
                icon_file = icon_dir / icon_name
                icon_file.touch()  # Crear archivo vacío como placeholder
        
        print("   ✅ Estructura de iconos creada")
    
    def build_android_apk(self):
        """Construir APK Android"""
        print("\n🔨 Construyendo APK Android...")
        
        try:
            # Limpiar builds anteriores
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
            
            # Inicializar Buildozer
            cmd_init = ['buildozer', 'init']
            result = subprocess.run(cmd_init, cwd=self.mobile_dir, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"   ❌ Error inicializando Buildozer: {result.stderr}")
                return False
            
            # Build debug APK
            cmd_debug = ['buildozer', 'android', 'debug']
            result = subprocess.run(cmd_debug, cwd=self.mobile_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                apk_path = self.mobile_dir / 'bin' / 'raulimobile-0.1-armeabi-v7a-debug.apk'
                if apk_path.exists():
                    print(f"   ✅ APK construido exitosamente: {apk_path}")
                    return apk_path
                else:
                    print("   ⚠️ Build completado pero APK no encontrado")
                    return False
            else:
                print(f"   ❌ Error en build: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error durante build: {e}")
            return False
    
    def create_ios_project(self):
        """Crear proyecto iOS"""
        print("\n🍎 Creando proyecto iOS...")
        
        # Estructura básica de proyecto iOS
        ios_structure = {
            'RAULIMobile.xcodeproj': {},
            'RAULIMobile': {
                'Images.xcassets': {
                    'AppIcon.appiconset': {},
                    'LaunchImage.launchimage': {}
                },
                'ViewController.swift': '',
                'AppDelegate.swift': '',
                'Info.plist': ''
            }
        }
        
        def create_structure(base_path, structure):
            for name, content in structure.items():
                path = base_path / name
                if isinstance(content, dict):
                    path.mkdir(exist_ok=True)
                    create_structure(path, content)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, 'w') as f:
                        f.write(content)
        
        create_structure(self.ios_dir, ios_structure)
        print(f"   ✅ Estructura iOS creada: {self.ios_dir}")
        
        return self.ios_dir
    
    def generate_build_report(self, success: bool, apk_path=None):
        """Generar reporte de build"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'build_type': 'mobile_cross_platform',
            'success': success,
            'platforms': {
                'android': {
                    'built': apk_path is not None,
                    'apk_path': str(apk_path) if apk_path else None,
                    'file_size': os.path.getsize(apk_path) if apk_path and apk_path.exists() else 0
                },
                'ios': {
                    'project_created': self.ios_dir.exists(),
                    'project_path': str(self.ios_dir)
                }
            },
            'requirements_met': self.check_requirements(),
            'next_steps': []
        }
        
        if success:
            report['next_steps'] = [
                '📱 Instalar APK en dispositivo Android',
                '🍎 Configurar proyecto iOS en Xcode',
                '🧪 Realizar pruebas funcionales',
                '📢 Publicar en stores'
            ]
        else:
            report['next_steps'] = [
                '🔧 Corregir errores de configuración',
                '📦 Instalar dependencias faltantes',
                '🔍 Verificar requisitos del sistema',
                '🔄 Reintentar proceso de build'
            ]
        
        # Guardar reporte
        report_file = self.mobile_dir / 'build_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report_file
    
    def run_complete_build(self):
        """Ejecutar build completo"""
        print("🚀 INICIANDO BUILD COMPLETO MOBILE RAULI")
        print("=" * 50)
        
        # 1. Verificar requisitos
        if not self.check_requirements():
            print("\n❌ Requisitos no cumplidos. Por favor instala las dependencias faltantes.")
            return False
        
        # 2. Configurar entorno
        self.setup_android_environment()
        
        # 3. Crear estructura Android
        self.create_android_manifest()
        self.create_gradle_build_files()
        self.create_app_icons()
        
        # 4. Crear proyecto iOS
        self.create_ios_project()
        
        # 5. Build APK
        apk_path = self.build_android_apk()
        success = apk_path is not None
        
        # 6. Generar reporte
        report_file = self.generate_build_report(success, apk_path)
        
        print(f"\n📊 Reporte de build: {report_file}")
        
        if success:
            print(f"\n🎉 BUILD COMPLETADO EXITOSAMENTE!")
            print(f"📱 APK Android: {apk_path}")
            print(f"🍎 Proyecto iOS: {self.ios_dir}")
            print(f"📊 Reporte: {report_file}")
        else:
            print(f"\n❌ BUILD FALLIDO")
            print(f"📊 Revisa el reporte para detalles: {report_file}")
        
        return success

def main():
    """Función principal"""
    builder = RAULIMobileBuilder()
    success = builder.run_complete_build()
    
    if success:
        print(f"\n🎯 NEXT STEPS:")
        print("1. 📱 Transferir APK al dispositivo Android")
        print("2. 🔐 Habilitar instalación de fuentes desconocidas")
        print("3. 📲 Instalar y probar la app")
        print("4. 🍎 Abrir proyecto iOS en Xcode")
        print("5. 🧪 Ejecutar pruebas de integración")
        
        # Notificación de éxito
        try:
            import subprocess
            subprocess.run([
                'python', r'C:\dev\herramientas_rauli\hablar.py',
                'Build móvil completado exitosamente. APK Android generado y proyecto iOS creado.'
            ], capture_output=True)
        except:
            pass
    else:
        print(f"\n🔧 ACCIONES REQUERIDAS:")
        print("1. 📦 Instalar Android SDK")
        print("2. ☕ Instalar Java JDK")
        print("3. 🔧 Instalar Buildozer")
        print("4. 🔄 Reintentar el build")

if __name__ == "__main__":
    main()
