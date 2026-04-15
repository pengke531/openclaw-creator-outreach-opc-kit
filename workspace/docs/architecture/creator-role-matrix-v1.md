# Creator Role Matrix v1

## Team structure

- `creator_manager / A01 Campaign Manager`: owner interface, approvals, orchestration, state advancement
- `creator_scout / A02 Scout`: sourcing, screening, evidence, dedup pre-check
- `creator_connector / A03 Connector`: outreach execution, delivery feedback, reply packet drafting
- `creator_analyst / A04 Analyst`: ROI review, stop-loss, optimization advice

## Ownership matrix

| Work type | Primary owner | Secondary support | Final acceptance |
| --- | --- | --- | --- |
| Batch goal intake | `creator_manager` | none | `creator_manager` |
| Creator sourcing | `creator_scout` | `creator_manager` | `creator_manager` |
| Evidence gap escalation | `creator_scout` | `creator_manager` | `creator_manager` |
| Dedup judgement packet | `creator_scout` | `creator_manager` | `creator_manager` |
| Outreach list release | `creator_manager` | `creator_connector` | `creator_manager` |
| Email delivery | `creator_connector` | `creator_manager` | `creator_connector` |
| Delivery failure reporting | `creator_connector` | `creator_manager` | `creator_manager` |
| Inbound reply packet | `creator_connector` | `creator_manager` | `creator_manager` |
| Day-4 ROI review | `creator_analyst` | `creator_manager` | `creator_manager` |
| Day-8 closeout | `creator_analyst` | `creator_manager` | `creator_manager` |
| Screening optimization feedback | `creator_analyst` | `creator_manager` | `creator_manager` |
| Outreach copy optimization feedback | `creator_analyst` | `creator_manager` | `creator_manager` |

## Routing rules

- If the task is about owner communication, approval, status advancement, or next-step assignment, `creator_manager` owns it.
- If the task is about finding or validating creator candidates, `creator_scout` owns it.
- If the task is about sending or monitoring outreach, `creator_connector` owns it.
- If the task is about ROI or campaign-quality judgement, `creator_analyst` owns it.

## Red-line rules

- `creator_scout` never contacts creators.
- `creator_connector` never sends an unapproved reply to a creator message.
- `creator_analyst` never changes live campaign state directly.
- `creator_manager` never fabricates specialist evidence to save time.
