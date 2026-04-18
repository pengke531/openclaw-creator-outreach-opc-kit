# Usage

Assumption: OpenClaw is already installed and the gateway can run normally.

## Fast path

1. Clone this repository on the target machine
2. Run the installer
3. Let the installer import the domain pack and install the recurring cron
4. Use the manual batch script or wait for cron
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
- `~/.openclaw/domains/creator-outreach-opc/workspace/scripts/instagram_ops.py`
- `~/.openclaw/domains/creator-outreach-opc/workspace/scripts/instagram_registry_ops.py`
- `~/.openclaw/domains/creator-outreach-opc/workspace/registry/indexes/instagram-nepal-index.json`
- `~/.openclaw/domains/creator-outreach-opc/workspace/inbox/outreach-results/instagram-nepal-pending-submissions.json`
