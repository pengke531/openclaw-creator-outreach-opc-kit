from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


EXPECTED = ["creator_manager", "creator_scout", "creator_connector", "creator_analyst"]


def run_json(cmd: list[str]):
    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or f"failed: {' '.join(cmd)}")
    return json.loads(completed.stdout)


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    registry = root / "workspace" / "registry"
    schemas = root / "workspace" / "schemas"

    print("[creator-opc] validating host config...")
    subprocess.run(["openclaw", "config", "validate"], check=True)

    print("[creator-opc] checking agent registry...")
    agents = run_json(["openclaw", "agents", "list", "--json"])
    actual = {entry["id"] for entry in agents}
    missing = [agent for agent in EXPECTED if agent not in actual]
    if missing:
        raise RuntimeError(f"missing expected agents: {', '.join(missing)}")

    print("[creator-opc] checking registry folders...")
    for rel in ["creators", "campaigns", "approvals", "metrics"]:
        full = registry / rel
        if not full.exists():
            raise RuntimeError(f"missing registry folder: {full}")

    print("[creator-opc] checking schema files...")
    for rel in ["creator.schema.json", "campaign.schema.json", "approval.schema.json"]:
        full = schemas / rel
        if not full.exists():
            raise RuntimeError(f"missing schema: {full}")

    print("[creator-opc] probing gateway...")
    subprocess.run(["openclaw", "gateway", "probe"], check=True)

    print("[creator-opc] smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
