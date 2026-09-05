#!/usr/bin/env bash
# Shell script to start Ayur-Lex-AI Unified Server on macOS and Linux

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "=========================================================="
echo " Starting Ayur-Lex-AI: Indian Patent Law & Ayurvedic Engine"
echo "=========================================================="

# Build frontend if dist does not exist
if [ ! -f "$DIR/frontend/dist/index.html" ]; then
    echo "[*] Compiling frontend production bundle..."
    cd "$DIR/frontend" && npm run build && cd "$DIR"
fi

echo "[*] Launching Unified Server on http://localhost:8000..."
cd "$DIR/backend"
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python3 -m uvicorn app.main:app --port 8000 --reload
