#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-$HOME/.openclaw}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[creator-opc] python or python3 not found in PATH"
  exit 1
fi

"$PYTHON_BIN" "$SCRIPT_DIR/workspace/scripts/preflight.py" --target-root "$TARGET_ROOT" --package-root "$SCRIPT_DIR"
"$SCRIPT_DIR/workspace/scripts/smoke-test.sh"
