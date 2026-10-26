# Run one Codex session in a Git worktree. Windows PowerShell 5.1 and PowerShell 7.
# Fix: Codex prints its startup banner to stderr. Under WinPS 5.1, 2>&1 +
# ErrorActionPreference Stop terminates on even nonfatal native stderr.
# Prefer the npm .cmd shim, temporarily use Continue for the CLI invocation,
# preserve BOTH output streams and fail on actual exit code.
# Sandbox protection: if Codex cannot write .git, commit ONLY owned changes
# from the host-side launcher after validating paths and staged content.
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
$owned = @{
    '00' = @('src/outreach_engine/core', 'src/outreach_engine/cli.py',
             'src/outreach_engine/__init__.py', 'src/outreach_engine/__main__.py',
             'src/outreach_engine/pipelines/__init__.py', 'pyproject.toml',
             'tests/core', 'README.md', 'docs/API_CONTRACT_V2.md',
             'docs/RESULTS_FOUNDATION.md')
    '01' = @('src/outreach_engine/pipelines/gt_gra', 'tests/gt_gra', 'docs/RESULTS_GRA.md')
    '02' = @('src/outreach_engine/pipelines/gt_gta', 'tests/gt_gta', 'docs/RESULTS_GTA.md')
    '03' = @('src/outreach_engine/pipelines/industry', 'tests/industry', 'docs/RESULTS_INDUSTRY.md')
    '04' = @('src/outreach_engine/research', 'src/outreach_engine/drafting',
             'tests/research', 'tests/drafting', 'docs/RESULTS_RESEARCH.md')
    '05' = @('src/outreach_engine/outlook_local', 'tests/outlook_local', 'docs/RESULTS_OUTLOOK.md')
    '06' = @('tests/acceptance', 'tests/security', 'docs/RESULTS_QA.md')
    '07' = @('src/outreach_engine', 'tests', 'docs', 'README.md', 'pyproject.toml',
             'scripts', 'AGENTS.md')
}
$codex = Get-Command codex.cmd -ErrorAction SilentlyContinue
if (-not $codex) { $codex = Get-Command codex -ErrorAction SilentlyContinue }
if (-not $codex) { throw 'Codex CLI is not installed or not on PATH.' }
$gitRoot = @(& git -C $Workspace rev-parse --show-toplevel)
if ($LASTEXITCODE -ne 0 -or $gitRoot.Count -eq 0) { throw "Not a Git worktree: $Workspace" }
$root = $gitRoot[0].Trim()
$promptPath = Join-Path $root ("codex_prompts/" + $map[$Session])
if (-not (Test-Path -LiteralPath $promptPath)) { throw "Prompt not found: $promptPath" }
$logs = Join-Path $root '.codex_runs'
New-Item -ItemType Directory -Force -Path $logs | Out-Null
$logFile = Join-Path $logs ("session-" + $Session + '.log')
$branch = (& git -C $root branch --show-current).Trim()
$headBefore = (& git -C $root rev-parse HEAD).Trim()
$beforeChanges = @(& git -C $root status --porcelain --untracked-files=all)
if ($beforeChanges.Count -ne 0) {
    throw "Session $Session cannot start in a dirty worktree. Preserve existing changes first: $root"
}
Write-Host "Starting Codex Session $Session in $root ($branch)"
Write-Host "Prompt: $promptPath"
Write-Host "Log: $logFile"
Write-Host "Codex command: $($codex.Source) exec --sandbox workspace-write -"

function Test-OwnedPath([string]$relativePath) {
    $p = $relativePath.Replace('\', '/')
    foreach ($allow in $owned[$Session]) {
        if ($p -eq $allow -or $p.StartsWith($allow + '/', [System.StringComparison]::Ordinal)) { return $true }
    }
    return $false
}
Push-Location $root
try {
    # stderr is a NORMAL log stream for Codex. Treat exit code, not any stderr
    # line, as the success/failure signal. Always restore strict error policy.
    $originalPreference = $ErrorActionPreference
    $exit = 999
    try {
        $ErrorActionPreference = 'Continue'
        Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8 |
            & $codex.Source exec --sandbox workspace-write - 2>&1 |
            ForEach-Object {
                if ($_ -is [System.Management.Automation.ErrorRecord]) {
                    $_.Exception.Message
                } else { $_ }
            } |
            Tee-Object -FilePath $logFile
        $exit = $LASTEXITCODE
    }
    finally { $ErrorActionPreference = $originalPreference }
    if ($exit -ne 0) { throw "Codex failed with exit code $exit. See $logFile" }
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'Git diff --check failed after Codex.' }
    $changed = @(& git status --porcelain --untracked-files=all)
    if ($changed.Count -gt 0) {
        $paths = @()
        foreach ($entry in $changed) {
            # Existing system owns an ASCII src/docs/tests namespace; quoted
            # pathnames are deliberately rejected rather than misparsed.
            $p = $entry.Substring(3)
            if ($p -match '^"' -or $p -match ' -> ') {
                throw "Ambiguous renamed/quoted path in git status, manual review required (Session $Session)."
            }
            $p = $p.Replace('\', '/')
            if (-not (Test-OwnedPath $p)) {
                throw "Out-of-scope file changed by Session $Session: $p. No files staged or committed."
            }
            if ($p -match '(^|/)(data|secrets|tokens|\.codex_runs)/' -or
                $p -match '(?i)\.(pdf|ost|pst|pfx|pem|key|eml|msg)$') {
                throw "Private or sensitive path cannot be auto-committed: $p"
            }
            $paths += $p
        }
        if ($paths.Count -gt 0) {
            & git add -A -- $paths
            if ($LASTEXITCODE -ne 0) { throw 'Git add of owned files failed.' }
            $stagedNames = @(& git diff --cached --name-only)
            foreach ($name in $stagedNames) {
                if (-not (Test-OwnedPath $name)) { throw "Unexpected staged file: $name" }
            }
            & git diff --cached --check
            if ($LASTEXITCODE -ne 0) { throw 'Staged diff whitespace check failed.' }
            # Check added bytes privately; NEVER print matched secret or diff.
            $patchText = (& git diff --cached --unified=0 --no-ext-diff | Out-String)
            if ($patchText -match 'AIza[A-Za-z0-9_-]{25,}' -or
                $patchText -match 'sk-[A-Za-z0-9_-]{24,}' -or
                $patchText -match 'gh[pousr]_[A-Za-z0-9]{25,}') {
                & git reset --quiet HEAD --
                throw 'Possible credential detected in staged changes. No commit created.'
            }
            & git commit -m ("feat(outreach): Codex session " + $Session + " implementation")
            if ($LASTEXITCODE -ne 0) { throw 'Host-side owned-files commit failed.' }
        }
    }
    $headAfter = (& git rev-parse HEAD).Trim()
    if ($headAfter -eq $headBefore) {
        throw "Session $Session returned successfully but made no commit or changes. Inspect $logFile."
    }
    $remaining = @(& git status --porcelain --untracked-files=all)
    if ($remaining.Count -gt 0) {
        throw "Session $Session has uncommitted/out-of-scope changes; inspect git status in $root."
    }
    Write-Host "Session $Session completed. HEAD: $headAfter (clean worktree)."
}
finally { Pop-Location }
