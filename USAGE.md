# Usage

Assumption: OpenClaw is already installed and working.

## One-command user flow

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

## What the import command does

- runs preflight
- imports the creator-outreach domain into the user's existing OpenClaw state
- merges the overlay config
- validates config
- runs smoke verification automatically when the gateway is already running

## If the gateway is not running

Start it, then run the same import command again:

```bash
openclaw gateway
```
