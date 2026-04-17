param(
  [string]$TargetRoot = "$HOME\\.openclaw"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
  throw "[creator-opc] python or python3 not found in PATH"
}

Write-Host "[creator-opc] repo root:   $repoRoot"
Write-Host "[creator-opc] host target: $TargetRoot"

${env:OPENCLAW_STATE_DIR} = $TargetRoot
${env:OPENCLAW_CONFIG_PATH} = Join-Path $TargetRoot "openclaw.json"

Push-Location $repoRoot
try {
  powershell -ExecutionPolicy Bypass -File ".\\workspace\\scripts\\bootstrap-profile.ps1"
  powershell -ExecutionPolicy Bypass -File ".\\workspace\\scripts\\preflight.ps1" -TargetRoot $TargetRoot
  powershell -ExecutionPolicy Bypass -File ".\\workspace\\scripts\\sync-optional-skills.ps1"
  & $python.Source ".\\workspace\\scripts\\deploy_profile.py" --target-root $TargetRoot --package-root $repoRoot

  $domainRoot = Join-Path $TargetRoot "domains\\creator-outreach-opc"
  $envTemplate = Join-Path $domainRoot ".env.template"
  $envPath = Join-Path $domainRoot ".env"
  if ((Test-Path $envTemplate) -and -not (Test-Path $envPath)) {
    Copy-Item -LiteralPath $envTemplate -Destination $envPath -Force
    Write-Host "[creator-opc] created optional template file: $envPath"
  }

  openclaw config validate | Out-Host

  $gatewayOk = $false
  try {
    openclaw gateway probe | Out-Host
    $gatewayOk = $true
  }
  catch {
    Write-Host "[creator-opc] gateway probe skipped or failed; import still completed."
  }

  if ($gatewayOk) {
    try {
      powershell -ExecutionPolicy Bypass -File ".\\workspace\\scripts\\smoke-test.ps1"
    }
    catch {
      Write-Host "[creator-opc] automatic smoke test failed. Run verify-creator-outreach.ps1 after checking the gateway."
      throw
    }
  }

  Write-Host ""
  Write-Host "[creator-opc] import complete."
  Write-Host "[creator-opc] next steps:"
  Write-Host "  1. Review optional integration template: $envPath"
  if (-not $gatewayOk) {
    Write-Host "  2. Start OpenClaw normally: openclaw gateway"
    Write-Host "  3. Verify the domain: powershell -ExecutionPolicy Bypass -File .\\verify-creator-outreach.ps1"
  }
  else {
    Write-Host "  2. Domain import and smoke test already passed."
    Write-Host "  3. Re-run verification any time: powershell -ExecutionPolicy Bypass -File .\\verify-creator-outreach.ps1"
  }
}
finally {
  Pop-Location
}
