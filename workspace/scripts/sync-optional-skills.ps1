$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$dest = Join-Path $root "workspace\\skills\\shared"
$source = Join-Path $HOME ".agents\\skills"

$skills = @(
  "search",
  "tavily",
  "agent-reach",
  "autoglm-browser-agent",
  "web-scraping",
  "clawdefender-1",
  "notion",
  "gog"
)

$found = @()
$missing = @()

New-Item -ItemType Directory -Force $dest | Out-Null

foreach ($name in $skills) {
  $from = Join-Path $source $name
  if (Test-Path $from) {
    $to = Join-Path $dest $name
    Copy-Item $from $to -Recurse -Force
    $found += $name
  }
  else {
    $missing += $name
  }
}

Write-Host "[creator-opc] optional shared skills synchronized."
Write-Host ("[creator-opc] found:   " + ($(if ($found.Count -gt 0) { $found -join ", " } else { "(none)" })))
Write-Host ("[creator-opc] missing: " + ($(if ($missing.Count -gt 0) { $missing -join ", " } else { "(none)" })))
