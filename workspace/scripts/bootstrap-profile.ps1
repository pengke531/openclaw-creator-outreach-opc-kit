$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$config = Join-Path $root "openclaw.json"

Write-Host "[creator-opc] root: $root"

if (-not (Test-Path $config)) {
  throw "openclaw.json not found: $config"
}

$required = @(
  "agents\\wangcai\\AGENTS.md",
  "agents\\laicai\\AGENTS.md",
  "agents\\facai\\AGENTS.md",
  "workspace\\AGENTS.md",
  "workspace\\MEMORY.md"
)

foreach ($rel in $required) {
  $full = Join-Path $root $rel
  if (-not (Test-Path $full)) {
    throw "missing required file: $full"
  }
}

Write-Host "[creator-opc] profile scaffold is structurally complete."
