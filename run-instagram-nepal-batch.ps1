param(
  [string]$Agent = "main",
  [int]$BatchSize = 24,
  [int]$MicroBatchSize = 8,
  [string]$Thinking = "medium"
)

$ErrorActionPreference = "Stop"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
  throw "python or python3 not found in PATH"
}

& $python.Source "$PSScriptRoot\workspace\scripts\instagram_ops.py" manual-run --agent $Agent --batch-size $BatchSize --micro-batch-size $MicroBatchSize --thinking $Thinking
