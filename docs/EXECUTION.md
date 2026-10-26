# Run the implementation with Codex CLI on Windows

The branch was prepared on 2026-10-26. It contains a full implementation contract, verified reference sources, templates, and a fail-closed patch to three legacy direct-SMTP send scripts. It is NOT yet a functioning production outreach engine. Codex must implement it and produce passing tests.

## Existing local repository — PowerShell

Open PowerShell inside the existing `WebScraping_Email_Automation` repository. Keep local uncommitted work safe before switching branches.

```powershell
git fetch origin
git switch feat/research-outreach-engine-2026-10-26
codex exec --full-auto "Read AGENTS.md, docs/CODEX_MASTER_PROMPT.md, docs/RESEARCH_SOURCES_AND_TEMPLATES.md, docs/CLAY_PLAYBOOK.md, docs/OUTLOOK_SETUP.md, and docs/USER_ACTIONS.md. Execute the COMPLETE implementation end to end: refactor and build all three pipelines, implement high-integrity scrapers and publication lookup, safely rank and compose factual personalized emails, integrate verified Outlook Drafts and two reply folders, implement Clay CSV import and optional authorized adapter, test thoroughly, repair failures, and produce an evidence-backed docs/RESULTS.md. Do not stop after planning, scaffolding, or mock-only implementation. Never send real emails, request Mail.Send, fabricate papers/emails/jobs, bypass site restrictions, or run legacy SMTP scripts. Group owner-only credentials, OAuth tenant consent, and the Qualtrics export into one docs/USER_ACTIONS.md checklist. Leave all external actions dry-run until explicitly approved."
```

If there is no local checkout, clone and select the prepared branch first:
```powershell
git clone https://github.com/langerprakhar/WebScraping_Email_Automation.git
cd WebScraping_Email_Automation
git switch feat/research-outreach-engine-2026-10-26
```
Then run the Codex command above.

Codex CLI `codex exec --full-auto` is documented for autonomous workspace development; it does not imply license to email third parties. Restrict network permissions to the minimum needed, and do not pass passwords or tokens in command-line prompt text.

## One-time local inputs
Existing GTA verification CSV exported from ChatGPT: `GT_Spring_2027_TA_Contacts.csv`. Store under ignored `data/private`, then import with the implemented CLI.
Resume: `C:\Users\Prakhar\Music\Company-Wise-Resumes\PrakharLanger_research.pdf`. The file must remain local, not committed to this PUBLIC repository.

## Minimum proof for accepting code
```powershell
python -m pytest -q
python -m outreach_engine doctor
python -m outreach_engine run --campaign gt-gra --semester 2027-spring --dry-run
python -m outreach_engine run --campaign gt-gta --semester 2027-spring --dry-run
python -m outreach_engine run --campaign industry --season 2027-summer --dry-run
```
If actual installed entrypoint differs, document exact commands. Count only observed, run-specific results. No real Outlook draft creation until owner reviews and explicitly approves leads; create and read back 1 synthetic test draft before attempting a real batch. A user action is necessary for OAuth and possibly Qualtrics permissions.
