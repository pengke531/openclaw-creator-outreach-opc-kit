from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_CREATORS = ROOT / "registry" / "creators"
REGISTRY_INDEXES = ROOT / "registry" / "indexes"
EVIDENCE_CREATORS = ROOT / "evidence" / "creators"
INBOX_OUTREACH = ROOT / "inbox" / "outreach-results"
INDEX_PATH = REGISTRY_INDEXES / "instagram-nepal-index.json"
PENDING_SUBMISSIONS_PATH = INBOX_OUTREACH / "instagram-nepal-pending-submissions.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value or "creator"


def normalize_url(url: str) -> str:
    url = (url or "").strip()
    url = re.sub(r"\?.*$", "", url)
    url = url.rstrip("/")
    if url and not url.startswith("http"):
        url = f"https://{url.lstrip('/')}"
    return url.lower()


def extract_handle(url: str, fallback: str = "") -> str:
    url = normalize_url(url)
    match = re.search(r"instagram\.com/([^/?#]+)", url)
    if match:
        return match.group(1).lower()
    return fallback.strip().lstrip("@").lower()


def parse_followers(raw: Any) -> int:
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float):
        return int(raw)
    text = str(raw or "").strip().lower().replace(",", "")
    if not text:
        raise ValueError("followers value missing")
    multiplier = 1
    if text.endswith("k"):
        multiplier = 1000
        text = text[:-1]
    elif text.endswith("m"):
        multiplier = 1000000
        text = text[:-1]
    return int(float(text) * multiplier)


@dataclass
class ReviewPayload:
    creator_name: str
    profile_url: str
    followers: str
    geography_status: str
    persona_status: str
    followers_status: str
    decision: str
    evidence_summary: str
    evidence_refs: list[str]
    geography_evidence: str
    persona_evidence: str
    followers_evidence: str

    @property
    def normalized_url(self) -> str:
        return normalize_url(self.profile_url)

    @property
    def handle(self) -> str:
        return extract_handle(self.profile_url, self.creator_name)

    @property
    def followers_count(self) -> int:
        return parse_followers(self.followers)


def load_payload(path: Path) -> ReviewPayload:
    raw = read_json(path, None)
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")
    return ReviewPayload(
        creator_name=str(raw.get("creator_name", "")).strip(),
        profile_url=str(raw.get("profile_url", "")).strip(),
        followers=str(raw.get("followers", "")).strip(),
        geography_status=str(raw.get("geography_status", "")).strip().upper(),
        persona_status=str(raw.get("persona_status", "")).strip().upper(),
        followers_status=str(raw.get("followers_status", "")).strip().upper(),
        decision=str(raw.get("decision", "")).strip().upper(),
        evidence_summary=str(raw.get("evidence_summary", "")).strip(),
        evidence_refs=[str(item) for item in raw.get("evidence_refs", [])],
        geography_evidence=str(raw.get("geography_evidence", "")).strip(),
        persona_evidence=str(raw.get("persona_evidence", "")).strip(),
        followers_evidence=str(raw.get("followers_evidence", "")).strip(),
    )


def validate_review(payload: ReviewPayload) -> None:
    if not payload.creator_name:
        raise ValueError("creator_name is required")
    if not payload.normalized_url or "instagram.com/" not in payload.normalized_url:
        raise ValueError("profile_url must be an Instagram profile URL")
    if not payload.handle:
        raise ValueError("unable to determine Instagram handle")
    if payload.decision not in {"QUALIFIED", "DUPLICATE", "SCREENED_FAIL", "EVIDENCE_GAP"}:
        raise ValueError("decision must be QUALIFIED, DUPLICATE, SCREENED_FAIL, or EVIDENCE_GAP")
    if payload.decision in {"QUALIFIED", "DUPLICATE"} and payload.followers_count < 100000:
        raise ValueError("qualified or duplicate entries must have followers >= 100000")


def load_index() -> dict[str, Any]:
    return read_json(
        INDEX_PATH,
        {
            "platform": "instagram",
            "region": "Nepal",
            "submitted_handles": [],
            "records": {},
            "updated_at": utc_now(),
        },
    )


def save_index(index: dict[str, Any]) -> None:
    index["updated_at"] = utc_now()
    write_json(INDEX_PATH, index)


def evidence_file_name(handle: str) -> str:
    return f"instagram-nepal-{slugify(handle)}.json"


def creator_file_name(handle: str) -> str:
    return f"instagram-nepal-{slugify(handle)}.json"


def write_evidence(payload: ReviewPayload) -> str:
    rel = evidence_file_name(payload.handle)
    out = EVIDENCE_CREATORS / rel
    body = {
        "platform": "instagram",
        "region": "Nepal",
        "creator_name": payload.creator_name,
        "profile_url": payload.normalized_url,
        "handle": payload.handle,
        "followers": payload.followers,
        "decision": payload.decision,
        "geography_status": payload.geography_status,
        "persona_status": payload.persona_status,
        "followers_status": payload.followers_status,
        "geography_evidence": payload.geography_evidence,
        "persona_evidence": payload.persona_evidence,
        "followers_evidence": payload.followers_evidence,
        "evidence_summary": payload.evidence_summary,
        "evidence_refs": payload.evidence_refs,
        "updated_at": utc_now(),
    }
    write_json(out, body)
    return str(out.relative_to(ROOT)).replace("\\", "/")


def load_pending_submissions() -> dict[str, Any]:
    return read_json(
        PENDING_SUBMISSIONS_PATH,
        {
            "platform": "instagram",
            "region": "Nepal",
            "items": [],
            "updated_at": utc_now(),
        },
    )


