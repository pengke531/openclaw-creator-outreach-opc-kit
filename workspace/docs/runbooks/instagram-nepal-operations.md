# Instagram Nepal Operations

This runbook covers the Instagram-only Nepal creator sourcing line.

## Objective

Continuously discover, verify, register, and queue submission-ready Nepal
Instagram personal creators without letting partial evidence leak into the
formal registry.

## Batch rhythm

1. Search 8 new candidates.
2. Verify each candidate profile.
3. Save an evidence JSON payload for each review.
4. Run the registry helper script on every reviewed candidate.
5. Allow only fully qualified records into `registry/creators`.
6. Let duplicates update followers and `updated_at` only.
7. Pull the simplified pending submission bundle only after the user target is met.

## Payload shape for the helper script

```json
{
  "creator_name": "Example Creator",
  "profile_url": "https://www.instagram.com/example/",
  "followers": "152K",
  "geography_status": "PASS",
  "persona_status": "PASS",
  "followers_status": "PASS",
  "decision": "QUALIFIED",
  "evidence_summary": "Bio and repeated profile content indicate Nepal-based personal creator.",
  "evidence_refs": [],
  "geography_evidence": "Bio says Kathmandu, Nepal.",
  "persona_evidence": "Profile is clearly a person-led creator account.",
  "followers_evidence": "Visible profile follower display shows 152K."
}
```

## Commands

Qualified record:

```powershell
python workspace/scripts/instagram_registry_ops.py upsert-qualified --payload .\tmp\payload.json
```

Evidence gap, fail, or duplicate:

```powershell
python workspace/scripts/instagram_registry_ops.py record-review --payload .\tmp\payload.json
```

## Output locations

- evidence packets: `workspace/evidence/creators/`
- canonical creators: `workspace/registry/creators/`
- dedup index: `workspace/registry/indexes/instagram-nepal-index.json`
- pending submissions: `workspace/inbox/outreach-results/instagram-nepal-pending-submissions.json`

## Rules that must never be bypassed

- Never register a creator unless all hard gates pass.
- Never submit the same handle twice.
- Never continue automated progression after a creator reply is received.
