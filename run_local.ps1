# PowerShell script to start Ayur-Lex-AI Unified Server
$RootPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Ayur-Lex-AI: Indian Patent Law & Ayurvedic Engine" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verify frontend build
$DistPath = Join-Path $RootPath "frontend\dist\index.html"
if (-not (Test-Path $DistPath)) {
    Write-Host "[*] Frontend build not found. Compiling production bundle..." -ForegroundColor Yellow
    Push-Location (Join-Path $RootPath "frontend")
    npm run build
    Pop-Location
}

# 2. Start Unified Server on Port 8000
Write-Host "[*] Launching Unified Server (FastAPI + React SPA) on http://localhost:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\backend'; if (Test-Path '.\.venv\Scripts\Activate.ps1') { & '.\.venv\Scripts\Activate.ps1' }; python -m uvicorn app.main:app --reload --port 8000"

Write-Host "`nAyur-Lex-AI Unified Server is active!" -ForegroundColor Green
Write-Host "Web Application:  http://localhost:8000/" -ForegroundColor Cyan
Write-Host "Legal Chamber:    http://localhost:8000/chamber" -ForegroundColor Cyan
Write-Host "API Swagger Docs: http://localhost:8000/docs" -ForegroundColor Cyan
