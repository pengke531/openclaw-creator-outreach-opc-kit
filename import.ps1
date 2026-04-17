param(
  [string]$TargetRoot = "$HOME\\.openclaw"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path (Join-Path $PSScriptRoot "install-creator-outreach.ps1"))) {
  throw "[creator-opc] import.ps1 must be run from the repository directory. The file install-creator-outreach.ps1 was not found next to it."
}

powershell -ExecutionPolicy Bypass -File "$PSScriptRoot\\install-creator-outreach.ps1" -TargetRoot $TargetRoot
