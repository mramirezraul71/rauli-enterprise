# 🤖 CASCADE AUTHORIZATION SCRIPT - POWERSHELL
Write-Host "🤖 Iniciando autorización de Cascade como Arquitecto Técnico de RAULI..." -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\RAULI_CORE"

try {
    python cascade_authorization.py
    Write-Host "✅ Cascade autorizado y configurado como Arquitecto Técnico Principal" -ForegroundColor Green
    Write-Host "🎯 Listo para ejecutar implementaciones enterprise" -ForegroundColor Green
    Write-Host "🚀 RAULI Enterprise - Cascade Integration Complete" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en autorización: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Presione Enter para continuar"
