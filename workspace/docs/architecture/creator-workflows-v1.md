# Creator Workflows v1

## Required workflow set

This OPC must cover these recurring workflows without role ambiguity:

1. campaign brief intake
2. creator sourcing and evidence collection
3. deduplication and exclusion filtering
4. owner review and release
5. outreach delivery and failure handling
6. inbound reply freeze and approval packet generation
7. day-4 ROI review and stop-loss suggestion
8. day-8 closeout and creator grading
9. parameter feedback into the next cycle

## Workflow details

### 1. Campaign brief intake

- Owner: `creator_manager`
- Inputs: target geography, creator type, volume target, operating constraints
- Outputs: task contract, batch id, screening config, approval level

### 2. Creator sourcing

- Owner: `creator_scout`
- Inputs: screening config, category rules, minimum thresholds
- Outputs: screened creator report, evidence set, scoring summary, evidence gaps

### 3. Outreach release

- Owner: `creator_manager`
- Inputs: screened creator report, dedup outcome, owner preferences
- Outputs: approved outreach list, blocked list, exclusions

### 4. Delivery execution

- Owner: `creator_connector`
- Inputs: approved outreach list, email templates, cadence policy
- Outputs: delivery report, failures, campaign state update

### 5. Reply packet

- Owner: `creator_connector`
- Inputs: creator reply, current campaign state, prior messages
- Outputs: original creator text, proposed reply v1, risk note, approval request

### 6. ROI review

- Owner: `creator_analyst`
- Inputs: day-4 or day-8 performance data
- Outputs: ROI judgement, creator grading, stop-loss or optimization recommendation

### 7. Parameter feedback

- Owner: `creator_manager`
- Inputs: analyst recommendation package
- Outputs: updated screening parameters, updated outreach rules, next-cycle brief
