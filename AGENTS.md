# AGENTS.md — Research Outreach Engine V2 (LOCAL OUTLOOK ONLY)

Authoritative contract: docs/MASTER_V2_LOCAL_OUTLOOK.md. Read it and docs/API_CONTRACT_V2.md in full before writing code. This supersedes former Graph-first, SMTP, and removed --full-auto guidance in the original project.

MISSION: Build one high-integrity mother research outreach engine with three child pipelines: Georgia Tech GRA Spring 2027, Georgia Tech GTA Spring 2027, and industry Summer 2027 AI/ML research internships. Optimize legitimate qualified replies, not raw scraped addresses. Offline/dry-run preview must work without credentials.

IMPLEMENTATION: A sequence of isolated Codex CLI sessions specified in codex_prompts/00-foundation.md through 07-integration.md. Custom bounded auditing subagents in .codex/agents/*.toml. The mother-pipeline shared core is built and COMMITTED in Session 00 first; child sessions 01-06 branch off it, use distinct Git worktrees and edit ONLY their path ownership in docs/API_CONTRACT_V2.md; Session 07 merges, tests, repairs, and reports. Use subagents for read-only exploration and independent review only; no simultaneous writes to shared modules.

LOCAL OUTLOOK IS FINAL:
- NO Microsoft Graph, MSAL, Azure registration, Outlook connector, SMTP, Mail.Send, or any programmatic sending feature.
- Classic Outlook for Windows COM via pywin32 on interactive Windows desktop, with exactly verified mailbox/store+Drafts folder, MailItem.Save(), attachment verification, idempotence and explicit human-approved drafts. Never call Send().
- Fallback: private .eml files with correctly attached resume. These are NOT Outlook mailbox drafts until manually imported and saved. New Outlook does not support classic COM.
- Build exactly two optional Inbox reply folders: GT Assistantship Replies, Industry Research Replies. Read-only conservative reply scan first; no unapproved moving/deletion.

PUBLIC REPOSITORY SECURITY WARNING: Historical SMTP/Gemini files contain previously hardcoded credential-like values, exposed in original default main and Git history. Feature branch already disabled three SMTP functions and removed current hardcoded values in those scripts. DO NOT execute old email scripts, print historic secrets, commit new credentials, or force-rewrite history. Owner should rotate/revoke exposed credentials promptly. Resume/contact CSVs are LOCAL and ignored by Git.

Owner resume external file: C:\Users\Prakhar\Music\Company-Wise-Resumes\PrakharLanger_research.pdf. Never commit PDF or source contact lists. Spring 2027 GTA prior CSV is a private input and must be reverified. Qualtrics is NOT presumed completed.

Use only publicly listed professional contacts pertinent to relevant outreach, verify person/current appointment/cited publications/current openings, respect robots/usage rules and opt-outs. Never invent names, citations, grades, hiring eligibility, emails, results, consent, or Outlook Draft saved status. Explicit review and approval gate required per recipient; never mass send or use BCC.

Codex supported CLI pattern: Get-Content -Raw codex_prompts/NN-name.md | codex exec --sandbox workspace-write -
Do NOT use removed --full-auto or --yolo. Secure session scripts: scripts/run_codex_session.ps1 and scripts/build_all_codex.ps1.

Finish each session with code, tests and factual report, then commit only owned safe changes on its own branch. If live Outlook isn't actually tested with owner authorization, label it UNVERIFIED and demonstrate mocked COM plus EML fallback instead.
