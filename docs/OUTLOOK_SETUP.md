# LOCAL Outlook Drafts V2: no Graph, no OAuth, no SMTP

Reference docs:
Microsoft: https://learn.microsoft.com/en-us/office/dev/add-ins/outlook/one-outlook (New Outlook does not support COM/VSTO)
Microsoft: https://learn.microsoft.com/en-us/office/vba/api/outlook.mailitem.save (MailItem.Save)
Microsoft: https://learn.microsoft.com/en-us/office/vba/api/outlook.application.createitem (classic MailItem)
Microsoft: https://learn.microsoft.com/en-us/office/vba/api/outlook.mailitem.sendusingaccount (account selection)
Microsoft: https://learn.microsoft.com/en-us/office/client-developer/outlook/selecting-an-api-or-technology-for-developing-solutions-for-outlook (STA / local machine).

## Must-have runtime
- Windows on the user's interactive logged-in desktop.
- Classic Outlook desktop, already installed and signed in to the intended mail account. Outlook policy can restrict automation and those restrictions must be respected.
- Python 3.11+ and pywin32 optional Windows dependency. No need to expose/send Outlook password to the application or Codex.
- Test platform capabilities via outreach outlook diagnose, which MUST NOT create mail or folders.
- A mailbox may have multiple accounts/stores. Require explicit intended account; verify its SMTP address, stable StoreID, and actual Drafts folder; do not assume the first default account.
- MailItem.Save() saves a new MailItem to the default item-type folder; if the account's folder needs another location, explicitly Move() to correct Drafts store and verify. Outlook COM operates on STA; do not call from a background worker thread/service/WSL. Never call MailItem.Send().

## Approved draft flow
1. Confirm verified contact email, recipient person/current employer, campaign, cited verified paper/course/job, reviewed exact message SHA, resume exists and compute local SHA256.
2. User explicitly approves named draft IDs. Before any real run, request owner approval for ONE self-addressed test draft. No authorization, no mailbox writes.
3. Create Classic Outlook COM MailItem: subject, To, body, attachment. Save() and ensure actual item belongs to selected account Drafts folder. Read back item EntryID+StoreID, recipient/subject/body, attachment filename and metadata; if mismatch, keep NEEDS_REVIEW and report failure, not success. Detect preexisting IDempotency marker after timeout before retry.
4. Exactly two optional Inbox subfolders: GT Assistantship Replies and Industry Research Replies; create only on explicit owner command, existing folder reuse, never duplicate.
5. Conservative read-only scan Sent Items and Inbox to identify actual sent/replied status; do not infer sending from Draft. Ambiguous messages human review. Moving incoming replies between folders is opt-in only.
6. All live mail operations remain local/interactive; no Graph/MSAL/SMTP/sending.

## If only New Outlook is installed, or COM blocked
Export RFC-compliant .eml files under data/drafts/[campaign], one per APPROVED recipient. Include To, Subject, text/plain, attached PDF (application/pdf) and audit manifest. Mark EML_ONLY_EXPORTED, not OUTLOOK_DRAFT_SAVED. Inform owner that .eml files require manual opening/import and explicit saving/sending. The application may offer a review link to .eml but may not claim they are synced to mailbox.
NEVER write .ost/.pst or Outlook cache directory; there is no supported file drop that causes an .eml to become a synchronized Draft automatically.
