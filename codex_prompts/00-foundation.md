# CODEX SESSION 00 — FOUNDATION / CTO / CONTRACT OWNER
Priority: FIRST, run to completion and commit BEFORE any other session starts.
Read AGENTS.md, docs/MASTER_V2_LOCAL_OUTLOOK.md, docs/API_CONTRACT_V2.md, docs/RESEARCH_SOURCES_AND_TEMPLATES.md. This is an implementation task, NOT a planning-only request.

ROLE: Senior Python systems architect. Work in feature branch feat/research-outreach-engine-2026-10-26. Own only:
src/outreach_engine/core/**, src/outreach_engine/cli.py, src/outreach_engine/__init__.py, pyproject.toml, tests/core/**, README.md, docs/API_CONTRACT_V2.md, docs/RESULTS_FOUNDATION.md.
Legacy hardcoded credentials already removed from three direct SMTP sender implementations on this feature branch, and those send functions fail closed. DO NOT execute them; audit for other secrets WITHOUT printing them. Never add Send() or SMTP to new system. No Graph/MSAL/OAuth.

IMMEDIATELY delegate two nonconflicting subagent missions if Codex collaboration tools are available:
1. explorer/security-auditor (read-only): inventory root/nested legacy scrapers, test dependencies, public secret exposures and existing reusable patterns. Return paths and remediation advice only, never print credentials.
2. contract-test reviewer (read-only): design adversarial test matrix for core models, state machine, ID/dedup, CSV injection, resume-path safety, invalid inputs, real Windows path handling. Return test cases.
DO NOT delegate concurrent edits to files you own. Implement yourself and use the reports.

DELIVERABLES:
A. Editable installable Python 3.11+ package with typed Pydantic v2 (or equivalent) models matching actual documented contract. Implement Campaign, Person, AffiliationEvidence, ContactEvidence, Publication, CourseSection, JobOpportunity, ResumeClaim, Lead, DraftProposal, Approval, MailboxDraftReceipt, ScoreBreakdown, timestamps and ID derivation. NO loose untyped bags for core.
B. Real SQLite schema + safe migrations and WAL, unique constraints, audit events, state transition finite-state machine; invalid state transitions and duplicate contact suppression fail closed.
C. Shared pluggable interfaces: DiscoveryAdapter, PublicationProvider, MatchProvider, DraftGenerator, DraftValidator, OutlookDraftAdapter, ReportProvider; dependency injection, no concrete live integrations in foundation. Freeze import paths for child branches, updating docs/API_CONTRACT_V2.md with exact Python signatures.
D. Shared resilient HTTP fetch client with robots/terms check policy hooks, per-host throttling, max-depth domain allowlists, timeouts, retries/Retry-After, non-HTML and prompt injection filtering. Use only public pages and authorized APIs. Write reproducible mocked tests, not unapproved live scraping.
E. CSV import/export with RFC 4180 quoting, utf-8-sig, Unicode support, formula-injection escaping, evidence schema, fail closed for guessed emails. Store private outputs under ignored path.
F. Minimal functional CLI (Typer/argparse) with help, doctor, run --campaign, import-gta-courses, import-clay, enrich, rank, compose, review, approve, outlook diagnose/draft/export-eml/folders, replies scan, report, and explicit dry-run. Child adapters not yet implemented should respond UNAVAILABLE / NOT_INTEGRATED, NOT success.
G. Resume reader stores claim truth bank and SHA256 of external PDF, no sharing/committing PDF. Default OUTREACH_RESUME_PATH points at user's Windows path but may not exist outside Windows. Missing file is a clear expected blocker, never invent contents.
H. Offline tests for schema, CLI, dedup, DB crashes, export injection and safety; runnable pytest; lint. Tests must not access mailbox/network.
I. README setup and RESULTS_FOUNDATION.md with exact commands and actual pass/fail, no claimed Outlook behavior.

REQUIREMENTS: Subagents should be asked to review after first implementation; use their findings to fix core defects. Do not stop after scaffolding. As a final step perform secret scan and git diff --check, stage only owned files and commit with message 'feat(outreach): build frozen core and CLI foundation'. Ensure branch is clean apart from ignored private outputs. If a tool is missing, provide mocked acceptance and record the exact blocker; don't fabricate test runs.
