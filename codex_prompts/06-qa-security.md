# CODEX SESSION 06 — ADVERSARIAL ACCEPTANCE TESTS + RED TEAM

CUSTOM SUBAGENT PROFILES: Explicitly request security_qa_auditor and outlook_com_auditor (project-local .codex/agents/*.toml) for bounded read-only audits. Wait for their results. If named spawning is unsupported in the installed client, use normal explorer subagents; do not claim they ran when they did not. Parallel write access remains restricted to this session's owning agent.

Requires Session 00 foundation. Worktree branch codex/qa-security. Read full V2 contract and API. This branch adds TESTS only; no production modifications or fake green tests.

Delegate two read-only subagents:
- Privacy and outreach correctness adversary: inspect API contract and generated integration modules only insofar as accessible in your branch. Design tests for credential leaks, public email misuse, mass spam patterns, poor source provenance, unsubscribe/decline, fake affiliations/papers, national eligibility.
- Windows COM and multi-session integration adversary: test API edge contracts, mocked STA/COM, only new Outlook, retry duplicates, unknown store, stale leads, contradictory campaigns, forbidden SMTP/Graph/send symbols, wrong drafts folders.

Own tests/acceptance/**, tests/security/**, docs/RESULTS_QA.md. Build:
1. Acceptance fixture pack covering 3 example campaigns using fictional recipients/domains reserved for testing (example.org/.test) and fixture PDF with no private user resume.
2. Every 'verified person' requires confirmed public professional source URL, source date, current affiliation, precise person/email bind. Missing any hard field should fail drafting; nonhuman uncertain = review.
3. Publication disambiguation tests: same name across colleges/companies, two same-year papers, outdated affiliation in paper PDF, DOI mismatch, abstract unsupported paraphrase.
4. GTA exact course+semester+CRN join and false form-submission claims; GTRI citizenship rule; job listing stale/expired; Cloud career API 429/403/robots denial; Clay provider stale info.
5. COM no Send(), no SMTP, no Graph, no Mail.Send scopes, no mailbox mutations in dry-run, one-account verified draft ID, one attachment SHA256, no phantom status, EML not equal Outlook Draft, no OST/PST injection. Static checks can examine new src/outreach_engine only, avoid legacy historical bytes except explicit secret remediation detection; don't print secrets.
6. Prompt injection through PDF or page (instructions to remove validations and send), CSV formulas, SQL injection, path traversal, arbitrary file read, concurrency/resume unique contact.
7. Test failure signal required; do NOT xfail tests merely to make CI green. If integration targets absent on this branch, build test shims with clear skip reason and report pending integration; test suite becomes fully active in Session 07 after branches merge.
8. Strict evidence report with proven failures/open issues and exact test counts.

Exit: run available tests, commit owned files 'test(outreach): add acceptance and safety gates'. Do not invent successes.
