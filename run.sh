#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/src"

PORT=8000

if [ "$1" == "--stop" ]; then
    pkill -f "uvicorn api:app"
    exit 0
fi

python -m uvicorn api:app --host 0.0.0.0 --port ${PORT}
