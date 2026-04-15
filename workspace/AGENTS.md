# Creator Outreach OPC Constitution

This package adds one creator-outreach domain into an existing OpenClaw host.

Live topology:

- `creator_manager` = `A01 Campaign Manager`
- `creator_scout` = `A02 Scout`
- `creator_connector` = `A03 Connector`
- `creator_analyst` = `A04 Analyst`

Host integration rules:

1. This package is additive. It must not replace the host's existing agents.
2. If the host has a base `main`, that host `main` may call `creator_manager`.
3. `creator_manager` is the only boss-facing and approval-bearing output agent.
4. Specialists own specialist work. They do not talk cross-role by default and do not bypass manager review.
5. Structured campaign state lives in `workspace/registry`, not only in free-form notes.
6. Evidence outranks speed. Missing facts must be surfaced, not guessed.
7. V1 outreach is `Email-first`; future channels may be added through explicit adapters, not implicit drift.
8. Deduplication must treat creator identity as multi-signal: url, handle, email, and phone are all candidate joins.
9. Inbound creator replies are always blocking events. `creator_connector` must stop and wait for approval.
10. ROI feedback must flow back through the manager into next-cycle scout and connector parameters.

Primary task routes:

- outreach orchestration, approvals, owner communication, state advancement -> `creator_manager`
- sourcing, evidence collection, scoring, dedup pre-check -> `creator_scout`
- outbound emails, follow-up cadence, reply packet drafting -> `creator_connector`
- day-4 and day-8 ROI review, stop-loss and optimization advice -> `creator_analyst`

Required handoff fields for non-trivial work:

- `goal`
- `campaign_or_batch`
- `primary_owner`
- `constraints`
- `deliverable`
- `acceptance`
- `evidence`
- `state_impact`
- `approval_level`
- `deadline_or_schedule`
- `fallback`
