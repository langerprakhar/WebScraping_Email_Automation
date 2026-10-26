# CODEX SESSION 01 — GT GRA DISCOVERY / FUNDING RELEVANCE
Requires committed Session 00 foundation. Work ONLY in assigned worktree on branch codex/gt-gra.
Read AGENTS.md, docs/MASTER_V2_LOCAL_OUTLOOK.md, docs/API_CONTRACT_V2.md, docs/RESEARCH_SOURCES_AND_TEMPLATES.md and the actual core models. Do not edit core API contracts or files owned by other sessions.

If available, spawn two bounded subagents for READ-ONLY independent jobs:
- GT official-site atlas agent: map institutional/departmental/faculty/lab entry points across ALL Georgia Tech colleges, and check robots/rate-limit obligations; return authoritative URLs, cross-domain issues, nonfaculty filters.
- GRA relevance / eligibility red-teamer: design cases for emeritus profs, adjuncts, lab staff vs PIs, joint appointments, misleading open positions, GTRI citizenship/clearance requirements and prior-advisor contact histories; return tests.
Wait for their findings and build implementation yourself.

Own src/outreach_engine/pipelines/gt_gra/**, tests/gt_gra/**, docs/RESULTS_GRA.md. Implement the following end to end:
1. GT seed discovery registry: ML@GT cross-college directory, CoC schools CS/IC/CSE, ECE, biomedical, ISyE, math, mechanics, biology, chemical engineering, public policy, Scheller and institutes. Follow official site directories/sitemaps and approved links only, with depth, rate and domain constraints. Do not claim 'all sites' without a measurable coverage report.
2. Extract current faculty + PI roles, research areas, active lab URLs, professional public emails visibly published at official pages, employer/site provenance, recency, explicit labs hiring or funded spots. Never guess an address, never imply funding without evidence.
3. Extract independent affiliations/cross-appointments, disambiguate homonyms; no accidental duplicate records. Ensure faculty with relevant NLP, ML systems, applied ML, healthcare AI, long-running agents, RAG, agent eval, database systems are prioritized. Lab/hiring signals should boost rather than substitute for accurate research fit.
4. Add optional GTRI current-job adapter with role eligibility constraint flags. Citizenship/clearance blocker must stop outreach recommendations to ineligible person; unknown -> human review.
5. Feed VERIFIED GRA leads and evidence to core interface and general research/drafting module to be wired at integration. Separate discovery from messaging; no emails are sent or drafted in mailbox here.
6. Offline fixtures with official-like HTML, joint appointments, no email, retiree, lab site change, redirected site, 429/403/robots, stale pages, namesakes, partial crawl, GTRI eligibility.
7. Source coverage report: number of GT departments seeded, pages successfully parsed, people with verified work email, leads with strong relevant fit, uncovered/blocked sites, publication-ready cases. Never invent live counts. If safe approved public requests available, perform small crawl and log actual URLs/results; otherwise report mocked tests.

Exit: pytest tests/gt_gra -q, static checks, commit only owned files 'feat(outreach): implement Georgia Tech GRA discovery'. Report commit and compatibility issues as text, do not modify shared core files.
