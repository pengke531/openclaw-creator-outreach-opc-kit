from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "registry" / "indexes" / "instagram-nepal-index.json"
PENDING_SUBMISSIONS_PATH = ROOT / "inbox" / "outreach-results" / "instagram-nepal-pending-submissions.json"
RUNTIME_SCRIPT_PATH = ROOT / "scripts" / "instagram_runtime.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_openclaw() -> str:
    for candidate in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    raise RuntimeError("openclaw executable not found in PATH")


def run_command(cmd: list[str], *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)


def require_ok(completed: subprocess.CompletedProcess[str], action: str) -> None:
    if completed.returncode != 0:
        raise RuntimeError(f"{action} failed: {(completed.stderr or completed.stdout).strip()}")


def build_batch_message(batch_size: int, micro_batch_size: int) -> str:
    return (
        "Run one Instagram Nepal creator discovery cycle now. "
        "Use the instagram-nepal-creator-pipeline skill. "
        f"Target {batch_size} candidates total in micro-batches of {micro_batch_size}. "
        "Only Instagram. Keep hard gates strict: Nepal only, personal creator only, followers >= 100000, "
        "evidence gaps must stay out of registry. "
        "Delegate profile discovery and verification to wangcai. "
        "After each verified candidate, use exec to run workspace/scripts/instagram_registry_ops.py with a payload file "
        "so qualified creators are registered, duplicates only update followers and updated_at, and unqualified or evidence-gap records stay out of formal registry. "
        "Do not deliver an external report. Update only workspace/evidence, workspace/registry, and workspace/inbox pending submissions."
    )


def build_workking_message() -> str:
    return (
        "Invoke the workking skill now. "
        "Treat it as /workking start. "
        "Start the Instagram Nepal runtime and return only the runtime status summary."
    )


def agent_turn(*, agent: str, message: str, thinking: str) -> dict[str, Any]:
    openclaw_cmd = resolve_openclaw()
    completed = run_command(
        [openclaw_cmd, "agent", "--agent", agent, "--message", message, "--thinking", thinking, "--json"]
    )
    require_ok(completed, "openclaw agent")
    stdout = completed.stdout.strip()
    return json.loads(stdout) if stdout else {"ok": True}


def parse_cron_list(raw: str) -> list[dict[str, Any]]:
    data = json.loads(raw)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("jobs"), list):
            return [item for item in data["jobs"] if isinstance(item, dict)]
        if isinstance(data.get("items"), list):
            return [item for item in data["items"] if isinstance(item, dict)]
    return []


def install_cron(*, every: str, agent: str, job_name: str, batch_size: int, micro_batch_size: int) -> dict[str, Any]:
    openclaw_cmd = resolve_openclaw()
    list_cmd = run_command([openclaw_cmd, "cron", "list", "--json"])
    if list_cmd.returncode == 0 and list_cmd.stdout.strip():
        for job in parse_cron_list(list_cmd.stdout):
            if job.get("name") == job_name and job.get("id"):
                rm = run_command([openclaw_cmd, "cron", "remove", str(job["id"])])
                require_ok(rm, f"remove existing cron job {job_name}")

    message = build_workking_message()
    add = run_command(
        [
            openclaw_cmd,
            "cron",
            "add",
            "--name",
            job_name,
            "--every",
            every,
            "--session",
            "isolated",
            "--agent",
            agent,
            "--message",
            message,
            "--no-deliver",
        ]
    )
    require_ok(add, "openclaw cron add")
    return {"ok": True, "job_name": job_name, "schedule": every, "agent": agent}


def start_runtime(*, agent: str, batch_size: int, micro_batch_size: int, thinking: str) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(RUNTIME_SCRIPT_PATH),
        "start",
        "--agent",
        agent,
        "--batch-size",
        str(batch_size),
        "--micro-batch-size",
        str(micro_batch_size),
        "--thinking",
        thinking,
    ]
    completed = run_command(cmd, env=os.environ.copy())
    require_ok(completed, "instagram runtime start")
    stdout = completed.stdout.strip()
    return json.loads(stdout) if stdout else {"ok": True}


