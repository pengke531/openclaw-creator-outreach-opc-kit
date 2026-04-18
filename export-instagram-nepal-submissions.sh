#!/usr/bin/env bash
set -euo pipefail

FORMAT="${1:-markdown}"
OUTPUT_PATH="${2:-}"
MARK_SUBMITTED="${3:-}"

if [ -z "$OUTPUT_PATH" ]; then
  echo "output path required"
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "python or python3 not found in PATH"
  exit 1
fi

ARGS=(
  "$(cd "$(dirname "$0")" && pwd)/workspace/scripts/instagram_ops.py"
  export-pending
  --format "$FORMAT"
  --output "$OUTPUT_PATH"
)

if [ "$MARK_SUBMITTED" = "--mark-submitted" ]; then
  ARGS+=(--mark-submitted)
fi

"$PYTHON_BIN" "${ARGS[@]}"
