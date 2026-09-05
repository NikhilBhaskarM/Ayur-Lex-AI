#!/usr/bin/env bash
# Universal self-bootstrapping runner for Ayur-Lex-AI on macOS & Linux

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "=========================================================="
echo " Ayur-Lex-AI: Indian Patent Law & Ayurvedic IPR Engine"
echo "=========================================================="
echo ""

# 1. Initialize .env if missing
if [ ! -f "$DIR/.env" ] && [ -f "$DIR/.env.example" ]; then
    echo "[*] Initializing .env configuration from template..."
    cp "$DIR/.env.example" "$DIR/.env"
fi

# 2. Setup Python virtual environment if missing
if [ ! -d "$DIR/backend/.venv" ]; then
    echo "[*] Setting up Python virtual environment (backend/.venv)..."
    python3 -m venv "$DIR/backend/.venv"
    source "$DIR/backend/.venv/bin/activate"
    echo "[*] Installing backend dependencies..."
    pip install -r "$DIR/backend/requirements.txt"
else
    source "$DIR/backend/.venv/bin/activate"
fi

# 3. Setup frontend dependencies and build if missing
if [ ! -d "$DIR/frontend/node_modules" ]; then
    echo "[*] Installing frontend dependencies (npm install)..."
    cd "$DIR/frontend" && npm install && cd "$DIR"
fi

if [ ! -f "$DIR/frontend/dist/index.html" ]; then
    echo "[*] Compiling frontend production bundle (npm run build)..."
    cd "$DIR/frontend" && npm run build && cd "$DIR"
fi

echo ""
echo "[*] Launching Unified Server on http://0.0.0.0:8000..."
cd "$DIR/backend"

# Try opening default browser in background
(sleep 2 && (which xdg-open > /dev/null && xdg-open http://localhost:8000 || which open > /dev/null && open http://localhost:8000)) &

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
