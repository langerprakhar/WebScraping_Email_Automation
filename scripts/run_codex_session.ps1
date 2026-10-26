# Run exactly one Codex V2 session in its own workspace (PowerShell 5.1+).
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("00", "01", "02", "03", "04", "05", "06", "07")]
    [string]$Session,
    [string]$Workspace = (Get-Location).Path
)
$ErrorActionPreference = 'Stop'
$map = @{
    '00' = '00-foundation.md'
    '01' = '01-gt-gra.md'
    '02' = '02-gt-gta.md'
    '03' = '03-industry-clay.md'
    '04' = '04-research-drafting.md'
    '05' = '05-outlook-local.md'
    '06' = '06-qa-security.md'
    '07' = '07-integration.md'
}
$codex = Get-Command codex -ErrorAction SilentlyContinue
if (-not $codex) { throw 'Codex CLI is not installed or is not on PATH. Install/sign in first.' }
$root = (& git -C $Workspace rev-parse --show-toplevel)
if ($LASTEXITCODE -ne 0 -or -not $root) { throw "Workspace is not a Git worktree: $Workspace" }
$root = ($root | Select-Object -First 1).Trim()
$promptPath = Join-Path $root ("codex_prompts/" + $map[$Session])
if (-not (Test-Path -LiteralPath $promptPath)) { throw "Prompt file not found: $promptPath" }
$logs = Join-Path $root ".codex_runs"
New-Item -ItemType Directory -Force -Path $logs | Out-Null
$logFile = Join-Path $logs ("session-" + $Session + ".log")
$branch = (& git -C $root branch --show-current).Trim()
Write-Host "Starting Codex Session $Session in $root ($branch)"
Write-Host "Prompt: $promptPath"
Write-Host "Live output log: $logFile"
Push-Location $root
try {
    Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8 |
        & $codex.Source exec --sandbox workspace-write - 2>&1 |
        Tee-Object -FilePath $logFile
    $code = $LASTEXITCODE
    if ($code -ne 0) { throw "Codex session $Session exited with code $code. Inspect $logFile" }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw "Git whitespace/conflict check failed for session $Session" }
    $dirty = @(& git status --porcelain)
    if ($dirty.Count -gt 0) {
        throw "Codex session $Session finished without a clean commit. Inspect git status in $root and $logFile; do not blindly stage private files."
    }
    Write-Host "Session $Session finished successfully, working tree clean."
}
finally { Pop-Location }
