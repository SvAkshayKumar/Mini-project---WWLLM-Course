@echo off
REM ==========================================================
REM   IndicWrite AI - Windows Quickstart Launcher
REM ==========================================================
echo Starting IndicWrite AI Full-Stack Environment...

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Create directories
if not exist "storage\faiss" mkdir "storage\faiss"
if not exist "storage\documents" mkdir "storage\documents"
if not exist "storage\uploads" mkdir "storage\uploads"

REM Copy .env if missing
if not exist ".env" (
    copy .env.example .env
    echo Created .env configuration file.
)

echo Starting FastAPI Backend on http://localhost:8000 ...
start "IndicWrite Backend" cmd /k "cd backend && uvicorn app.main:app --port 8000 --reload"

echo Starting Frontend on http://localhost:3000 ...
start "IndicWrite Frontend" cmd /k "npm run dev"

echo IndicWrite AI is launching! Visit http://localhost:3000 in your browser.
