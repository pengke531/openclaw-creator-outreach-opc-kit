# Stable Operations v1

This creator package is designed to run inside an existing OpenClaw host
without an external workflow orchestrator.

## Stability principles

- keep one host OpenClaw root
- add one creator domain under `domains/creator-outreach-opc`
- keep the manager approval path clear so specialists cannot bypass it
- prefer structured registry writes over long free-form memory drift
- degrade cleanly when optional skills or integrations are missing

## Runtime expectations

- host `main` may route creator work into `creator_manager`
- `creator_manager` handles intake, approval, routing, and acceptance
- `creator_scout` handles sourcing and screening
- `creator_connector` handles delivery and reply packet drafting
- `creator_analyst` handles review and optimization

## Operational notes

- validate host config after import
- keep optional domain integrations in `domains/creator-outreach-opc/.env`
- do not require the domain to own host provider configuration
- keep structured registry files under `domains/creator-outreach-opc/workspace/registry`

## Failure posture

- missing optional skills -> continue with explicit warning
- missing required structural files -> fail fast
- unresolved creator evidence -> mark `EVIDENCE_GAP`
- unresolved approval -> freeze further outbound action
- unresolved ROI ambiguity -> annotate assumptions and escalate
