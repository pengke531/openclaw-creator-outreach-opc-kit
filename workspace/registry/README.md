# Registry

This folder is the structured source of truth for the creator-outreach domain.

## Subfolders

- `creators/` -> canonical creator records
- `campaigns/` -> campaign briefs, rule locks, and lifecycle state
- `approvals/` -> Wangcai approval decisions
- `metrics/` -> accepted day4/day8 snapshots
- `indexes/` -> dedup and alias indexes

## Rules

- only Wangcai writes `registry/`
- one creator = one canonical file
- one campaign = one canonical campaign file
- approval records are immutable after issue; append versions instead of rewriting history
- dedup indexes must point back to canonical creator ids
- Laicai and Facai submit packets into `workspace/inbox/`, then Wangcai decides what enters the registry
