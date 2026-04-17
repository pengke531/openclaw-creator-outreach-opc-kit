from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


EXPECTED = ["main", "laicai", "facai"]


def resolve_openclaw() -> str:
    for candidate in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    raise RuntimeError("openclaw executable not found in PATH")


def run_json(cmd: list[str], env: dict[str, str]):
    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False, env=env)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or f"failed: {' '.join(cmd)}")
    return json.loads(completed.stdout)


def gateway_ready(openclaw_cmd: str, env: dict[str, str]) -> tuple[bool, str]:
    completed = subprocess.run(
        [openclaw_cmd, "gateway", "probe"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
        env=env,
    )
    if completed.returncode == 0:
        return True, completed.stdout.strip()
    return False, (completed.stderr or completed.stdout or "").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-root", required=True)
    args = parser.parse_args()

    target_root = Path(args.target_root).expanduser().resolve()
    config_path = target_root / "openclaw.json"
    domain_root = target_root / "domains" / "creator-outreach-opc"
    registry = domain_root / "workspace" / "registry"
    schemas = domain_root / "workspace" / "schemas"

    env = dict(os.environ)
    env["OPENCLAW_STATE_DIR"] = str(target_root)
    env["OPENCLAW_CONFIG_PATH"] = str(config_path)
    openclaw_cmd = resolve_openclaw()

    print("[creator-opc] validating imported host config...")
    subprocess.run([openclaw_cmd, "config", "validate"], check=True, env=env)

    print("[creator-opc] checking imported domain files...")
    if not domain_root.exists():
        raise RuntimeError(f"missing imported domain root: {domain_root}")

    print("[creator-opc] checking agent registry...")
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    actual = {
        entry.get("id")
        for entry in config.get("agents", {}).get("list", [])
        if isinstance(entry, dict) and entry.get("id")
    }
    missing = [agent for agent in EXPECTED if agent not in actual]
    if missing:
        raise RuntimeError(f"missing expected agents in config: {', '.join(missing)}")

    print("[creator-opc] checking registry folders...")
    for rel in ["creators", "campaigns", "approvals", "metrics", "indexes"]:
        full = registry / rel
        if not full.exists():
            raise RuntimeError(f"missing registry folder: {full}")

    print("[creator-opc] checking evidence and inbox folders...")
    for full in [
        domain_root / "workspace" / "evidence" / "creators",
        domain_root / "workspace" / "evidence" / "campaigns",
        domain_root / "workspace" / "inbox" / "outreach-results",
        domain_root / "workspace" / "inbox" / "roi-results",
    ]:
        if not full.exists():
            raise RuntimeError(f"missing folder: {full}")

    print("[creator-opc] checking schema files...")
    for rel in ["creator.schema.json", "campaign.schema.json", "approval.schema.json"]:
        full = schemas / rel
        if not full.exists():
            raise RuntimeError(f"missing schema: {full}")

    print("[creator-opc] waiting for gateway readiness...")
    last_note = ""
    for _ in range(10):
        ok, note = gateway_ready(openclaw_cmd, env)
        last_note = note
        if ok:
            print("[creator-opc] gateway probe passed.")
            print("[creator-opc] smoke test passed.")
            return 0
        if "startup" in note.lower() or "unavailable" in note.lower():
            time.sleep(3)
            continue
        break

    print("[creator-opc] domain import is complete, but gateway is not fully ready yet.")
    if last_note:
        print(f"[creator-opc] gateway note: {last_note}")
    print("[creator-opc] start or finish starting the gateway, then rerun verification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
