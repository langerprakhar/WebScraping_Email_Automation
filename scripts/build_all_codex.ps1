# Guarded multi-session orchestration: core first, six isolated worker worktrees, final integration.
# Usage (after git fetch && git switch feature):
#     .\scripts\build_all_codex.ps1 -MaxParallel 3
# Requires Windows PowerShell 5.1+ or PowerShell 7, git and signed-in Codex CLI.
# Each Codex worker MUST commit its changes. Never force-reset or stash a user's changes.
[CmdletBinding()]
param(
    [ValidateRange(1, 6)][int]$MaxParallel = 3,
    [switch]$SkipFoundation
)
$ErrorActionPreference = 'Stop'
$rootRaw = (& git rev-parse --show-toplevel)
if ($LASTEXITCODE -ne 0 -or -not $rootRaw) { throw 'Open PowerShell inside a Git checkout first.' }
$root = ($rootRaw | Select-Object -First 1).Trim()
$feature = 'feat/research-outreach-engine-2026-10-26'
$existing = @(& git -C $root status --porcelain)
if ($existing.Count -gt 0) { throw 'Working tree has local edits. Commit/move them before launching sessions; no data will be discarded.' }
$cur = (& git -C $root branch --show-current).Trim()
if ($cur -ne $feature) { throw "Switch to $feature (git fetch origin; git switch $feature) before running." }
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw 'Codex CLI missing. Install/sign in and rerun.' }
$runner = Join-Path $root 'scripts/run_codex_session.ps1'
if (-not (Test-Path -LiteralPath $runner)) { throw "Missing worker script: $runner" }

if (-not $SkipFoundation) {
    Write-Host '[0/7] Building mother pipeline foundation...'
    & $runner -Session '00' -Workspace $root
    if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw 'Foundation failed. Inspect session-00.log.' }
}
$baseRaw = (& git -C $root rev-parse HEAD)
if ($LASTEXITCODE -ne 0) { throw 'Cannot determine foundation commit.' }
$base = ($baseRaw | Select-Object -First 1).Trim()
if (-not (Test-Path -LiteralPath (Join-Path $root 'src/outreach_engine/core'))) {
    throw 'Foundation did not build src/outreach_engine/core. Parallel sessions were NOT started.'
}
$specs = @(
    @{ Id = '01'; Name = 'gt-gra'; Branch = 'codex/gt-gra' },
    @{ Id = '02'; Name = 'gt-gta'; Branch = 'codex/gt-gta' },
    @{ Id = '03'; Name = 'industry-clay'; Branch = 'codex/industry-clay' },
    @{ Id = '04'; Name = 'research-drafting'; Branch = 'codex/research-drafting' },
    @{ Id = '05'; Name = 'outlook-local'; Branch = 'codex/outlook-local' },
    @{ Id = '06'; Name = 'qa-security'; Branch = 'codex/qa-security' }
)
$parent = Split-Path $root -Parent
$workRoot = Join-Path $parent 'Outreach-V2-Worktrees'
New-Item -ItemType Directory -Force -Path $workRoot | Out-Null
$psBin = (Get-Process -Id $PID).Path
if (-not $psBin) { throw 'Could not determine PowerShell executable for worker processes.' }
foreach ($spec in $specs) {
    $path = Join-Path $workRoot $spec.Name
    $spec.Path = $path
    if (-not (Test-Path -LiteralPath $path)) {
        & git -C $root show-ref --verify --quiet ('refs/heads/' + $spec.Branch)
        if ($LASTEXITCODE -eq 0) {
            & git -C $root worktree add $path $spec.Branch
        }
        else {
            & git -C $root worktree add -b $spec.Branch $path $base
        }
        if ($LASTEXITCODE -ne 0) { throw "Could not create worktree for $($spec.Name)" }
    }
    $actual = (& git -C $path branch --show-current).Trim()
    if ($actual -ne $spec.Branch) { throw "Wrong worktree branch in $path. Expected $($spec.Branch), got $actual" }
    $ownDirty = @(& git -C $path status --porcelain)
    if ($ownDirty.Count -gt 0) { throw "Worktree has uncommitted changes: $path. No reset performed." }
}
Write-Host "Foundation commit: $base. Prepared $($specs.Count) isolated worktrees."

for ($i = 0; $i -lt $specs.Count; $i += $MaxParallel) {
    $upper = [Math]::Min($i + $MaxParallel - 1, $specs.Count - 1)
    $batch = @($specs[$i..$upper])
    $running = @()
    foreach ($spec in $batch) {
        Write-Host "Launching Codex session $($spec.Id) in $($spec.Path)"
        $args = '-NoProfile -ExecutionPolicy Bypass -File "' + $runner + '" -Session ' + $spec.Id + ' -Workspace "' + $spec.Path + '"'
        $process = Start-Process -FilePath $psBin -ArgumentList $args -PassThru -WorkingDirectory $spec.Path
        $running += [pscustomobject]@{ Process = $process; Spec = $spec }
    }
    $failures = @()
    foreach ($item in $running) {
        $item.Process.WaitForExit()
        $item.Process.Refresh()
        if ($item.Process.ExitCode -ne 0) { $failures += "$($item.Spec.Id): exit $($item.Process.ExitCode)" }
    }
    if ($failures.Count -gt 0) {
        throw ("One or more child sessions failed: " + ($failures -join ', ') + '. See each child worktree .codex_runs/session-XX.log. No merge attempted.')
    }
}
# Git metadata is not reliably writable inside the Codex workspace-write sandbox.
# Merge each completed child branch here, in the trusted host PowerShell process.
# Distinct session ownership makes these merges normally conflict-free. If a
# conflict occurs, fail safely for explicit resolution; never reset/force.
Write-Host '[7/7] Merging completed child branches in the host process...'
foreach ($spec in $specs) {
    $current = @(& git -C $root status --porcelain --untracked-files=all)
    if ($current.Count -gt 0) { throw 'Integration tree has uncommitted changes. Resolve before merging.' }
    Write-Host "Merging $($spec.Branch)"
    & git -C $root merge --no-ff --no-edit $spec.Branch
    if ($LASTEXITCODE -ne 0) {
        throw "Merge conflict/error for $($spec.Branch). Review git status in $root; no force/reset performed. Do not rerun launcher until resolved."
    }
}
Write-Host '[7/7] All six branches merged; Codex integration and full test repair next...'
& $runner -Session '07' -Workspace $root
if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) { throw 'Integration failed; inspect session-07.log.' }
Write-Host 'Build orchestration completed. Review docs/RESULTS.md and the draft PR. No emails were sent.'
