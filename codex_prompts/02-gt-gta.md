# CODEX SESSION 02 — GT GTA COURSE / INSTRUCTOR INTELLIGENCE

CUSTOM SUBAGENT PROFILES: Explicitly request ta_course_auditor and security_qa_auditor (project-local .codex/agents/*.toml) for bounded read-only audits. Wait for their results. If named spawning is unsupported in the installed client, use normal explorer subagents; do not claim they ran when they did not. Parallel write access remains restricted to this session's owning agent.

Requires committed Session 00 foundation. Work ONLY in assigned worktree branch codex/gt-gta.
Read AGENTS.md, docs/MASTER_V2_LOCAL_OUTLOOK.md, docs/API_CONTRACT_V2.md and existing private-input guidelines. Do not change shared core or other child modules.

Spawn two bounded read-only subagents if available:
- Course and Qualtrics fact-finder: inspect legitimate GT GTA application route, public course lists/OSCAR entry points; design authorized course export/import with no logins bypassed and no false application status.
- Subject qualification/negative-case auditor: verify rank features for GTA, course/instructor/section exact joins, potential false teaching claims, graduate vs undergraduate sections, term mismatch and duplications.

Own src/outreach_engine/pipelines/gt_gta/**, tests/gt_gta/**, docs/RESULTS_GTA.md. Build:
1. Import existing owner's GT_Spring_2027_TA_Contacts.csv with fields index, Priority, Dropdown course code, Course title, Spring 2027 Atlanta instructor(s), Published contact email(s) / review, Atlanta section CRN(s), Spring 2027 result, Verified all contact emails?, Outreach sent?, OSCAR verified?. CSV is on owner's machine if manually placed under ignored data/private/. Handle field newline/semicolon/multi-instructor variants.
2. Official Qualtrics link is https://gatech.co1.qualtrics.com/jfe/form/SV_8ofvtf1XAwJnkMu. Allow a manual authorized dropdown CSV export or visible-page browser-assisted import in attended local session. Do NOT automatically submit form; NEVER bypass authentication, CAPTCHA or survey protection. Prior sheet is preliminary, not proof submitted.
3. Course->term->section/CRN->published instructor mapping through official OSCAR/catalog page when publicly accessible. Mark UNVERIFIED on stale or missing terms, multiple sections, cross-listing mismatches. Distinguish coordinator vs instructor.
4. Rank by documented user background, prior verified coursework/grades and subject competence; do not infer completed current class or TA history. Match AI, ML, NLP, DL, LLM, Data Systems and systems courses. Do not use unrelated paper summary for GTA template.
5. Return qualifying GTA leads with course evidence for research/drafting pipeline, including official process notes. Suppress repetitive contacts to course team and users already emailed.
6. Tests: malformed CSV, CRNs numeric/quoted/leading zeros, repeated instructor, email "Published contact email(s)/review" field with multiple name/email pairs, absent form import, false survey submitted, current semester mistaken for Spring 2027.
7. Report source counts, import counts, course match confidence, candidate GTA leads, defects/review blockers. Use real observed data only.

Exit: run tests, commit only owned directories and docs with 'feat(outreach): implement Spring 2027 GTA course intelligence'. Do not send or create drafts.
