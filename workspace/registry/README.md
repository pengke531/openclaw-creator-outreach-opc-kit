# Registry

This folder is the structured state layer for the creator-outreach domain.

## Subfolders

- `creators/` -> canonical creator records and dedup metadata
- `campaigns/` -> outreach batch and lifecycle state records
- `approvals/` -> owner approval packets and decisions
- `metrics/` -> day-4 and day-8 review snapshots

## Rules

- one creator = one canonical file
- one batch = one canonical campaign record
- approval packets should be immutable once issued; append new versions instead of overwriting history
- metrics snapshots should reference the campaign and creator ids they evaluate
