@echo off
title AgriVision AI Platform Launcher
echo =======================================================
echo   AgriVision AI (TAH-015) - Precision Agriculture
echo =======================================================
echo.
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "AgriVision Backend" cmd /k "cd /d "%~dp0backend" && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting React Frontend on http://localhost:5173 ...
start "AgriVision Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

timeout /t 3 /nobreak >nul
echo.
echo [+] Opening web application in browser...
start http://localhost:5173

echo.
echo =======================================================
echo   AgriVision is LIVE!
echo   Frontend : http://localhost:5173
echo   Backend  : http://127.0.0.1:8000
echo   API Docs : http://127.0.0.1:8000/docs
echo =======================================================
