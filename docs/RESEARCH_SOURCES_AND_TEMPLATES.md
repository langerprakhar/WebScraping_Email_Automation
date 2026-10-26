# Research sources, outreach copy, and hard validation rules (verified Oct 26, 2026)

## Official Georgia Tech sources
- Georgia Tech MS CSE FAQ (formal GTA survey route + contacting professors about GRAs): https://cse.gatech.edu/current-student-faqs
- Graduate Education GRAs/GTAs funding and assistantship eligibility: https://grad.gatech.edu/paying-for-grad-school
- Graduate student policy, including tuition waiver distinction: https://policylibrary.gatech.edu/academic-affairs/graduate-student-enrollment-and-employment
- ML@GT directory (all six colleges): https://ml.gatech.edu/people and https://ml.gatech.edu/people/faculty
- ML PhD program faculty directory: https://www.ml.gatech.edu/ml-phd-program-faculty (filter out non-current profiles)
- CoC, CS, CSE, IC, ECE, ISyE, biomedical, Math, ME, ChBE, Biology, Scheller and interdisciplinary labs: discover canonical people pages by official GT navigation. Do NOT pretend this list covers all GT websites; implement depth-limited, domain-allowlisted index expansion.
- GTRI jobs: https://careers.gtri.gatech.edu/jobs/search ; note that some relevant AI/ML GRAs explicitly require U.S. citizenship, which must block recommendations for an ineligible applicant.
- GTA user-supplied form: https://gatech.co1.qualtrics.com/jfe/form/SV_8ofvtf1XAwJnkMu . As of 2026-10-26, programmatic retrieval did not expose form options. User-side authorized import is required. Use prior `GT_Spring_2027_TA_Contacts.csv` as fallback PRE-VERIFICATION; it does not prove application status or final instructor assignments.

## Academic metadata/API strategy
- OpenAlex docs: https://help.openalex.org/api/ and https://help.openalex.org/api/llm-quick-reference/
- OpenAlex institution and ORCID resolved authors; do not match by name alone.
- OpenAlex works supports author.id, institutions.id, dates, and cited_by_count; retrieve top-cited separately from recent; cite DOI/canonical source. Cache TTL and handle evolving quotas/auth.
- Semantic Scholar API: https://api.semanticscholar.org/api-docs/ (author/paper IDs, abstracts, citations). Handle API key and 429.
- Crossref, DBLP, arXiv, Europe PMC, PubMed and OpenReview official APIs for DOI/bibliographic metadata, subject-specific validation, open-access abstracts/full text where permitted. Avoid unauthorized Google Scholar scraping.
- Papers/affiliations are historical; corroborate with current faculty/company profile. Paper emails are candidates only until current employer and professional email identity are confirmed.

## Teaching, GRA and networking source rationale
- UW Office of Undergraduate Research: https://www.washington.edu/undergradresearch/how-to-reach-out-to-a-mentor/ (brief introduction + why research connects + small meeting ask; follow up after ~7 business days)
- Tufts Career Center: https://careers.tufts.edu/blog/2025/09/16/contacting-faculty-about-research-opportunities/ (specific current research paper and lab's outreach directions)
- University of Memphis: https://www.memphis.edu/ugresearch/students/email.php (avoid bulk obvious templates)
- University of Illinois URSA: https://ursa.grainger.illinois.edu/emailing-professors/ (brief, specific, relevant qualifications)
These are qualitative writing recommendations, not proof of a numerical reply-rate lift.

## User's evidence bank (from their provided 1-page research resume; verify current version at runtime)
Current GT MSCS AI (Aug 2026-May 2028); D2I lab under Kexin Rong and Sham Navathe; MIMIC-IV ICU diagnostics at 6/12/24h; five forecast methods and candidate-recall 0.874 initial pilot. NYU Courant with Dennis Shasha, MIMIC-III and cutoff/leakage controls. NSE India R&D: agent orchestration, incident RAG, llama.cpp SLMs, vLLM/Prometheus. NUS: 500+ PubMed papers and liposomal drug pairing. First-author published IEEE ICET 2025 StoryGuard; healthcare FHE/GenAI manuscript is MINOR REVISION, NOT PUBLISHED. Agent state/memory eval synthetic score from 0.681 to 0.792, never claim real-world measured success.
Do not invent grades or GTA teaching experience. Claims from outside the resume must be approved in a local provenance-tagged truth bank.
No non-work personal details in emails.

## Templates: short, plain text, exact evidence-backed placeholders

### GRA | target 100-140 words
Subject: Spring 2027 GRA inquiry — [specific area]

Dear Professor [LAST_NAME],

I'm a Georgia Tech M.S. Computer Science student specializing in AI, currently working on [TRUTH_BANK_GT_PROJECT]. I'm writing about potential funded GRA opportunities in your group for Spring 2027.

