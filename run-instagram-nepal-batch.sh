#!/usr/bin/env bash
set -euo pipefail

AGENT="${1:-main}"
BATCH_SIZE="${2:-24}"
MICRO_BATCH_SIZE="${3:-8}"
THINKING="${4:-medium}"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "python or python3 not found in PATH"
  exit 1
fi

"$PYTHON_BIN" "$(cd "$(dirname "$0")" && pwd)/workspace/scripts/instagram_ops.py" manual-run --agent "$AGENT" --batch-size "$BATCH_SIZE" --micro-batch-size "$MICRO_BATCH_SIZE" --thinking "$THINKING"
