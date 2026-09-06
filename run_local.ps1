# PowerShell script to start Ayurvedic IPR Assistant locally
$RootPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting Ayurvedic IPR & Regulatory AI Assistant" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Start Backend in separate PowerShell window
Write-Host "[1/2] Launching Backend on http://localhost:8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\backend'; if (Test-Path '.\.venv\Scripts\Activate.ps1') { & '.\.venv\Scripts\Activate.ps1' }; python -m uvicorn app.main:app --reload --port 8000"

# 2. Start Frontend in separate PowerShell window
Write-Host "[2/2] Launching Frontend on http://localhost:3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$RootPath\frontend'; npm run dev"

Write-Host "`nBoth services are starting in dedicated terminal windows!" -ForegroundColor Green
Write-Host "Web Application: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Swagger Docs: http://localhost:8000/docs" -ForegroundColor Cyan
