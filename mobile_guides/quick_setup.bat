@echo off
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
setx ANDROID_HOME "%USERPROFILE%\AppData\Local\Android\Sdk"
setx ANDROID_SDK_ROOT "%USERPROFILE%\AppData\Local\Android\Sdk"
setx JAVA_HOME "C:\Program Files\Java\jdk-17"

echo.
echo 📱 Verificando Android SDK...
if exist "%USERPROFILE%\AppData\Local\Android\Sdk" (
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
echo 2. Navega al proyecto: cd C:\RAULI_CORE\professional_tools\mobile
echo 3. Build APK: buildozer android debug
echo.
echo 📖 Para ayuda completa consulta:
echo C:\RAULI_CORE\mobile_guides\COMPLETE_MOBILE_SETUP_GUIDE.md
echo.
pause
