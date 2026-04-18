#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-$HOME/.openclaw}"
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "[creator-opc] repo root:   $REPO_ROOT"
echo "[creator-opc] host target: $TARGET_ROOT"

if ! command -v openclaw >/dev/null 2>&1; then
  echo "[creator-opc] openclaw not found in PATH"
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "[creator-opc] python or python3 not found in PATH"
  exit 1
fi

cd "$REPO_ROOT"

for rel in \
  "agents/laicai/AGENTS.md" \
  "agents/facai/AGENTS.md" \
  "workspace/AGENTS.md" \
  "workspace/MEMORY.md"
do
  if [ ! -f "$REPO_ROOT/$rel" ]; then
    echo "[creator-opc] missing required file: $REPO_ROOT/$rel"
    exit 1
  fi
done

"$PYTHON_BIN" "./workspace/scripts/preflight.py" --target-root "$TARGET_ROOT" --package-root "$REPO_ROOT"
if [ -d "$HOME/.agents/skills" ]; then
  mkdir -p "$REPO_ROOT/workspace/skills/shared"
  for skill in search tavily agent-reach autoglm-browser-agent web-scraping clawdefender-1 notion gog
  do
    if [ -d "$HOME/.agents/skills/$skill" ]; then
      rm -rf "$REPO_ROOT/workspace/skills/shared/$skill"
      cp -R "$HOME/.agents/skills/$skill" "$REPO_ROOT/workspace/skills/shared/$skill"
    fi
  done
fi
"$PYTHON_BIN" "./workspace/scripts/deploy_profile.py" --target-root "$TARGET_ROOT" --package-root "$REPO_ROOT"

DOMAIN_ROOT="$TARGET_ROOT/domains/creator-outreach-opc"
if [ -f "$DOMAIN_ROOT/.env.template" ] && [ ! -f "$DOMAIN_ROOT/.env" ]; then
  cp "$DOMAIN_ROOT/.env.template" "$DOMAIN_ROOT/.env"
  echo "[creator-opc] created optional template file: $DOMAIN_ROOT/.env"
fi

openclaw config validate

GATEWAY_OK=0
if PROBE_JSON="$(openclaw gateway probe --json 2>/dev/null)"; then
  echo "$PROBE_JSON"
  if "$PYTHON_BIN" -c 'import json,sys; data=json.loads(sys.stdin.read() or "{}"); targets=data.get("targets", []); sys.exit(0 if any(t.get("connect", {}).get("ok") for t in targets if isinstance(t, dict)) else 1)' <<<"$PROBE_JSON"; then
    GATEWAY_OK=1
  fi
fi

if [ "$GATEWAY_OK" -eq 1 ]; then
  ./workspace/scripts/smoke-test.sh
  if [ -z "${OPENCLAW_SKIP_DOMAIN_CRON:-}" ]; then
    ./install-instagram-nepal-cron.sh
  fi
else
  echo "[creator-opc] gateway probe skipped or failed; import still completed."
fi

cat <<EOF

[creator-opc] import complete.
[creator-opc] next:
  1. Review optional integration template: $DOMAIN_ROOT/.env
EOF

if [ "$GATEWAY_OK" -eq 1 ]; then
  cat <<EOF
  2. Domain import and smoke test already passed.
  3. Re-run verification any time: ./verify-creator-outreach.sh
EOF
else
  cat <<EOF
  2. Start OpenClaw normally: openclaw gateway
  3. Verify the domain: ./verify-creator-outreach.sh
  4. Install recurring Instagram cron after the gateway is healthy: ./install-instagram-nepal-cron.sh
EOF
fi
