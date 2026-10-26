# NOTICE — Superseded by V2

The original October 26 V1 master document has been superseded by the owner's explicit LOCAL-OUTLOOK-ONLY decision.

Read and follow these newer authoritative files instead:
1. docs/MASTER_V2_LOCAL_OUTLOOK.md
2. docs/API_CONTRACT_V2.md
3. codex_prompts/00-foundation.md through codex_prompts/07-integration.md
4. docs/OUTLOOK_SETUP.md and docs/EXECUTION.md

Do not build Microsoft Graph, MSAL, Azure app registration, delegated permissions, SMTP, automatic sender or a workflow that claims writing local .eml files into AppData automatically creates Outlook Drafts.

The existing historical repository may contain compromised credentials; rotate/revoke them and avoid exposing values in output. The new feature branch's legacy SMTP entry points must stay fail-closed.

Use documented current Codex CLI syntax, not removed --full-auto. Owner's default email dispatch mode remains DRY_RUN and explicitly human-approved local COM draft-save only.
