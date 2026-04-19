param(
  [string]$TargetRoot = "$HOME\\.openclaw"
)

$ErrorActionPreference = "Stop"

${env:OPENCLAW_STATE_DIR} = $TargetRoot
${env:OPENCLAW_CONFIG_PATH} = Join-Path $TargetRoot "openclaw.json"

powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\\workspace\\scripts\\preflight.ps1" -TargetRoot $TargetRoot
powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\\workspace\\scripts\\smoke-test.ps1"

$required = @(
  "$PSScriptRoot\\workspace\\scripts\\instagram_ops.py",
  "$PSScriptRoot\\workspace\\scripts\\instagram_runtime.py",
  "$PSScriptRoot\\workspace\\scripts\\instagram_registry_ops.py",
  "$PSScriptRoot\\workspace\\skills\\shared\\instagram-nepal-creator-pipeline\\SKILL.md",
  "$PSScriptRoot\\workspace\\skills\\shared\\workking\\SKILL.md",
  "$PSScriptRoot\\install-instagram-nepal-cron.ps1",
  "$PSScriptRoot\\run-instagram-nepal-batch.ps1",
  "$PSScriptRoot\\export-instagram-nepal-submissions.ps1"
)

foreach ($path in $required) {
  if (-not (Test-Path $path)) {
    throw "missing required Instagram Nepal runtime file: $path"
  }
}
