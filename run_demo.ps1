# AgriVision 1-Click PowerShell Demo Launcher
Write-Host "=======================================================" -ForegroundColor Green
Write-Host "  AgriVision AI (TAH-015) - 1-Click Platform Launcher" -ForegroundColor Green
Write-Host "=======================================================" -ForegroundColor Green

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "[1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Launching React 19 Frontend on http://localhost:5173 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\frontend'; npm run dev"

Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"

Write-Host "=======================================================" -ForegroundColor Green
Write-Host "  AgriVision is now running!" -ForegroundColor Green
Write-Host "  Web App : http://localhost:5173" -ForegroundColor Cyan
Write-Host "  Swagger : http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Green
