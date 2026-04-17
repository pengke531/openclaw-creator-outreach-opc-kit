$ErrorActionPreference = "Stop"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
  throw "[creator-opc] python or python3 not found in PATH"
}

$targetRoot = if ($env:OPENCLAW_STATE_DIR) { $env:OPENCLAW_STATE_DIR } else { "$HOME\\.openclaw" }
& $python.Source (Join-Path $PSScriptRoot "smoke_test.py") --target-root $targetRoot
