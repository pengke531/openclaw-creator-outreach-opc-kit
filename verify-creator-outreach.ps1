param(
  [string]$TargetRoot = "$HOME\\.openclaw"
)

$ErrorActionPreference = "Stop"

powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\\workspace\\scripts\\preflight.ps1" -TargetRoot $TargetRoot
powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\\workspace\\scripts\\smoke-test.ps1"
