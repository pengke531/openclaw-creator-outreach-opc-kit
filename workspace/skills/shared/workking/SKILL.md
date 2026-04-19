---
name: workking
description: Start, stop, or inspect the Instagram Nepal continuous discovery runtime. Use /workking to start the loop immediately. This command is for Instagram-only Nepal creator discovery with strict qualification, local dedup, provider rotation, and runtime stop rules.
user-invocable: true
---

# Workking Runtime Control

This skill is the user-facing entrypoint for the Instagram Nepal pipeline.

Direct command:

- `/workking`

Supported forms:

- `/workking`
- `/workking start`
- `/workking status`
- `/workking stop`

Treat omitted input as `start`.

## Rules

- This command controls the Instagram Nepal runtime only.
- The runtime must use the existing file-based registry, evidence, and inbox
  state under `workspace/`.
- Do not manually edit registry files. Use the packaged Python helper instead.
- Do not ask the user to restate the workflow. Start it directly.

## Start behavior

When the input is empty or `start`:

1. Use `exec`.
2. Run:

```powershell
python workspace/scripts/instagram_runtime.py start
```

3. Return the resulting runtime status and stop reason summary.

The runtime script already handles:

- reading the current registry index first
- skipping already stored creators
- rotating the preferred provider each launch
- enforcing 15 minute max per cycle
- stopping after 30 minutes without a new unique qualified creator
- immediate per-creator persistence
- self-looping until a stop condition is reached

## Status behavior

When the input is `status`:

```powershell
python workspace/scripts/instagram_runtime.py status
```

## Stop behavior

When the input is `stop`:

```powershell
python workspace/scripts/instagram_runtime.py stop
```

## Dispatch notes

- Use the `instagram-nepal-creator-pipeline` skill as the operational rulebook
  for each internal discovery cycle.
- Keep output short and operational.
- Do not generate a candidate list in chat.
