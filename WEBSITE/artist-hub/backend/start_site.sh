#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/artist-hub/backend"
FRONTEND_DIR="$PROJECT_ROOT/front end"
FRONTEND_PORT=8080
BACKEND_PORT=8000

port_is_free() {
  python3 - <<'PY'
import socket, sys
port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.bind(("127.0.0.1", port))
    sock.close()
    sys.exit(0)
except OSError:
    sys.exit(1)
PY
  return $?
}

while ! port_is_free "$BACKEND_PORT"; do
  echo "Backend port $BACKEND_PORT is already in use, trying next port..."
  BACKEND_PORT=$((BACKEND_PORT + 1))
  if [ "$BACKEND_PORT" -gt 8099 ]; then
    echo "No available backend port found between 8000 and 8099."
    exit 1
  fi
done

while ! port_is_free "$FRONTEND_PORT"; do
  echo "Frontend port $FRONTEND_PORT is already in use, trying next port..."
  FRONTEND_PORT=$((FRONTEND_PORT + 1))
  if [ "$FRONTEND_PORT" -gt 8999 ]; then
    echo "No available frontend port found between 8080 and 8999."
    exit 1
  fi

done

cd "$BACKEND_DIR"
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

trap 'echo "Stopping servers..."; kill "$BACKEND_PID" 2>/dev/null || true; exit 0' INT TERM EXIT

uvicorn main:app --reload --host 0.0.0.0 --port "$BACKEND_PORT" &
BACKEND_PID=$!
echo "Backend running at http://127.0.0.1:$BACKEND_PORT/"

echo "Frontend running at http://127.0.0.1:$FRONTEND_PORT/"
cd "$FRONTEND_DIR"
python3 -m http.server "$FRONTEND_PORT"
