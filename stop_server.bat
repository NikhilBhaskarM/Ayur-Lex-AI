@echo off
title Stop Ayur-Lex-AI Server
echo Stopping server running on port 8000...

for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo Terminating PID %%a...
    taskkill /f /pid %%a >nul 2>&1
)

echo Ayur-Lex-AI server on port 8000 has been stopped.
pause