def export_pending(*, output: Path, fmt: str, mark_submitted: bool) -> dict[str, Any]:
    pending = read_json(PENDING_SUBMISSIONS_PATH, {"items": []})
    items = list(pending.get("items", []))
    output.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "json":
        write_json(output, items)
    elif fmt == "csv":
        with output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["creator_name", "profile_url", "followers"])
            writer.writeheader()
            for item in items:
                writer.writerow(
                    {
                        "creator_name": item.get("creator_name", ""),
                        "profile_url": item.get("profile_url", ""),
                        "followers": item.get("followers", ""),
                    }
                )
    elif fmt == "markdown":
        lines = ["| Creator Name | Profile URL | Followers |", "| --- | --- | --- |"]
        for item in items:
            lines.append(
                f"| {item.get('creator_name', '')} | {item.get('profile_url', '')} | {item.get('followers', '')} |"
            )
        output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        raise ValueError(f"unsupported format: {fmt}")

    if mark_submitted and items:
        index = read_json(
            INDEX_PATH,
            {"platform": "instagram", "region": "Nepal", "submitted_handles": [], "records": {}, "updated_at": utc_now()},
        )
        submitted = set(index.get("submitted_handles", []))
        for item in items:
            handle = str(item.get("handle", "")).strip().lower()
            if handle:
                submitted.add(handle)
        index["submitted_handles"] = sorted(submitted)
        index["updated_at"] = utc_now()
        write_json(INDEX_PATH, index)
        pending["items"] = []
        pending["updated_at"] = utc_now()
        write_json(PENDING_SUBMISSIONS_PATH, pending)

    return {"ok": True, "count": len(items), "output": str(output), "format": fmt, "marked_submitted": mark_submitted}


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    manual = subparsers.add_parser("manual-run")
    manual.add_argument("--agent", default="main")
    manual.add_argument("--batch-size", type=int, default=24)
    manual.add_argument("--micro-batch-size", type=int, default=8)
    manual.add_argument("--thinking", default="medium")

    runtime = subparsers.add_parser("start-runtime")
    runtime.add_argument("--agent", default="main")
    runtime.add_argument("--batch-size", type=int, default=int(os.environ.get("INSTAGRAM_BATCH_SIZE", "24")))
    runtime.add_argument("--micro-batch-size", type=int, default=int(os.environ.get("INSTAGRAM_MICRO_BATCH_SIZE", "8")))
    runtime.add_argument("--thinking", default="medium")

    cron = subparsers.add_parser("install-cron")
    cron.add_argument("--agent", default="main")
    cron.add_argument("--job-name", default="Instagram Nepal Discovery")
    cron.add_argument("--every", default=os.environ.get("INSTAGRAM_CRON_INTERVAL", "12h"))
    cron.add_argument("--batch-size", type=int, default=int(os.environ.get("INSTAGRAM_BATCH_SIZE", "24")))
    cron.add_argument("--micro-batch-size", type=int, default=int(os.environ.get("INSTAGRAM_MICRO_BATCH_SIZE", "8")))

    export = subparsers.add_parser("export-pending")
    export.add_argument("--format", choices=["json", "csv", "markdown"], default="markdown")
    export.add_argument("--output", required=True)
    export.add_argument("--mark-submitted", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "manual-run":
            result = agent_turn(
                agent=args.agent,
                message=build_batch_message(batch_size=args.batch_size, micro_batch_size=args.micro_batch_size),
                thinking=args.thinking,
            )
        elif args.command == "start-runtime":
            result = start_runtime(
                agent=args.agent,
                batch_size=args.batch_size,
                micro_batch_size=args.micro_batch_size,
                thinking=args.thinking,
            )
        elif args.command == "install-cron":
            result = install_cron(
                every=args.every,
                agent=args.agent,
                job_name=args.job_name,
                batch_size=args.batch_size,
                micro_batch_size=args.micro_batch_size,
            )
        else:
            result = export_pending(
                output=Path(args.output).expanduser().resolve(),
                fmt=args.format,
                mark_submitted=args.mark_submitted,
            )
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
