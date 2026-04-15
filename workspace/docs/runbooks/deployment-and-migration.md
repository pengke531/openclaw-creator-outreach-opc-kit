# Deployment And Migration

## Safety objective

This package must augment an existing OpenClaw host without replacing the host's
base architecture.

Target host root:

```text
~/.openclaw
```

Creator domain install root:

```text
~/.openclaw/domains/creator-outreach-opc
```

## Recommended host environments

1. macOS or Linux native
2. Windows via WSL2
3. Docker or Podman hosts with a healthy existing OpenClaw install

Native Windows is supported for install and validation, but WSL2 is the
recommended always-on runtime path.

## Local development steps

1. Run `workspace/scripts/bootstrap-profile.ps1`
2. Run `workspace/scripts/preflight.ps1`
3. Run `workspace/scripts/sync-optional-skills.ps1`
4. Deploy with `python workspace/scripts/deploy_profile.py`
5. Validate host config
6. Start the host gateway normally
7. Optionally wire domain integrations in `domains/creator-outreach-opc/.env`

## Migration package

Portable asset set:

- `openclaw.json`
- `agents/`
- `workspace/`
- `.env.template`
- `install-creator-outreach.ps1`
- `install-creator-outreach.sh`
- `workspace/scripts/preflight.ps1`
- `workspace/scripts/deploy_profile.py`
- `workspace/scripts/smoke-test.ps1`
- `workspace/scripts/repair-profile.ps1`

## Deployment contract

- deploy into the host's existing `~/.openclaw`
- copy domain assets into `domains/creator-outreach-opc`
- back up the host `openclaw.json` before merge
- merge overlay config additively
- preserve an existing host `.env`, host channels, and host provider choices
- append outreach agents without deleting unrelated host agents

## Rollback posture

- the deploy step creates a dated backup of the host config
- the domain assets live under their own folder and can be removed without touching unrelated host assets
- `repair-profile.ps1` can be used to re-stamp missing domain files without wiping host state

## Cross-platform note

This package avoids forcing PowerShell Core on Unix-like hosts for merge logic
by using Python for the heavy deployment path. Shell and PowerShell wrappers are
kept only for user entry points.
