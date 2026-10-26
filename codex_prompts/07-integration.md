# CODEX SESSION 07 — CTO INTEGRATION / COMPLETE WORKING PRODUCT

CUSTOM SUBAGENT PROFILES: Explicitly request security_qa_auditor and publication_identity_auditor (project-local .codex/agents/*.toml) for bounded read-only audits. Wait for their results. If named spawning is unsupported in the installed client, use normal explorer subagents; do not claim they ran when they did not. Parallel write access remains restricted to this session's owning agent.

Runs LAST in original feature branch feat/research-outreach-engine-2026-10-26 after Sessions 01-06 finish and commit. THIS SESSION MUST ACTUALLY MERGE BRANCHES, TEST, REPAIR, DOCUMENT. It must not stop after creating a plan.
Read AGENTS.md, docs/MASTER_V2_LOCAL_OUTLOOK.md, docs/API_CONTRACT_V2.md, all codex_prompts, and results docs.

Delegate two read-only subagents if available:
- Merge/contract auditor: inspect diffs and API boundaries, static import errors and dangerous Graph/SMTP/send instructions; produce integration fix list.
- End-to-end QA auditor: inspect all suites for unjustified xfails/mocked-as-real, wrong person/company/paper mapping, local Outlook COM failure, and high-quality message grading; produce precise issue list.
You are the single integration writer.

PROCESS:
1. Confirm branches exist: codex/gt-gra, codex/gt-gta, codex/industry-clay, codex/research-drafting, codex/outlook-local, codex/qa-security. Each must have commit(s) after Session 00 foundation. Document missing branch instead of claiming integrated. If missing, implement essential fallback yourself after assessing impact.
2. Merge in this exact deterministic order using git merge --no-ff --no-edit: codex/gt-gra; codex/gt-gta; codex/industry-clay; codex/research-drafting; codex/outlook-local; codex/qa-security. Resolve conflicts carefully; no force/reset/delete history. If uncommitted work pre-exists stop safely and report, don't stash/delete blindly.
3. Wire all campaigns and commands in shared CLI so real validated data flows to common SQLite, papers, scoring, drafts generation and approval. No fake metrics or placeholder outputs disguised as results.
4. Run python -m pip install -e ".[dev,windows]" only on Windows if optional Windows dependency available, otherwise pip install -e ".[dev]" for CI. Run pytest, ruff, import tests, type tests, and application CLI doctor/dry-runs. Fix all actual defects with repeated tests. Never loosen tests simply to make them pass.
5. Run 3 deterministic offline E2E fixtures: GRA professor+verified paper->resume evidence->review; GTA course+CRN+verified instructor->review; industry official active role+verified researcher->Clay CSV->review. Validate no Send or Graph code, persisted leads, sources, blocked cases, hashes, report.
6. Live public external discovery only within site rules and when workspace network access allows: collect small verifiable sample, record actual status and actual source URLs. Do not bypass rate limit/403. If network restricted, state 'live not tested'.
7. On actual owner's Windows machine run Outlook read-only diagnose to distinguish Classic vs New Outlook; do not create a real Outlook draft until owner approval of single test item. For absent COM, output correctly attached .eml samples under ignored folder and mark local-only. Never claim Outlook mailbox draft created unless read back from real store.
8. Create README quickstart: one-command setup, CLI examples; source coverage report; docs/RESULTS.md with real tests, real vs mocked provider counts, CSV sample, exact local paths, verified Outlook mode; docs/USER_ACTIONS.md strictly limited to credential rotation and any needed Classic Outlook/account setup, Qualtrics authorized export, Clay optional key, first-draft human approval. Do not ask many piecemeal questions.
9. Security go/no-go: hardcoded literals removed in feature branch, historical Git exposure flagged for owner rotation; no new code path can call SMTP/Send/Graph; no saved contact CSV or private PDF in Git; no unverified lead can become REVIEW_READY; no silent duplicate drafts; no unwanted mailbox message move.
10. Commit final integration 'feat(outreach): integrate research outreach V2 end to end', report commit SHA and actual test results. Leave PR #1 open as draft until reviewed. Never force merge to main or send real mails.

Definition of DONE: fully runnable offline end-to-end three campaign routes with deterministic tests, actual properly verified local COM draft save when owner authorizes (else accurate EML fallback), high-integrity sourced leads, explicit human approval gate, private data protection, and reproducible report. If pieces blocked, report exact limitation and amount actually completed; no theatrical success.
