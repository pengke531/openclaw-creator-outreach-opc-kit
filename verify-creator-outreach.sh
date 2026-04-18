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

for path in \
  "$SCRIPT_DIR/workspace/scripts/instagram_ops.py" \
  "$SCRIPT_DIR/workspace/scripts/instagram_registry_ops.py" \
  "$SCRIPT_DIR/workspace/skills/shared/instagram-nepal-creator-pipeline/SKILL.md" \
  "$SCRIPT_DIR/install-instagram-nepal-cron.sh" \
  "$SCRIPT_DIR/run-instagram-nepal-batch.sh" \
  "$SCRIPT_DIR/export-instagram-nepal-submissions.sh"
do
  if [ ! -f "$path" ]; then
    echo "[creator-opc] missing required Instagram Nepal runtime file: $path"
    exit 1
  fi
done
