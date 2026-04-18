param(
  [string]$Every = "12h",
  [string]$Agent = "main",
  [int]$BatchSize = 24,
  [int]$MicroBatchSize = 8
)

$ErrorActionPreference = "Stop"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
  throw "python or python3 not found in PATH"
}

& $python.Source "$PSScriptRoot\workspace\scripts\instagram_ops.py" install-cron --every $Every --agent $Agent --batch-size $BatchSize --micro-batch-size $MicroBatchSize
