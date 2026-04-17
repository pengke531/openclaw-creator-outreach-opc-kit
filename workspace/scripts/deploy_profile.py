from __future__ import annotations

import argparse
import json
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path


def rewrite(value, domain_root: Path, target_root: Path):
    if isinstance(value, str):
        return (
            value.replace("__DOMAIN_ROOT__", str(domain_root).replace("\\", "/"))
            .replace("__PROFILE_ROOT__", str(target_root).replace("\\", "/"))
        )
    if isinstance(value, list):
        return [rewrite(v, domain_root, target_root) for v in value]
    if isinstance(value, dict):
        return {k: rewrite(v, domain_root, target_root) for k, v in value.items()}
    return value


def deep_fill(dst, src):
    if isinstance(dst, dict) and isinstance(src, dict):
        for k, v in src.items():
            if k not in dst:
                dst[k] = deepcopy(v)
            else:
                dst[k] = deep_fill(dst[k], v)
        return dst
    return dst


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--package-root", required=True)
    args = parser.parse_args()

    package_root = Path(args.package_root).resolve()
    target_root = Path(args.target_root).expanduser().resolve()
    domain_root = target_root / "domains" / "creator-outreach-opc"
    config_path = target_root / "openclaw.json"
    backup_path = target_root / f"openclaw.json.creator-outreach-backup.{datetime.now():%Y%m%d-%H%M%S}.bak"

    target_root.mkdir(parents=True, exist_ok=True)
    domain_root.mkdir(parents=True, exist_ok=True)

    for rel in ["agents", "workspace"]:
        src = package_root / rel
        dst = domain_root / rel
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    shutil.copy2(package_root / ".env.template", domain_root / ".env.template")

    overlay = json.loads((package_root / "openclaw.json").read_text(encoding="utf-8"))
    overlay = rewrite(overlay, domain_root, target_root)

    if config_path.exists():
        current = json.loads(config_path.read_text(encoding="utf-8-sig"))
        backup_path.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        current = {}

    skills = current.setdefault("skills", {})
    skills_load = skills.setdefault("load", {})
    skills_load.setdefault("extraDirs", [])
    for d in overlay.get("skills", {}).get("load", {}).get("extraDirs", []):
        if d not in skills_load["extraDirs"]:
            skills_load["extraDirs"].append(d)

    agents = current.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    for k, v in overlay.get("agents", {}).get("defaults", {}).items():
        if k == "workspace":
            continue
        if k not in defaults:
            defaults[k] = deepcopy(v)
        elif isinstance(v, dict) and isinstance(defaults[k], dict):
            defaults[k] = deep_fill(defaults[k], v)

    agents.setdefault("list", [])
    by_id = {a.get("id"): a for a in agents["list"] if isinstance(a, dict)}
    for overlay_agent in overlay.get("agents", {}).get("list", []):
        by_id[overlay_agent["id"]] = deepcopy(overlay_agent)
    agents["list"] = list(by_id.values())

    main_agent = next((a for a in agents["list"] if a.get("id") == "main"), None)
    if main_agent:
        sub = main_agent.setdefault("subagents", {})
        allow = sub.setdefault("allowAgents", [])
        for agent_id in ["wangcai", "laicai", "facai"]:
            if agent_id not in allow:
                allow.append(agent_id)

    config_path.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[creator-opc] overlay imported into {domain_root}")
    if backup_path.exists():
        print(f"[creator-opc] backup created: {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
