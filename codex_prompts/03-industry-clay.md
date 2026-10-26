# CODEX SESSION 03 — INDUSTRY RESEARCH JOBS, RESEARCHER DISCOVERY AND CLAY

CUSTOM SUBAGENT PROFILES: Explicitly request industry_jobs_auditor and publication_identity_auditor (project-local .codex/agents/*.toml) for bounded read-only audits. Wait for their results. If named spawning is unsupported in the installed client, use normal explorer subagents; do not claim they ran when they did not. Parallel write access remains restricted to this session's owning agent.

Requires Session 00 foundation. Worktree branch codex/industry-clay. No shared-core modifications.
Read AGENTS.md, docs/MASTER_V2_LOCAL_OUTLOOK.md, docs/API_CONTRACT_V2.md, docs/CLAY_PLAYBOOK.md.

Spawn two read-only research/review subagents if available:
- Official-jobs provider mapper: investigate documented official ATS/company jobs pages and APIs for Ashby, Lever, Greenhouse, Workday (only when public and terms allow), research labs, and research internship titles for Summer 2027; flag stale/offseason listings.
- Publications/team mapper: map how company lab/team pages and paper author current affiliations can connect to jobs; review Clay CSV columns, credit-efficient waterfall and opt-out behavior.

Own src/outreach_engine/pipelines/industry/**, tests/industry/**, docs/RESULTS_INDUSTRY.md. Build:
1. Configurable company registry including Google Research/DeepMind, Microsoft Research, Meta FAIR, Amazon/AWS AGI, Apple ML, NVIDIA, Adobe Research, IBM, Salesforce AI Research, Databricks, Snowflake, plus other research-active companies only where career evidence exists. These are DISCOVERY targets, NEVER claim open role unless official page says open.
2. Search public official career listings first. Normalize title, company, team, job URL/ID, dates, season, US office, international-student authorization/citizenship/clearance, link health, status and checked_at, with freshness TTL 48 hours before draft approval. Suppress closed/unverified/ambiguous listings.
3. Search company scientific publication pages and recognized proceedings APIs to identify current relevant researchers; reconcile current company and current professional email using official current profile/Clay. Paper-specific historic email is insufficient proof of present employer. Keep up to 20 people per company for ranking, not 20 automatic drafts. Prefer team-associated staff to executives.
4. Clay integration MVP is robust CSV import/export and data enrichment provenance normalization; optional official API adapter only if owner provides allowed credentials. Keep Clay credits low by enriching qualifying leads only after job/company research fit. No behind-login LinkedIn scraping.
5. Score job fit, research overlap, contact identity confidence and likelihood the person knows the team, not prestige alone. No fabricated referral.
6. Tests: official job expired, title irrelevant, season incorrect, citizenship blocker, author employed elsewhere, outdated Clay employer, aliases/duplicate subsidiaries, ambiguous work email, multiple teams, stale job, CSV formula injection, quotas. Return review-only eligible leads to shared modules.
7. Actual useful output: source-backed sample company/job/person records if accessible (avoid invented open roles); export sample under ignored private paths.

Exit: run tests, commit only owned files 'feat(outreach): implement industry research and Clay pipeline'. Do not send or create Outlook drafts.
