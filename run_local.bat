@echo off
setlocal enabledelayedexpansion
title Ayur-Lex-AI Unified Server Launcher
echo ==========================================================
echo   Ayur-Lex-AI: Indian Patent Law & Ayurvedic IPR Engine
echo ==========================================================
echo.

cd /d "%~dp0"

:: 1. Auto-create .env if missing
if not exist ".env" (
    if exist ".env.example" (
        echo [*] Initializing .env configuration from template...
        copy .env.example .env >nul
    )
)

:: 2. Auto-setup Python virtualenv if missing
if not exist "backend\.venv\Scripts\python.exe" (
    echo [*] Python virtual environment not found. Setting up backend\.venv...
    python -m venv backend\.venv
    if errorlevel 1 (
        echo [!] ERROR: Python is required to run Ayur-Lex-AI. Please install Python 3.10+.
        pause
        exit /b 1
    )
    echo [*] Installing backend dependencies (one-time setup)...
    backend\.venv\Scripts\pip install -r backend\requirements.txt
)

:: 3. Auto-setup frontend node_modules & build if missing
if not exist "frontend\node_modules" (
    echo [*] Frontend dependencies not found. Running npm install...
    cd frontend
    call npm install
    cd ..
)

if not exist "frontend\dist\index.html" (
    echo [*] Frontend production bundle not found. Building static assets...
    cd frontend
    call npm run build
    cd ..
)

echo.
echo [*] Launching Unified Origin Server (FastAPI + React SPA)...
echo.

:: Launch server with 0.0.0.0 so other laptops on the same Wi-Fi can connect
start "Ayur-Lex-AI Unified Server" cmd /k "cd /d "%~dp0backend" && call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: Give server 2 seconds to initialize then open browser
timeout /t 2 /nobreak >nul
start http://localhost:8000/

echo ==========================================================
echo   Ayur-Lex-AI is LIVE!
echo   
echo   This Laptop:     http://localhost:8000/
echo   Other Laptops:   http://%COMPUTERNAME%:8000/
echo   API Docs:        http://localhost:8000/docs
echo ==========================================================
pause
