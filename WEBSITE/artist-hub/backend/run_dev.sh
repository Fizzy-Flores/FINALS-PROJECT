#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
uvicorn main:app --reload --host 0.0.0.0 --port 8000
