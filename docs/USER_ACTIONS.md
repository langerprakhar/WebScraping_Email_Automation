# Owner actions needed for live operation (grouped, not a repetitive Q&A)

This repo branch provides technical instructions only; Codex must implement and validate them before live use.

## Immediate security (do now)
- Rotate/revoke any Gmail app passwords / passwords, Gemini keys and other tokens historically hardcoded in this PUBLIC GitHub repo. Treat them as compromised even if later deleted from current files.
- Review exposed history and agree on a separate coordinated history-cleanup plan before any force-push. Do NOT force-rewrite history without explicit owner approval, because it can break clones/forks. Removing credentials from working tree is NOT sufficient.
- Do not run legacy SMTP scripts. No need to post literal secrets or private resume to GitHub.

## One-time local inputs
- On the owner's Windows machine, check `C:\Users\Prakhar\Music\Company-Wise-Resumes\PrakharLanger_research.pdf` exists. The repo must take it from a local path or `OUTREACH_RESUME_PATH`; never commit it.
- Put previously generated `GT_Spring_2027_TA_Contacts.csv` in `data/private` and import; it needs OSCAR and application-list revalidation. This earlier file is in user's ChatGPT file library, not the GitHub repo.
- Owner accesses the official GTA Qualtrics form and supplies an authorized export of course options or permits a local interactive read-only browser-assisted import. This tool cannot assume access to the form or claim submission.
- Provide/confirm whether College of Computing Spring 2027 GTA application has been SUBMITTED; else outbound copy must not say it was.

## Outlook
- Select intended Outlook account/profile. If Georgia Tech account: Microsoft Graph app registration/delegated Mail.ReadWrite may require admin consent; do not bypass. Login via explicit approved Microsoft OAuth UI. Never supply mail password to Codex.
- If admin consent is denied, check Classic Outlook is installed/configured and whether COM can create a verified test draft. New Outlook COM won't work.
- Approve first 1 self-addressed test draft; inspect actual Drafts and attachment. Only then approve real drafts in review CSV/UI; the engine will never auto-send.

## Clay
- Open owner's Clay workspace; run a small validated company/jobs-first table; only enrich qualified candidate rows and export to private CSV.
- If an API key is needed and allowed, enter via local secure OS credential store/.env not tracked by Git.

## Human review
- Read sampled individualized emails, proof paper references and course/role accuracy, and explicitly select approved lead IDs. Actual sending remains manual in Outlook.
- Avoid spamming professors already contacted, especially current/previous advisors; register those existing relationships and prior replies in local suppression/contact-history input.

## What is NOT required from owner
- Re-answer routine architecture prompts, manually paste the same resume bio for every lead, guess addresses, upload secrets to ChatGPT/GitHub, send 1500 near-identical emails, or manually create every draft in Outlook.