def save_pending_submissions(payload: dict[str, Any]) -> None:
    payload["updated_at"] = utc_now()
    write_json(PENDING_SUBMISSIONS_PATH, payload)


def append_pending_submission(record: dict[str, Any], index: dict[str, Any]) -> None:
    handle = record["channels"][0]["handle"]
    if handle in set(index.get("submitted_handles", [])):
        return
    pending = load_pending_submissions()
    items = pending.get("items", [])
    if any(item.get("handle") == handle for item in items):
        return
    items.append(
        {
            "creator_name": record["registryView"]["creator_name"],
            "profile_url": record["registryView"]["profile_url"],
            "followers": record["registryView"]["followers"],
            "handle": handle,
            "canonical_id": record["canonicalId"],
            "queued_at": utc_now(),
        }
    )
    pending["items"] = items
    save_pending_submissions(pending)


def build_creator_record(payload: ReviewPayload, evidence_ref: str, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    canonical_id = existing["canonicalId"] if existing else f"instagram-nepal-{slugify(payload.handle)}"
    prior_refs = list(existing.get("evidenceRefs", [])) if existing else []
    merged_refs = sorted(set(prior_refs + [evidence_ref] + payload.evidence_refs))
    return {
        "canonicalId": canonical_id,
        "displayName": payload.creator_name,
        "region": "Nepal",
        "platform": "instagram",
        "pageUrl": payload.normalized_url,
        "channels": [
            {
                "platform": "instagram",
                "handle": payload.handle,
                "url": payload.normalized_url,
            }
        ],
        "dedupKeys": {
            "urls": [payload.normalized_url],
            "handles": [payload.handle],
            "emails": [],
            "phones": [],
        },
        "screeningMetrics": {
            "followerCount": payload.followers_count,
        },
        "evidenceRefs": merged_refs,
        "screeningDecision": "screened_pass",
        "status": "registered",
        "notes": payload.evidence_summary,
        "updatedAt": utc_now(),
        "registryView": {
            "creator_name": payload.creator_name,
            "profile_url": payload.normalized_url,
            "followers": payload.followers,
            "status": "registered",
            "updated_at": utc_now(),
        },
        "instagramQualification": {
            "geography_status": payload.geography_status,
            "persona_status": payload.persona_status,
            "followers_status": payload.followers_status,
            "geography_evidence": payload.geography_evidence,
            "persona_evidence": payload.persona_evidence,
            "followers_evidence": payload.followers_evidence,
        },
    }


def register_qualified(payload: ReviewPayload) -> dict[str, Any]:
    if payload.decision != "QUALIFIED":
        raise ValueError("upsert-qualified requires decision=QUALIFIED")
    if payload.geography_status != "PASS":
        raise ValueError("qualified record must have geography_status=PASS")
    if payload.persona_status != "PASS":
        raise ValueError("qualified record must have persona_status=PASS")
    if payload.followers_status != "PASS":
        raise ValueError("qualified record must have followers_status=PASS")

    evidence_ref = write_evidence(payload)
    index = load_index()
    existing_ref = index["records"].get(payload.handle) or index["records"].get(payload.normalized_url)
    existing = None
    if existing_ref:
        candidate_path = ROOT / existing_ref["creator_record"]
        if candidate_path.exists():
            existing = read_json(candidate_path, {})

    record = build_creator_record(payload, evidence_ref, existing=existing)
    creator_rel = f"registry/creators/{creator_file_name(payload.handle)}"
    write_json(ROOT / creator_rel, record)

    entry = {
        "canonical_id": record["canonicalId"],
        "creator_record": creator_rel,
        "profile_url": payload.normalized_url,
        "handle": payload.handle,
        "followers": payload.followers,
        "last_decision": "qualified",
        "updated_at": utc_now(),
    }
    index["records"][payload.handle] = entry
    index["records"][payload.normalized_url] = entry
    save_index(index)
    append_pending_submission(record, index)
    return {
        "result": "registered" if existing is None else "updated_existing",
        "canonical_id": record["canonicalId"],
        "creator_record": creator_rel,
        "evidence_ref": evidence_ref,
    }


def record_review(payload: ReviewPayload) -> dict[str, Any]:
    evidence_ref = write_evidence(payload)
    index = load_index()
    existing = index["records"].get(payload.handle) or index["records"].get(payload.normalized_url)

    result = {
        "result": payload.decision.lower(),
        "evidence_ref": evidence_ref,
        "duplicate_of": existing["canonical_id"] if existing else None,
    }

    if payload.decision == "DUPLICATE":
        if not existing:
            raise ValueError("duplicate decision requires an existing registered creator")
        creator_path = ROOT / existing["creator_record"]
        record = read_json(creator_path, {})
        record["screeningMetrics"]["followerCount"] = payload.followers_count
        record["registryView"]["followers"] = payload.followers
        record["registryView"]["updated_at"] = utc_now()
        record["updatedAt"] = utc_now()
        record["evidenceRefs"] = sorted(set(record.get("evidenceRefs", []) + [evidence_ref] + payload.evidence_refs))
        write_json(creator_path, record)
        existing["followers"] = payload.followers
        existing["last_decision"] = "duplicate_update"
        existing["updated_at"] = utc_now()
        index["records"][payload.handle] = existing
        index["records"][payload.normalized_url] = existing
        save_index(index)

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("upsert-qualified", "record-review"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--payload", required=True)

    args = parser.parse_args()
    payload = load_payload(Path(args.payload))
    validate_review(payload)

    try:
        if args.command == "upsert-qualified":
            result = register_qualified(payload)
        else:
            result = record_review(payload)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps({"ok": True, **result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
