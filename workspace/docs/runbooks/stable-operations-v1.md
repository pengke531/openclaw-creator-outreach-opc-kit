# Stable Operations v2

This package is designed around one controller and two narrow executors.

## Stability principles

- one controller brain: Wangcai (`main`)
- one formal source of truth: `registry/`
- one evidence layer: `evidence/`
- one execution inbox: `inbox/`
- no middle manager agent
- no subagent cross-talk

## Runtime expectations

- `main` handles intake, verification, dedup, approval, and final reporting
- `laicai` handles outreach execution only
- `facai` handles ROI review only

## Failure posture

- missing optional skills -> continue with warning
- missing required structural files -> fail fast
- unresolved creator evidence -> mark `EVIDENCE_GAP`
- unresolved approval -> freeze outbound action
- unresolved ROI ambiguity -> write assumptions explicitly into the packet
