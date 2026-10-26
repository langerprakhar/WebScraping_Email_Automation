# One short owner-action checklist for production use (Local Outlook V2)

Codex must implement and test the offline engine WITHOUT asking for a sequence of small permissions. These few dependencies cannot be bypassed by automation:

1. SECURITY NOW: revoke/rotate any previously hardcoded public-repo Gmail app password, Gemini API key and other exposed secrets; original Git history/default main retains disclosure even after feature branch cleanup. Do not paste live secrets into ChatGPT/GitHub. Separate owner-approved history cleanup is optional later, not a substitute for revocation.
2. Resume: local file should exist at C:\Users\Prakhar\Music\Company-Wise-Resumes\PrakharLanger_research.pdf (or set OUTREACH_RESUME_PATH). Do not copy this PDF into public git. Use runtime only.
3. GTA: copy earlier GT_Spring_2027_TA_Contacts.csv into ignored local data/private/; verify current authorized options in https://gatech.co1.qualtrics.com/jfe/form/SV_8ofvtf1XAwJnkMu and whether official GTA form is SUBMITTED. Do not claim submission otherwise.
4. Outlook: choose selected account/profile in CLASSIC Outlook on Windows. No Graph/OAuth/Azure app consent required. If ONLY New Outlook exists, the system uses .eml export with manual import/open/save. If Classic Outlook is policy-blocked for COM, obey restriction.
5. Human review: review first test email, approve exact IDs before any COM draft persistence. The engine does not auto-send. Create the two separate reply folders only after you approve that local mailbox operation.
6. Clay: optionally provide documented workspace/API access or privately export company/people CSV. Enrich only qualified companies with current verified relevant jobs. No need to connect Clay for GT GRA/GTA.

User should NOT have to re-enter resume information per recipient, manually look up each publication, manually hand-create hundreds of emails or answer architecture questions. Output exact blockers once in a single report.
