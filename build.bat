@echo off
title Building Steel Defect Detection Platform
cd /d %~dp0

echo ========================================
echo   Building Production Artifacts
echo ========================================
echo.

echo [1/3] Building Backend Docker Image...
docker build -t rsod-backend:latest ./backend
if %errorlevel% neq 0 (
    echo ERROR: Backend build failed
    exit /b 1
)
echo.

echo [2/3] Building Frontend Docker Image...
docker build -t rsod-frontend:latest ./frontend
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed
    exit /b 1
)
echo.

echo [3/3] Build Complete!
echo.
echo Run: docker compose up -d
echo Frontend: http://localhost
echo Backend:  http://localhost:8000/docs
echo.
pause
