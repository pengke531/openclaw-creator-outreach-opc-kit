# Smoke Test v2

## 1. Structural checks

```powershell
powershell -ExecutionPolicy Bypass -File .\workspace\scripts\preflight.ps1
openclaw config validate
```

## 2. Gateway checks

```powershell
openclaw gateway probe
```

## 3. Agent checks

```powershell
openclaw agents list --json
```

Confirm these agents exist:

- `main`
- `laicai`
- `facai`

## 4. System layer checks

Confirm these folders exist:

- `~/.openclaw/domains/creator-outreach-opc/workspace/registry`
- `~/.openclaw/domains/creator-outreach-opc/workspace/evidence`
- `~/.openclaw/domains/creator-outreach-opc/workspace/inbox`

## 5. Policy checks

- `main` can call only `laicai` and `facai`
- `laicai` has no subagent privileges
- `facai` has no subagent privileges
- only Wangcai writes formal records

## 6. Functional prompts

- ask `main` to turn a vague request into a campaign brief
- ask `main` to produce a creator evidence packet with `EVIDENCE_GAP` behavior
- ask `laicai` to produce a reply freeze packet instead of continuing
- ask `facai` to produce a day4 review packet
