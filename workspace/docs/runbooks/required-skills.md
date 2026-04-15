# Optional Skills

This package separates skills into three buckets:

## Tier 1: not required for installation

The package installs and validates without these skills.

- `search`
- `tavily`
- `agent-reach`
- `autoglm-browser-agent`

## Tier 2: useful for better sourcing fidelity

- `web-scraping`
- `clawdefender-1`

## Tier 3: useful when extending into CRM or docs automation

- `notion`
- `gog`
- `feishu-doc`
- `feishu-drive`

## Synchronization behavior

`sync-optional-skills.ps1` copies any available recommended skills from the host
global skill catalog into:

```text
~/.openclaw/domains/creator-outreach-opc/workspace/skills/shared
```

If a skill is missing:

- installation continues
- the preflight output prints it as optional-missing
- the operator can still run the core architecture pack

This is intentional. The package should degrade, not fail closed, when optional
ecosystem tools are absent.
