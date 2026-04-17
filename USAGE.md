# Usage

Assumption: OpenClaw is already installed and working.

## Preferred delivery mode

This repository is now the source of truth.

Preferred flow:

1. Clone this repository on the customer machine
2. Open Codex in this repository
3. Ask Codex to perform the local import by following `CUSTOMER_LOCAL_IMPORT.md`

That means the customer-local Codex should import the architecture from the repository files into the local OpenClaw profile, instead of depending only on a one-shot shell script.

## Customer-local Codex prompt

Use the instruction block in `CUSTOMER_LOCAL_IMPORT.md` directly.

## Auxiliary one-command import

### Windows

```powershell
git clone https://github.com/pengke531/openclaw-creator-outreach-opc-kit
cd openclaw-creator-outreach-opc-kit
powershell -ExecutionPolicy Bypass -File .\import.ps1
```

### macOS / Linux / WSL2

```bash
git clone https://github.com/pengke531/openclaw-creator-outreach-opc-kit
cd openclaw-creator-outreach-opc-kit
chmod +x ./import.sh
./import.sh
```

## Imported topology

- `main` -> Wangcai controller
- `laicai` -> outreach executor
- `facai` -> ROI analyst

## Imported storage layers

- `workspace/registry`
- `workspace/evidence`
- `workspace/inbox`

## Verify after import

```powershell
powershell -ExecutionPolicy Bypass -File .\verify-creator-outreach.ps1
```
