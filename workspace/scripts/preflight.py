from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def try_openclaw_validate(target_root: Path) -> tuple[bool, str]:
    if not command_exists("openclaw"):
        return False, "openclaw missing"
    config_path = target_root / "openclaw.json"
    if not config_path.exists():
        return True, "target config missing; validation skipped until deployment"
    try:
        env = dict(os.environ)
        env["OPENCLAW_STATE_DIR"] = str(target_root)
        env["OPENCLAW_CONFIG_PATH"] = str(config_path)
        completed = subprocess.run(
            ["openclaw", "config", "validate"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            env=env,
        )
    except Exception as exc:  # pragma: no cover
        return False, f"validate error: {exc}"
    if completed.returncode == 0:
        return True, "ok"
    stderr = (completed.stderr or completed.stdout or "").strip()
    return False, stderr or "validation failed"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--package-root", required=True)
    args = parser.parse_args()

    package_root = Path(args.package_root).resolve()
    target_root = Path(args.target_root).expanduser().resolve()

    checks = {
        "openclaw_in_path": command_exists("openclaw"),
        "python_in_path": command_exists("python") or command_exists("python3"),
        "package_root_exists": package_root.exists(),
        "target_root_parent_exists": target_root.parent.exists(),
    }

    validate_ok, validate_note = try_openclaw_validate(target_root)
    report = {
        "packageRoot": str(package_root),
        "targetRoot": str(target_root),
        "checks": checks,
        "hostConfigValidation": {
            "ok": validate_ok,
            "note": validate_note,
        },
        "recommendedRuntime": {
            "windows": "Prefer WSL2 for always-on operation.",
            "docker": "Supported if host OpenClaw is already healthy.",
        },
    }

    print("[creator-opc] preflight report")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    hard_fail = not all(
        [
            checks["openclaw_in_path"],
            checks["python_in_path"],
            checks["package_root_exists"],
            checks["target_root_parent_exists"],
        ]
    )
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
