@echo off
title Steel Defect Detection Platform - Production Deploy
cd /d %~dp0

echo ========================================
echo   Deploying Production Environment
echo ========================================
echo.
echo Building images and starting all services...
echo This may take 5-10 minutes on first run.
echo.

docker compose up -d --build

echo.
echo ========================================
echo   All services started!
echo ========================================
echo   Frontend: http://localhost
echo   Backend API: http://localhost:8000/docs
echo   MinIO: http://localhost:9001 (minioadmin/minioadmin)
echo.
echo   Stop: docker compose down
echo ========================================
pause
