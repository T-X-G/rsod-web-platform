@echo off
title Steel Defect Detection Platform
cd /d %~dp0

echo ========================================
echo   Starting Platform (Steel Defect P11)
echo ========================================
echo.

echo [1/3] Starting containers (PostgreSQL + Redis + MinIO)...
docker compose up -d postgres redis minio
docker compose ps

echo.
echo [2/3] Starting Backend (FastAPI + YOLO)...
start "Backend" cmd /k "cd backend && conda activate rsod-web && python -m uvicorn main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [3/3] Starting Frontend (Vue3 + Vite)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Done! Frontend: http://localhost:5173  Backend: http://localhost:8000/docs
pause
