# Creator Memory And State Model v3

## Goal

The system must support:

- one controlling brain
- one dedicated discovery and evidence executor
- one dedicated outreach executor
- one dedicated ROI executor
- deterministic dedup
- inbox-based execution handoff
- approval traceability
- audit-ready lifecycle history

## Storage layers

- `L0 Constitution` -> `workspace/AGENTS.md`
- `L1 Shared policy memory` -> `workspace/MEMORY.md`
- `L2 Formal registry` -> `workspace/registry/*`
- `L3 Evidence store` -> `workspace/evidence/*`
- `L4 Execution inbox` -> `workspace/inbox/*`

## Ownership

- `main` owns `registry/*`
- `wangcai` owns evidence packet drafting into `evidence/creators/*`
- `laicai` owns `inbox/outreach-results/*`
- `facai` owns `inbox/roi-results/*`

## Registry folders

- `registry/creators`
- `registry/campaigns`
- `registry/approvals`
- `registry/metrics`
- `registry/indexes`

## Evidence folders

- `evidence/creators`
- `evidence/campaigns`

## Inbox folders

- `inbox/outreach-results`
- `inbox/roi-results`

## Creator state machine

```text
discovered
-> evidence_collecting
-> evidence_gap | screened_fail | screened_pass
-> dedup_rejected | registered
-> approved_for_outreach
-> outreach_in_progress
-> reply_received
-> reply_pending_approval
-> negotiation_active
-> day4_review
-> day4_stoploss | day8_review
-> qualified | low_quality | excluded
-> closed
```

## Campaign state machine

```text
brief_created
-> rules_locked
-> screening_active
-> outreach_ready
-> outreach_active
-> reply_handling
-> mid_review
-> closeout_review
-> optimized
-> closed
```

## Artifact flow

- `main` writes campaign brief and screening rules
- `wangcai` writes evidence packets
- `main` writes canonical creator records and approvals
- `laicai` writes outreach result packets
- `facai` writes ROI packets
- `main` converts approved packets into official state changes

## Identity resolution signals

- canonical page url
- normalized platform handle
- email
- phone / whatsapp
- alternate handles
- manually confirmed alias edges

## Golden rule

If a fact affects approval, outreach release, dedup, or ROI classification, it
must live in `registry/` or `evidence/`, not only in free-form memory.
