# Interface contract frozen by Session 00 before parallel implementation

This is a CONTRACT blueprint; Session 00 must implement the corresponding typed Python models and stable interface functions in src/outreach_engine/core. Parallel sessions may add adapters but must NOT change shared interface signatures unilaterally.

## Data models (Pydantic v2 preferred)
Campaign enum: gt-gra, gt-gta, industry.
Person: id, full_name, names/aliases, current_affiliation, current_role, stable_identity_sources, candidate_professional_contacts, contact history.
AffiliationEvidence: name, organization, role, source_url, fetched_at, confidence, status current/uncertain/historical.
ContactEvidence: normalized email, person_id, professional/public indicator, source_url, fetched_at, verified_identity bool, verified_current_affiliation bool, contact permission flags.
Publication: DOI-or-canonical-ID, title, authors with ID, cited_by_count (source and retrieval date), year, abstract-supported claims, source_url, current-author match result.
JobOpportunity: external_job_id, company, official_job_url, job_title, team if known, checked_at, open_status, internship_season, US/location, eligibility flags.
CourseSection: term, course_code, official_title, section, CRN, instructor_ids, current course source, course eligibility, forms source.
ResumeClaim: claim_id, statement, verified source/resume section, tags, allowed_email_use, uncertainty note.
Lead: stable lead_id, campaign, person_id, opportunity_ref, contact_evidence_ref, ranking, current_status, suppression data, audit.
Evidence: evidence_id, entity_id, claim, source_url, fetch_timestamp, source_type, support_level, content_hash.
DraftProposal: recipient_contact_id, campaign, subject, body_plain_text, resume_path, resume_sha256, referenced_evidence_ids, email_score, blocking_reasons, rendered_sha256, review_version.
Approval: lead_id, draft_sha256, approved_at, reviewed_by local user, explicit yes/no.
MailboxDraftReceipt: draft_id, store_id, parent_folder_id, actual_account_email, saved_at, roundtrip_verified, subject_hash, attachment metadata, delivery_kind OUTLOOK_DRAFT or EML_EXPORT_ONLY.

## Shared functions and durable operations
- discover(ctx: RunContext) -> iterable[RawCandidate] with provenance; concrete adapters are child-owned and register by campaign.
- normalize_person(raw) -> Person and zero or more evidence/contacts. No guessed contact as verified.
- enrich_publications(person) -> list[Publication] via public academic APIs; return explicit errors/empty sets.
- rank_lead(lead, evidence, truth_bank) -> ScoreBreakdown, separate policy for campaign.
- compose_draft(lead, evidence, truth_bank) -> DraftProposal; structured schema, independent validator.
- approve_drafts(manifest IDs + SHA) -> audited approved set, no approval by default.
- persist_local_draft(ApprovedDraft, account_selector) -> MailboxDraftReceipt after COM Save()+read-back or EML_EXPORT_ONLY; never Send.
- scan_replies(dry_run=True) -> tagged events, read-only on first use; message moves opt-in only.

## Directory ownership
Session 00: src/outreach_engine/core/**, src/outreach_engine/cli.py, src/outreach_engine/__init__.py, pyproject.toml, README.md, tests/core/**, docs/API_CONTRACT_V2.md.
Session 01: src/outreach_engine/pipelines/gt_gra/**, tests/gt_gra/**, docs/RESULTS_GRA.md.
Session 02: src/outreach_engine/pipelines/gt_gta/**, tests/gt_gta/**, docs/RESULTS_GTA.md.
Session 03: src/outreach_engine/pipelines/industry/**, tests/industry/**, docs/RESULTS_INDUSTRY.md.
Session 04: src/outreach_engine/research/**, src/outreach_engine/drafting/**, tests/research/**, tests/drafting/**, docs/RESULTS_RESEARCH.md.
Session 05: src/outreach_engine/outlook_local/**, tests/outlook_local/**, docs/RESULTS_OUTLOOK.md.
Session 06: tests/acceptance/**, tests/security/**, docs/RESULTS_QA.md. Advisory findings, no production edits.
Session 07: integrates all branches; may modify any directory to repair tests, updates README, docs/RESULTS.md, docs/USER_ACTIONS.md, docs/OUTLOOK_SETUP.md.
Session 01/02/03/04/05 must build against Session 00 actual schema, use independently named modules, no modifying common files. Each child implements registration hooks or integration adapters in OWN directory and writes import instructions. Session 07 wires all modules to CLI. NO simultaneous writes on shared SQLite database by independent Codex sessions; offline isolated test DBs and no live drafts.

## Persistence
SQL schema versioned migration with foreign keys, unique campaign/person/opportunity keys, evidence source/provenance, state transition history, suppression entries and review/draft idempotency. Keep transaction atomic with WAL and test rollback/resume.
Campaign status enum: DISCOVERED, VERIFIED, ENRICHED, REVIEW_READY, APPROVED, OUTLOOK_DRAFT_SAVED, EML_ONLY_EXPORTED, SENT_OBSERVED, REPLIED, DECLINED, NEEDS_REVIEW, SUPPRESSED. Not all transitions direct; enforce finite state machine.
No hardcoded root-specific paths; Windows path environment OUTREACH_RESUME_PATH and OUTREACH_PRIVATE_DATA_DIR; default local private folder under repo ignored by Git.
