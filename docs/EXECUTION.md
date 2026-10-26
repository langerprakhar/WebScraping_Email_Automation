# ONE-COMMAND LOCAL Codex V2 BUILD (PowerShell, Windows)

Eight sessions: 00 foundation first; 01-06 in isolated Git worktrees, in waves of three by default; 07 merger/QA at end. Each session itself requests two bounded read-heavy Codex subagents. Does NOT make real mailbox drafts or send messages without owner explicit later action.

First install/update Git, Python 3.11+ and Codex CLI, and sign in interactively if not already done. Codex CLI 0.164.0 or newer recommended, verify codex --version. These commands operate ONLY on the owner's local machine.

## If existing repo is already cloned:
Open PowerShell in WebScraping_Email_Automation. Ensure current worktree changes are committed or kept separately; the launcher intentionally rejects dirty trees rather than losing work.
    git fetch origin
    git switch feat/research-outreach-engine-2026-10-26
    .\scripts\build_all_codex.ps1 -MaxParallel 3

## If the repo is not cloned:
    git clone https://github.com/langerprakhar/WebScraping_Email_Automation.git
    cd WebScraping_Email_Automation
    git switch feat/research-outreach-engine-2026-10-26
    .\scripts\build_all_codex.ps1 -MaxParallel 3

Run the .ps1 file in a PowerShell session that permits local script execution. If policy restricts scripts, do NOT bypass institutional restrictions; use the manual individual Codex session commands below.

## How the orchestrator works
1. Session 00 runs directly in feature branch and MUST produce a real typed core package, CI tests, stable API, CLI, and git commit.
2. It then creates sibling local worktrees in ../Outreach-V2-Worktrees, based on the SAME foundation commit.
3. Runs separate processes for 01-GRA, 02-GTA, 03-Industry (wave 1), 04-Research+Drafting, 05-Outlook COM, 06-QA (wave 2); switch -MaxParallel 6 only if capacity allows; 3 is safer. Windows PowerShell 5.1 native stderr is handled without treating Codex startup messages as fatal errors.
4. Each runs a specialized prompt via: Get-Content -Raw -Encoding UTF8 codex_prompts/NN-file.md | codex exec --sandbox workspace-write -
5. Verifies each process exit code; if Codex's sandbox cannot write .git, host PowerShell stages ONLY session-owned files after path/secret checks and commits them. The HOST launcher then merges the six completed branches into feature branch in a deterministic order, without force/reset, BEFORE starting Session 07. Session 07 verifies merges, repairs integration, runs offline tests, and reports actual status. It does NOT push/merge PR #1 to main, create live Outlook drafts, or send anyone mail.
6. Logs reside under ignored .codex_runs/session-XX.log within each worktree; complete user-action and test reports in docs/RESULTS.md and docs/RESULTS_*.md.

## To run each Codex session manually (if automatic orchestrator is blocked)
From its appropriate worktree, use:
    Get-Content -Raw -Encoding UTF8 .\codex_prompts\00-foundation.md | codex exec --sandbox workspace-write -
For other sessions change 00-foundation.md to 01-gt-gra.md, 02-gt-gta.md, 03-industry-clay.md, 04-research-drafting.md, 05-outlook-local.md, 06-qa-security.md, or 07-integration.md. Set up worktrees according to docs/API_CONTRACT_V2.md. **Do not run 01-06 before 00 has committed its frozen API.**

## Source/quality acceptance after integration
    python -m pip install -e ".[dev]"
    python -m pytest -q
    python -m outreach_engine doctor
    python -m outreach_engine run --campaign gt-gra --semester 2027-spring --dry-run
    python -m outreach_engine run --campaign gt-gta --semester 2027-spring --dry-run
    python -m outreach_engine run --campaign industry --season 2027-summer --dry-run
Actual CLI may use an installed outreach command; see README. These commands are a required *target contract*, not claimed to exist yet.

## Preview and local outlook test (after code ships)
1. Set OUTREACH_RESUME_PATH and, for GTA, privately import GT_Spring_2027_TA_Contacts.csv.
2. Review generated CSV/HTML and approve exact chosen IDs, never approve the full discovered set unseen.
3. Run outreach outlook diagnose: only Classic Outlook with correct account/store allows direct mailbox Drafts persistence.
4. Only after approval create ONE self-addressed test message with attachment and verify it appears in correct mailbox's Drafts. Never claim success from a COM mock. New Outlook-only -> .eml fallback, not automatically synced.
5. After test approval, create individually reviewed genuine message drafts; owner sends manually in Outlook.

Important: Previous Oct 26 V1 docs referenced --full-auto and Graph-first; both are superseded. Current Codex noninteractive documentation uses --sandbox workspace-write instead. No --yolo.
