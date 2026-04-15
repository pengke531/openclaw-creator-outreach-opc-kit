# Smoke Test

Run these checks after additive deployment into the host OpenClaw environment.

## 1. Structural checks

```powershell
powershell -ExecutionPolicy Bypass -File .\workspace\scripts\preflight.ps1
openclaw config validate
```

## 2. Gateway checks

```powershell
openclaw gateway probe
Invoke-WebRequest http://127.0.0.1:18789/ -UseBasicParsing
```

## 3. Agent checks

```powershell
openclaw agents list --json
```

Confirm these agents exist:

- `creator_manager`
- `creator_scout`
- `creator_connector`
- `creator_analyst`

If the host has a base `main`, confirm that `main` can call `creator_manager`.

## 4. Domain state checks

- confirm `~/.openclaw/domains/creator-outreach-opc/workspace/registry` exists
- confirm `creator.schema.json`, `campaign.schema.json`, and `approval.schema.json` exist
- confirm outreach templates exist

## 5. Policy checks

- manager allowlist includes the three specialists
- specialists do not have cross-agent subagent privileges
- connector has no approval-bypassing send policy inside the domain pack itself

## 6. Functional prompts

- ask `creator_manager` to classify a campaign brief and assign owners
- ask `creator_scout` to produce a creator screening packet with `EVIDENCE_GAP` behavior
- ask `creator_connector` to produce a reply-approval packet instead of sending a reply
- ask `creator_analyst` to classify a creator on day 4 and day 8
