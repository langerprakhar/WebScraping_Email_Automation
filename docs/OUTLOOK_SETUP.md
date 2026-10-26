# Outlook Drafts and reply management — implementation contract

## Microsoft Graph preferred (new or classic Outlook)
Docs: https://learn.microsoft.com/en-us/graph/api/user-post-messages ; https://learn.microsoft.com/en-us/graph/api/user-post-mailfolders ; https://learn.microsoft.com/en-us/graph/outlook-organize-messages .
Graph delegated OAuth scopes: User.Read and Mail.ReadWrite, never Mail.Send. MSAL interactive/device-code login; may require Georgia Tech Microsoft Entra admin approval for an application. Never attempt to bypass disabled tenant consent; stop with accurate status and provide Classic Outlook fallback if available.
Discover and confirm the account mailbox UPN/address. `POST /me/messages` creates a draft by default. Include resume as Graph fileAttachment with correct MIME content type and base64 content for supported small files, or create then attach separately; verify by GET. Store immutable draft ID or provider ID, stable idempotency key (campaign/person/job-or-course/draft version). On timeout query/search existing draft first, NEVER blindly duplicate. Use delta pagination where supported for response sync and revalidate actual mailbox.
Folders: create two inbox children only if absent, exactly `GT Assistantship Replies` and `Industry Research Replies`. Split the first with GRA/GTA categories, not unnecessary extra folders. Move INCOMING verified replies conservatively using prior thread ID/sender evidence; ambiguous = review queue, no destructive mailbox action. Do not move unrelated messages. Sent status only by confirmed Sent Items or explicit owner record.
Read-only dry-run must work without any account connection. In a real pilot, create 1 synthetic/self-addressed draft, read it back, verify attachment, subject, recipient, then inspect manually before batching.

## Classic Outlook COM conditional fallback
Microsoft says new Outlook for Windows does not support COM/VSTO:
https://learn.microsoft.com/en-us/office/dev/add-ins/outlook/one-outlook
Classic Outlook supports CreateItem(olMailItem) and MailItem.Save:
https://learn.microsoft.com/en-us/office/vba/api/outlook.application.createitem
https://learn.microsoft.com/en-us/office/vba/api/outlook.mailitem.save
On Windows with Classic Outlook active and explicitly selected owner account, using `win32com.client.Dispatch("Outlook.Application")`, `CreateItem(0)`, `To`, `Subject`, `Body`, `Attachments.Add`, `Save` creates a draft. Confirm account and folder through namespace before attempting 1 single draft. Never call .Send() or fill a BCC list. COM save may use default account; validate actual store; don't assume the sender.
Do not write to or attempt to mutate Outlook OST/PST/local cache. Files do not become synchronized drafts by appearing in AppData. `.eml` generation is a separate portable archival/review output, not the Outlook inbox.
Provide clear `doctor outlook` probes to identify (1) account, (2) Outlook flavor, (3) Graph permission available, (4) COM installed, (5) whether default drafts store is appropriate, without creating real data.

## Explicit operational guard
`outreach outlook-drafts --approved-only --limit 3` is the ONLY action allowed to create mailbox drafts, after approvals. It still may not send. If an external action is unavailable, report BLOCKED with what owner action is needed, do not falsely mark delivered.
