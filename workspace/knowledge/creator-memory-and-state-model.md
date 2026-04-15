# Creator Memory And State Model

## Purpose

The memory and state system must support:

- durable business rules
- creator identity resolution
- campaign lifecycle visibility
- approval traceability
- low token cost
- audit-friendly archival behavior

## Layers

- `L0 Constitution`
- `L1 Role-local memory`
- `L2 Shared policy memory`
- `L3 Structured registry state`
- `L4 External artifacts and evidence references`

## Rule of use

### Memory is for:

- policies
- stable heuristics
- reusable patterns
- current-cycle parameters that affect more than one creator

### Registry is for:

- creator records
- dedup keys
- campaign states
- approval packets
- ROI snapshots
- exclusion reasons

## Registry folders

- `registry/creators`
- `registry/campaigns`
- `registry/approvals`
- `registry/metrics`

## Core state transitions

```text
discovered
-> evidence_gap | dedup_rejected | manager_review
-> owner_review
-> approved_for_outreach
-> contacted
-> delivery_failed | awaiting_reply
-> reply_received
-> reply_pending_approval
-> reply_approved
-> negotiation_in_progress
-> day4_watch | day4_stoploss
-> day8_qualified | day8_low_quality | excluded
-> closed
```

## Identity resolution signals

- canonical page url
- platform handle
- email
- whatsapp / phone
- alternate handles
- operator-confirmed alias links

## Confidentiality rule

Store only the smallest operationally useful summary in memory. Detailed creator
records live in registry files or referenced evidence sources.
