@echo off
title Ayurvedic IPR Assistant Launcher
echo ==========================================================
echo   Starting Ayurvedic IPR & Regulatory AI Assistant
echo ==========================================================
echo.
echo [1/2] Starting Backend (FastAPI on http://localhost:8000)...
start "Ayurvedic IPR - Backend Server" cmd /k "cd /d %~dp0backend && (if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat) && python -m uvicorn app.main:app --reload --port 8000"

echo [2/2] Starting Frontend (React on http://localhost:3000)...
start "Ayurvedic IPR - Frontend UI" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ==========================================================
echo   Both services started in separate windows!
echo   Web Application:  http://localhost:3000
echo   Interactive Docs: http://localhost:8000/docs
echo ==========================================================
pause
