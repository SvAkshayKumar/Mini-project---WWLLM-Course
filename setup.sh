#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "   IndicWrite AI - Automated Setup Script (CS3235)        "
echo "=========================================================="

# 1. Check Python version
python3 --version || { echo "Python 3 is required. Please install Python 3.10+."; exit 1; }

# 2. Setup Virtual Environment
if [ ! -d "backend/venv" ]; then
    echo "[1/5] Creating Python virtual environment in backend/venv..."
    python3 -m venv backend/venv
fi

echo "[2/5] Activating virtual environment..."
source backend/venv/bin/activate

# 3. Install Python dependencies
echo "[3/5] Installing Python dependencies from backend/requirements.txt..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# 4. Initialize storage directories and FAISS index
echo "[4/5] Initializing local storage and FAISS vector database..."
mkdir -p storage/faiss storage/documents storage/uploads

# 5. Copy environment file if not present
if [ ! -f ".env" ]; then
    echo "[5/5] Creating .env from .env.example..."
    cp .env.example .env
fi

echo ""
echo "=========================================================="
echo "   Setup Complete! To start the application:              "
echo "   1. Run backend:  cd backend && uvicorn app.main:app --port 8000"
echo "   2. Run frontend: npm run dev                           "
echo "=========================================================="
