from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_INDEX_PATH = ROOT / "registry" / "indexes" / "instagram-nepal-index.json"
RUNTIME_STATE_PATH = ROOT / "registry" / "indexes" / "instagram-nepal-runtime-state.json"
RUNTIME_LOG_PATH = ROOT / "inbox" / "outreach-results" / "instagram-nepal-runtime-log.jsonl"
DOMAIN_ENV_PATH = ROOT.parent / ".env"


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def isoformat(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def load_dotenv(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def resolve_openclaw() -> str:
    for candidate in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    raise RuntimeError("openclaw executable not found in PATH")


def load_runtime_state() -> dict[str, Any]:
    return read_json(
        RUNTIME_STATE_PATH,
        {
            "trigger_command": "/workking",
            "status": "idle",
            "provider_cursor": 0,
            "provider_order": [],
            "started_at": None,
            "last_cycle_started_at": None,
            "last_cycle_finished_at": None,
            "last_unique_qualified_at": None,
            "last_stop_reason": None,
            "last_provider": None,
            "total_cycles": 0,
            "total_new_unique": 0,
            "updated_at": isoformat(utc_now()),
        },
    )


def save_runtime_state(state: dict[str, Any]) -> None:
    state["updated_at"] = isoformat(utc_now())
    write_json(RUNTIME_STATE_PATH, state)


def load_provider_order(env: dict[str, str]) -> list[str]:
    raw = env.get(
        "INSTAGRAM_PROVIDER_ORDER",
        "agent-reach,autoglm-browser-agent,search,apify,brightdata",
    )
    providers = [item.strip() for item in raw.split(",") if item.strip()]
    return providers or ["agent-reach", "search", "apify"]


def unique_registered_count() -> int:
    index = read_json(REGISTRY_INDEX_PATH, {"records": {}})
    records = index.get("records", {})
    canonical_ids = {
        str(entry.get("canonical_id", "")).strip()
        for entry in records.values()
        if isinstance(entry, dict) and str(entry.get("canonical_id", "")).strip()
    }
    return len(canonical_ids)


def build_cycle_message(*, provider_order: list[str], batch_size: int, micro_batch_size: int) -> str:
    preferred = provider_order[0]
    fallback = ", ".join(provider_order[1:]) if len(provider_order) > 1 else "none"
    return (
        "The /workking runtime has started one Instagram Nepal discovery cycle. "
        "Use the instagram-nepal-creator-pipeline skill. "
        "Before any search work, read workspace/registry/indexes/instagram-nepal-index.json "
        "and ignore every handle or profile URL already recorded there so duplicates are skipped up front. "
        f"Preferred provider for this cycle: {preferred}. "
        f"Fallback order if the preferred provider is unavailable, rate-limited, or unstable: {fallback}. "
        f"Logical batch size is {batch_size} with micro-batches of {micro_batch_size}. "
        "This cycle is Instagram only, Nepal only, personal creators only, followers must be >= 100000, "
        "and evidence gaps must not enter the registry. "
        "Persist each newly qualified creator immediately through workspace/scripts/instagram_registry_ops.py. "
        "As soon as this cycle has persisted at least one new unique qualified creator, wrap the cycle up promptly "
        "so the runtime can relaunch the next cycle automatically. "
        "Use record-review for screened-fail, evidence-gap, or duplicate cases. "
        "Keep the cycle within 15 minutes. "
        "Do not produce a chat delivery list. Update only registry, evidence, and pending submissions."
    )


def run_cycle(*, agent: str, thinking: str, timeout_seconds: int, message: str) -> dict[str, Any]:
    cmd = [
        resolve_openclaw(),
        "agent",
        "--agent",
        agent,
        "--message",
        message,
        "--thinking",
        thinking,
        "--json",
    ]
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
        payload = {
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
        if payload["stdout"]:
            try:
                payload["json"] = json.loads(payload["stdout"])
            except json.JSONDecodeError:
                payload["json"] = None
        return payload
    except subprocess.TimeoutExpired:
        return {
            "returncode": 124,
            "stdout": "",
            "stderr": f"cycle exceeded timeout of {timeout_seconds} seconds",
            "timed_out": True,
        }


def summarize_state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "trigger_command": state.get("trigger_command"),
        "status": state.get("status"),
        "provider_order": state.get("provider_order", []),
        "provider_cursor": state.get("provider_cursor", 0),
        "last_provider": state.get("last_provider"),
        "started_at": state.get("started_at"),
        "last_cycle_started_at": state.get("last_cycle_started_at"),
        "last_cycle_finished_at": state.get("last_cycle_finished_at"),
        "last_unique_qualified_at": state.get("last_unique_qualified_at"),
        "last_stop_reason": state.get("last_stop_reason"),
        "total_cycles": state.get("total_cycles", 0),
        "total_new_unique": state.get("total_new_unique", 0),
    }


def start_runtime(*, agent: str, thinking: str, batch_size: int, micro_batch_size: int) -> dict[str, Any]:
    domain_env = load_dotenv(DOMAIN_ENV_PATH)
    merged_env = {**domain_env, **os.environ}
    provider_order = load_provider_order(merged_env)
    single_cycle_timeout_seconds = int(merged_env.get("INSTAGRAM_SINGLE_CYCLE_TIMEOUT_SECONDS", "900"))
    idle_stop_minutes = int(merged_env.get("INSTAGRAM_IDLE_STOP_MINUTES", "30"))
    cycle_pause_seconds = int(merged_env.get("INSTAGRAM_CYCLE_PAUSE_SECONDS", "2"))

    state = load_runtime_state()
    cursor = int(state.get("provider_cursor", 0))
    started_at = utc_now()
    state["status"] = "running"
    state["started_at"] = isoformat(started_at)
    state["provider_order"] = provider_order
    state["last_stop_reason"] = None
    state["last_unique_qualified_at"] = isoformat(started_at)
    save_runtime_state(state)

    cycles: list[dict[str, Any]] = []

    while True:
        current_state = load_runtime_state()
        if current_state.get("status") == "stopped" and current_state.get("last_stop_reason") == "stopped manually":
            return {
                "ok": True,
                "status": "stopped",
                "stop_reason": "stopped manually",
                "cycles": cycles,
                "state": summarize_state(current_state),
            }

        active_order = provider_order[cursor % len(provider_order):] + provider_order[: cursor % len(provider_order)]
        cycle_provider = active_order[0]
        state["provider_cursor"] = (cursor + 1) % len(provider_order)
        state["last_provider"] = cycle_provider
        state["last_cycle_started_at"] = isoformat(utc_now())
        state["total_cycles"] = int(state.get("total_cycles", 0)) + 1
        save_runtime_state(state)

        before_count = unique_registered_count()
        cycle_result = run_cycle(
            agent=agent,
            thinking=thinking,
            timeout_seconds=single_cycle_timeout_seconds,
            message=build_cycle_message(
                provider_order=active_order,
                batch_size=batch_size,
                micro_batch_size=micro_batch_size,
            ),
        )
        after_count = unique_registered_count()
        new_unique = max(after_count - before_count, 0)
        finished_at = utc_now()

        state["last_cycle_finished_at"] = isoformat(finished_at)
        if new_unique > 0:
            state["last_unique_qualified_at"] = isoformat(finished_at)
            state["total_new_unique"] = int(state.get("total_new_unique", 0)) + new_unique
        save_runtime_state(state)

        log_entry = {
            "started_at": state.get("last_cycle_started_at"),
            "finished_at": state.get("last_cycle_finished_at"),
            "provider": cycle_provider,
            "new_unique": new_unique,
            "timed_out": bool(cycle_result.get("timed_out")),
            "returncode": cycle_result.get("returncode"),
            "stderr": cycle_result.get("stderr", ""),
        }
        append_jsonl(RUNTIME_LOG_PATH, log_entry)
        cycles.append(log_entry)

        last_unique = parse_iso(state.get("last_unique_qualified_at")) or started_at
        idle_for = finished_at - last_unique
        if new_unique == 0 and idle_for >= timedelta(minutes=idle_stop_minutes):
            state["status"] = "stopped"
            state["last_stop_reason"] = (
                f"no new unique qualified creator for {idle_stop_minutes} minutes"
            )
            save_runtime_state(state)
            return {
                "ok": True,
                "status": "stopped",
                "stop_reason": state["last_stop_reason"],
                "cycles": cycles,
                "state": summarize_state(state),
            }

        cursor = state["provider_cursor"]
        if cycle_pause_seconds > 0:
            time.sleep(cycle_pause_seconds)


def stop_runtime() -> dict[str, Any]:
    state = load_runtime_state()
    state["status"] = "stopped"
    state["last_stop_reason"] = "stopped manually"
    save_runtime_state(state)
    return {"ok": True, "state": summarize_state(state)}


def status_runtime() -> dict[str, Any]:
    state = load_runtime_state()
    return {"ok": True, "state": summarize_state(state)}


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start")
    start.add_argument("--agent", default="main")
    start.add_argument("--thinking", default="medium")
    start.add_argument("--batch-size", type=int, default=int(os.environ.get("INSTAGRAM_BATCH_SIZE", "24")))
    start.add_argument("--micro-batch-size", type=int, default=int(os.environ.get("INSTAGRAM_MICRO_BATCH_SIZE", "8")))

    subparsers.add_parser("status")
    subparsers.add_parser("stop")

    args = parser.parse_args()

    try:
        if args.command == "start":
            result = start_runtime(
                agent=args.agent,
                thinking=args.thinking,
                batch_size=args.batch_size,
                micro_batch_size=args.micro_batch_size,
            )
        elif args.command == "stop":
            result = stop_runtime()
        else:
            result = status_runtime()
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
