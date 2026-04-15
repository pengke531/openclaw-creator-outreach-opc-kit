#!/usr/bin/env bash
set -euo pipefail

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[creator-opc] python or python3 not found in PATH"
  exit 1
fi

"$PYTHON_BIN" "$(cd "$(dirname "$0")" && pwd)/smoke_test.py"
