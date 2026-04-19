# Install And Run Instagram Nepal

This package supports direct OpenClaw use after import.

## What gets installed

- domain agents and workspace
- bundled Instagram Nepal pipeline skill
- bundled `/workking` runtime-entry skill
- optional shared search skills when present on the host
- manual batch runner
- recurring cron installer
- final submission exporter

## First-time install

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-creator-outreach.ps1
```

Bash:

```bash
./install-creator-outreach.sh
```

## Manual batch run

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-instagram-nepal-batch.ps1
```

Bash:

```bash
./run-instagram-nepal-batch.sh
```

## Chat command

Open a new session after install, then use:

```text
/workking
```

Optional controls:

```text
/workking status
/workking stop
```

`/workking` starts the continuous runtime. It reads the existing local
registry first, rotates the preferred crawler provider, stores every qualified
creator immediately, and keeps looping until it hits the stop rule.

## Install recurring cron

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-instagram-nepal-cron.ps1
```

Bash:

```bash
./install-instagram-nepal-cron.sh
```

Default schedule: every 12 hours, isolated cron session, agent `main`, no direct delivery.

## Runtime rules now enforced

- each internal cycle is capped at 15 minutes
- if there is no new unique qualified creator for 30 minutes, runtime stops
- every start rotates the preferred provider in sequence
- duplicates are ignored up front by reading the local registry index first

## Export final submission list

Markdown:

```powershell
powershell -ExecutionPolicy Bypass -File .\export-instagram-nepal-submissions.ps1 -Format markdown -OutputPath "$HOME\Desktop\instagram-nepal-submissions.md"
```

CSV:

```powershell
powershell -ExecutionPolicy Bypass -File .\export-instagram-nepal-submissions.ps1 -Format csv -OutputPath "$HOME\Desktop\instagram-nepal-submissions.csv"
```

Use `-MarkSubmitted` only when that export is the official final submission.
