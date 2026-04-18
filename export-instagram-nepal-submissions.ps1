param(
  [ValidateSet("markdown", "csv", "json")]
  [string]$Format = "markdown",
  [string]$OutputPath,
  [switch]$MarkSubmitted
)

$ErrorActionPreference = "Stop"

if (-not $OutputPath) {
  throw "OutputPath is required"
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
  throw "python or python3 not found in PATH"
}

$args = @(
  "$PSScriptRoot\workspace\scripts\instagram_ops.py",
  "export-pending",
  "--format", $Format,
  "--output", $OutputPath
)

if ($MarkSubmitted) {
  $args += "--mark-submitted"
}

& $python.Source @args
