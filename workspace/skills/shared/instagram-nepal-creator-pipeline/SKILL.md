---
name: instagram-nepal-creator-pipeline
description: Use when OpenClaw needs to continuously discover, verify, deduplicate, register, and prepare submission lists for Nepal Instagram personal creators. This skill is Instagram-only. It enforces hard gates for Nepal geography, personal creator identity, follower count >= 100000, evidence sufficiency, no pre-registration before full qualification, duplicate update without duplicate submission, and reply-triggered freeze handling.
user-invocable: false
---

# Instagram Nepal Creator Pipeline

This skill is for the `wangcai` and `main` path inside the creator-outreach OPC
domain pack.

Use it only for:

- Nepal creator discovery on Instagram
- page-by-page qualification
- evidence packet drafting
- duplicate detection and qualified registration
- final three-column submission list preparation

Do not use it for:

- Facebook discovery
- TikTok / YouTube / X / other platforms
- outreach execution
- speculative registration before evidence is complete

## Hard gates

A creator may be registered or submitted only if all conditions are true:

1. `platform = instagram`
2. geography is clearly Nepal
3. account is clearly a personal creator / personal IP
4. followers shown on profile are at least `100000`
5. evidence is clear enough for geography, identity, and followers

If any gate is unclear, classify as `EVIDENCE_GAP`.

## Operating rhythm

Use this rhythm every cycle:

1. Run a logical batch of 24 candidates.
2. Execute it as three micro-batches of 8 to reduce noise and failure blast radius.
3. Verify each profile page one by one.
4. Draft evidence packets for each candidate.
5. Register only fully qualified creators.
6. Update duplicates in place.
7. Leave unqualified and evidence-gap creators out of formal registry.
8. Append only qualified, non-duplicate creators to the pending submission set.

Do not interrupt the user with partial delivery unless explicitly asked.

## Discovery and verification order

Prefer these sources in order:

1. bundled optional skill `agent-reach`
2. bundled optional skill `autoglm-browser-agent`
3. bundled optional skill `search` or `tavily`
4. direct provider API calls described in `references/provider-matrix.md`

Prefer `Apify` as the first bulk profile verification provider when available.
Use `Bright Data` as fallback when Apify is missing or unstable.

## Required deliverables

For every checked creator, produce:

- one evidence file in `workspace/evidence/creators/`
- one formal registry update only if fully qualified
- one pending submission entry only if newly qualified and not already submitted

Qualified records must preserve the simplified submission view:

- creator name
- profile url
- followers

## Stable file paths

- evidence packets: `workspace/evidence/creators/*.json`
- canonical creator records: `workspace/registry/creators/*.json`
- dedup and submission index: `workspace/registry/indexes/instagram-nepal-index.json`
- pending submission bundle: `workspace/inbox/outreach-results/instagram-nepal-pending-submissions.json`

## Registry guardrail

Use the helper script instead of hand-editing registry files:

```powershell
python workspace/scripts/instagram_registry_ops.py upsert-qualified --payload <payload.json>
```

The script enforces:

- no registration before all hard gates pass
- canonical dedup by normalized Instagram handle and profile URL
- duplicate update without duplicate submission
- stable `updated_at`
- pending submission queue updates only for new qualified creators

For evidence gaps:

```powershell
python workspace/scripts/instagram_registry_ops.py record-review --payload <payload.json>
```

## Reply freeze rule

If outreach later receives a creator reply, this pipeline must freeze further
automated progression for that creator until `main` explicitly approves the next
step. Do not auto-advance a replied creator back into discovery or outreach.

## What `wangcai` should do

- discover and verify candidates in micro-batches of 8
- verify geography, personal identity, and followers
- save proof-rich evidence packets
- return structured evidence to `main`
- report batch progress to `main`

## What `main` should do

- lock screening rules
- orchestrate one logical batch of 24
- use `exec` for domain-owned helper scripts when registration or export must be deterministic
- review only exception cases when needed
- trust the script-enforced dedup path for normal qualified updates
- release the final simplified list only after the full requested target is met

## References

Read these only when needed:

- `references/provider-matrix.md` for API/provider choices
- `references/evidence-rules.md` for exact acceptance rules