I was interested in your work on [EXACT_PAPER_OR_PROJECT_TITLE] ([YEAR]), particularly [SINGLE_CLAIM_CONFIRMED_IN_ABSTRACT_OR_FULLTEXT]. This connects with my [ONE_VERIFIED_RELEVANT_EXPERIENCE] where I [ONE_VERIFIED_CONTRIBUTION]. I'd be interested in contributing to [SPECIFIC_SHARED_DIRECTION], especially [SMALL_CONCRETE_POSSIBLE_CONTRIBUTION].

Would your group anticipate taking on a master's GRA next semester? If so, I'd appreciate a brief conversation. I've attached my research resume.

Best regards,
[NAME]
M.S. Computer Science | Georgia Tech
[UNIVERSITY_EMAIL]
[RESEARCH_PORTFOLIO_URL]

Validation: reference *one* verified publication/project; natural line; 100-140 words after substitutions; do not assert current funding availability without source.

### GTA | target 80-110 words
Subject: Spring 2027 GTA interest — [COURSE_CODE]

Dear Professor [LAST_NAME],

I'm a Georgia Tech M.S. CS student specializing in AI, and I'm interested in serving as a GTA for [EXACT_COURSE_CODE_AND_TITLE] in Spring 2027.

My background includes [SPECIFIC_VERIFIED_COURSE_OR_PROJECT] and [CONCRETE_SUBJECT_COMPETENCY]. I would be glad to support grading, office hours, assignment debugging, and student questions. [OFFICIAL_FORM_STATUS_ONLY_IF_VERIFIED]

Are you expecting GTA openings for this course, or is there a coordinator I should contact? I'd appreciate the chance to discuss where I could help. I've attached my resume.

Best regards,
[NAME]
Georgia Tech M.S. CS
[UNIVERSITY_EMAIL]

Validation: professor-course section match verified, not paper-first, no false grade/final TA history. Do not claim survey completion unless actually done.

### Industry research | target 90-130 words
Subject: [TEAM/RESEARCH_AREA] — [EXACT_ROLE_TITLE / SUMMER 2027]

Hello [RECIPIENT_FIRST_NAME],

I'm a Georgia Tech M.S. CS student working on [ONE_VERIFIED_PROJECT_AREA]. I came across your [EXACT_PAPER_TITLE_OR_VERIFIED_TEAM_PROJECT], especially [SUPPORTED_SPECIFIC_TAKEAWAY], and wanted to reach out.

I'm interested in [VERIFIED_OPEN_ROLE_TITLE] at [COMPANY] ([JOB_ID_IF_USEFUL]). In previous work at [VERIFIED_EXPERIENCE_INSTITUTION], I [ONE_CONCRETE_RELEVANT_CONTRIBUTION], which overlaps with [PROJECT_PROBLEM]. I would value your perspective on whether this team is a relevant fit and what skills I should emphasize.

If you have 10 minutes for a brief conversation, I'd be grateful. My resume is attached.

Best,
[NAME]
Georgia Tech M.S. CS
[PORTFOLIO_URL]

Validation: role officially open, current recipient/company identity verified, not a hard referral demand, no paper-summary invention.

## Email draft quality rubric (hard blockers trump numeric ranking)
100-point draft score: recipient+current role accuracy 20; paper/job/course identity and support 20; genuine experience bridge 20; clarity/conciseness 15; single natural ask 10; grammar and plain-text formatting 10; attachment integrity 5. 90+ auto-ready for HUMAN review, 75-89 human rework, <75 quarantined; any blocker prevents Outlook draft.
Block on: empty/guessed email, wrong org/person, affiliation stale/unclear, paper not authenticated, stale/closed role, U.S.-citizen requirement for ineligible applicant, false teaching grade, unverified form completion, unsupported publication claim, missing resume, lack of actual contact relevance, prior decline/opt-out, conflicting campaign history, invalid attachment, placeholder leakage.
Emails for familiar professors/advisors must be relationship-aware, not framed as unsolicited cold outreach.

## Expected CSV columns (separate raw and vetted)
`campaign,person_id,full_name,role,institution,department,company,team,professional_email,email_source_url,email_verified_at,current_affiliation_source_url,affiliation_checked_at,profile_url,paper_doi,paper_title,paper_year,paper_source_url,paper_abstract_source,author_match_confidence,paper_relevance_score,job_id,job_official_url,job_checked_at,job_status,job_eligibility,course_code,course_title,course_crn,course_instructor_source,source_url,contact_suppressed,recipient_score,draft_subject,draft_status,outlook_draft_id,reply_status,review_notes`.
No contact address lists checked into the public repository. 
