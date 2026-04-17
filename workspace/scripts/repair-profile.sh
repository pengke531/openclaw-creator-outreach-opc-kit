#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-$HOME/.openclaw}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[creator-opc] python or python3 not found in PATH"
  exit 1
fi

for rel in \
  "agents/laicai/AGENTS.md" \
  "agents/facai/AGENTS.md" \
  "workspace/AGENTS.md" \
  "workspace/MEMORY.md"
do
  if [ ! -f "$ROOT/$rel" ]; then
    echo "[creator-opc] missing required file: $ROOT/$rel"
    exit 1
  fi
done

"$PYTHON_BIN" "$SCRIPT_DIR/preflight.py" --target-root "$TARGET_ROOT" --package-root "$ROOT"
"$PYTHON_BIN" "$SCRIPT_DIR/deploy_profile.py" --target-root "$TARGET_ROOT" --package-root "$ROOT"
openclaw config validate
echo "[creator-opc] repair complete."
