@echo off
setlocal
cd /d "%~dp0"

:: Check if port 8000 is already active
netstat -ano | find ":8000" | find "LISTENING" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    start http://localhost:8000/
    exit /b
)

:: Start the server in background if not already running
start "" /b "%~dp0backend\.venv\Scripts\python.exe" -m uvicorn app.main:app --app-dir "%~dp0backend" --host 0.0.0.0 --port 8000

:: Poll until port 8000 is ready
set count=0
:wait_loop
timeout /t 1 /nobreak >nul
netstat -ano | find ":8000" | find "LISTENING" >nul 2>&1
if %ERRORLEVEL% equ 0 goto ready
set /a count+=1
if %count% geq 10 goto ready
goto wait_loop

:ready
start http://localhost:8000/
exit /b
