# Usage

Assumption: OpenClaw is already installed and the gateway can run normally.

## Fast path

1. Clone this repository on the target machine
2. Run the installer
3. Open a new OpenClaw chat session and run `/workking`
4. Or use the manual runtime script / recurring cron
5. Export the final list when the target delta is reached

## Install

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-creator-outreach.ps1
```

Bash:

```bash
./install-creator-outreach.sh
```

## Manual trigger

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-instagram-nepal-batch.ps1
```

Bash:

```bash
./run-instagram-nepal-batch.sh
```

## Chat trigger

```text
/workking
```

Optional:

```text
/workking status
/workking stop
```

## Recurring trigger

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-instagram-nepal-cron.ps1
```

Bash:

```bash
./install-instagram-nepal-cron.sh
```

## Export

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\export-instagram-nepal-submissions.ps1 -Format markdown -OutputPath "$HOME\Desktop\instagram-nepal-submissions.md"
```

Use `-MarkSubmitted` only for the official final export.

## Runtime path after install

Installed domain root:

- `~/.openclaw/domains/creator-outreach-opc`

Important files after install:

- `~/.openclaw/domains/creator-outreach-opc/workspace/skills/shared/instagram-nepal-creator-pipeline/SKILL.md`
- `~/.openclaw/domains/creator-outreach-opc/workspace/skills/shared/workking/SKILL.md`
- `~/.openclaw/domains/creator-outreach-opc/workspace/scripts/instagram_ops.py`
- `~/.openclaw/domains/creator-outreach-opc/workspace/scripts/instagram_runtime.py`
- `~/.openclaw/domains/creator-outreach-opc/workspace/scripts/instagram_registry_ops.py`
- `~/.openclaw/domains/creator-outreach-opc/workspace/registry/indexes/instagram-nepal-index.json`
- `~/.openclaw/domains/creator-outreach-opc/workspace/registry/indexes/instagram-nepal-runtime-state.json`
- `~/.openclaw/domains/creator-outreach-opc/workspace/inbox/outreach-results/instagram-nepal-pending-submissions.json`
