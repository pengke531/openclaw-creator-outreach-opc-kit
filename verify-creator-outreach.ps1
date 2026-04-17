param(
  [string]$TargetRoot = "$HOME\\.openclaw"
)

$ErrorActionPreference = "Stop"

${env:OPENCLAW_STATE_DIR} = $TargetRoot
${env:OPENCLAW_CONFIG_PATH} = Join-Path $TargetRoot "openclaw.json"

powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\\workspace\\scripts\\preflight.ps1" -TargetRoot $TargetRoot
powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\\workspace\\scripts\\smoke-test.ps1"
