# Usage

Assumption: OpenClaw is already installed and working.

## Preferred delivery mode

This repository is the source of truth.

Preferred flow:

1. Clone this repository on the customer machine
2. Open Codex in this repository
3. Ask Codex to manually fix and configure the local architecture by following `MANUAL_CONFIGURATION_SPEC.md`

That means the customer-local Codex should read the repository architecture and manually align the local OpenClaw profile, instead of depending on a one-shot shell script.

## Target architecture

- `main` -> manager
- `wangcai` -> discovery and evidence executor
- `laicai` -> outreach executor
- `facai` -> ROI executor

## System layers

- `workspace/registry`
- `workspace/evidence`
- `workspace/inbox`
