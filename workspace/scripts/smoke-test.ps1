$ErrorActionPreference = "Stop"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
  throw "[creator-opc] python or python3 not found in PATH"
}

& $python.Source (Join-Path $PSScriptRoot "smoke_test.py")
