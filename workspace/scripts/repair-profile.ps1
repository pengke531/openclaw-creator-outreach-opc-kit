param(
  [string]$TargetRoot = "$HOME\\.openclaw"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Write-Host "[creator-opc] running repair flow..."
powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "bootstrap-profile.ps1")
powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "preflight.ps1") -TargetRoot $TargetRoot
powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "sync-optional-skills.ps1")
powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "deploy-profile.ps1") -TargetRoot $TargetRoot
openclaw config validate | Out-Host
Write-Host "[creator-opc] repair complete."
