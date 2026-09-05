@echo off
title Ayur-Lex-AI Unified Server Launcher
echo ==========================================================
echo   Starting Ayur-Lex-AI: Indian Patent Law Engine
echo ==========================================================
echo.

:: Check if frontend/dist exists, if not build it
if not exist "%~dp0frontend\dist\index.html" (
    echo [*] Frontend production build not found. Building now...
    cd /d "%~dp0frontend"
    call npm run build
    cd /d "%~dp0"
)

echo [*] Launching Unified Origin Server (FastAPI + React SPA)...
start "Ayur-Lex-AI Unified Server" cmd /k "cd /d %~dp0backend && (if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat) && python -m uvicorn app.main:app --port 8000 --reload"

echo.
echo ==========================================================
echo   Ayur-Lex-AI is running independently!
echo   Web Application:  http://localhost:8000/
echo   Legal Chamber:    http://localhost:8000/chamber
echo   API Docs:         http://localhost:8000/docs
echo ==========================================================
pause
