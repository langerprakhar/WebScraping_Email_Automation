# Clay playbook for industry AI research outreach

Sources checked October 26, 2026:
https://university.clay.com/docs/finding-companies-and-people-in-clay
https://university.clay.com/docs/building-a-data-waterfall

Goal: qualified researcher/team contact for a real, relevant open Summer 2027 research internship, not an indiscriminate 20 emails to each firm.

1. Build a `Companies & live roles` table from OFFICIAL currently open research intern vacancies with company name, official company LinkedIn URL (more reliable than domain for Clay), location, team, role title/job ID, official URL, posted/verified timestamp, eligibility, and user-fit score. Refresh listings before drafting.
2. Before enriching people, filter the company table to verified relevant OPEN vacancies, US internship or stated alternative, and no known authorization blocker. Deduplicate brands/subsidiaries, job IDs and teams.
3. Use `Find People at These Companies` with current relevant titles (Research Scientist, Research Engineer, Research Manager, Applied Scientist, ML Research Scientist, technical recruiter for research interns, hiring manager) plus team/technical keywords. Don't start by collecting everyone at the company. Request at most 20 candidates per company for RANKING, not automatic sending.
4. Enrich a small priority subset first. Verify `current_experience` matches expected company domain, independently confirm with current official company publication/research profile when possible. Clay notes company snapshots can be stale; LinkedIn company URLs reduce wrong-domain matches.
5. Join official publications from OpenAlex/Semantic Scholar/OpenReview/DBLP/arXiv via persistent IDs to find direct paper overlap. Extract a public professional email if visibly published; do NOT treat paper's historic employer as current.
6. If no verified contact email, use a conditional business-email waterfall across provider(s) permitted by the Clay plan. Use the least costly reputable source first, stop at success, store provider and timestamp. No guessed-pattern email as VERIFIED. Respect people who opt out/no-contact.
7. Only enrich people with a current confirmed role+company match, strong publication/team overlap, and verified job match. Export CSV into `outreach import-clay --path <file>`. Direct Clay API implementation optional, only if documented and authorized.
8. Rank top 20 candidates PER company for human judgment; normally review a maximum of 2 per company over seven days to avoid multiple near-simultaneous contacts to the same team. Reach out to known/strongly relevant researchers before unrelated senior executives. A hiring manager may be more appropriate than a highly cited but unrelated scientist.
9. Keep per-row cost/provider, job evidence, paper evidence, current affiliation, professional email source, do-not-contact flag, date last verified, response status. Avoid paying repeatedly for already verified contacts.
10. Export `industry_candidates.csv`, `industry_ranked.csv`, `industry_rejected.csv`, and `industry_draft_review.csv`, all under ignored `data/private` or `data/exports`. Never commit real contact lists to public GitHub.
