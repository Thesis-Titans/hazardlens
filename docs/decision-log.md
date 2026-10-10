# HazardLens Decision Log

**Status:** Project-lead working direction updated 9 October 2026; formal team approval pending  
**Baseline:** SRS v3.1 merged on `main` via PR #9; formal whole-team approval remains pending.  
**Rule:** A decision is not final merely because it appears in this file. Record the decision owner, date, rationale, and affected requirements when the team agrees.

## Decision register

| ID | Topic | Current proposal / known fact | Status | Decision owner / next action |
|---|---|---|---|---|
| DEC-01 | SRS version | The SRS revision history contains v3.1 entry dated 9 Oct 2026. PR #9 merged on `main`, reconciling front matter and architecture/verification headers to v3.1. Formal whole-team kickoff confirmation pending. | **Merged review baseline on `main`; team confirmation pending** | Project lead + whole team: confirm baseline at kickoff. |
| DEC-02 | Database schema and migration strategy | SRS §4.6 names 14 logical tables, including dataset, location, and comparison_investigation; issue #1 previously used hazard_dataset and omitted two tables. | **Selected direction; details pending review** | Database owner + project lead: review the full logical design, then implement migrations incrementally as the MVP needs them. Settle types, nullability, constraints, indexes, uniqueness and deletion semantics before each migration. |
| DEC-03 | Evidence status semantics | Use FOUND, NO_EVIDENCE, OUTSIDE_COVERAGE, UNAVAILABLE, UNSUPPORTED. A source error or timeout is not NO_EVIDENCE. OUTSIDE_COVERAGE requires a defensible coverage rule. | **SRS rule; source-specific verification pending** | Project lead + source owner + QA: confirm semantics against each layer. |
| DEC-04 | Geocoding interaction/provider | Use explicit user-submitted place search plus coordinate/map fallback; no keystroke-by-keystroke autocomplete against public Nominatim. Project lead selects Geoapify as the working MVP provider. Verify current free-tier quota, Geoapify/OpenStreetMap attribution requirements and API-key restrictions before implementation; never commit an unrestricted key. | **Project-lead selection; team confirmation and configuration verification pending** | Backend + frontend owners: confirm provider, check current terms, configure key restrictions, implement timeout/error behavior and test coordinate fallback. https://apidocs.geoapify.com/docs/geocoding/ ; https://myprojects.geoapify.com/help/api-keys/ |
| DEC-05 | First delivery goal | Build a verified source → normalized API result → evidence UI vertical slice first; then integrate all required core sources before MVP sign-off. Defer AI and advanced features. | **Selected by project lead/user; team confirmation required** | Whole team: confirm at planning and agree observable exit criteria. |
| DEC-06 | MGB flood preview | PR #11 merged on `main` containing a limited preview adapter plus two captured response fixtures: a Central Iloilo query returned one `MF` feature, and an offshore Panay Gulf query returned an empty `features` array. The fixtures are replayed in mocked/offline tests; they prove the captured responses, not current endpoint availability, full coverage, or that an empty response is valid `NO_EVIDENCE`. | **Merged preview slice on `main`; live repeatability & coverage semantics pending Gate A** | Source owner + QA: independently repeat the query, preserve request/response provenance, verify coordinate/query behavior and coverage, and document source-date limitations under Gate A. |
| DEC-07 | Health endpoint contract | Separate `GET /health/live` (process-only, no dependency calls) and `GET /health/ready` (bounded checks of required internal dependencies; return 503 if a required dependency prevents core service). Track MGB, PHIVOLCS and weather-provider health independently; do not make liveness fail due to upstream outages or probe every provider on every health request. Responses must not expose secrets or stack traces. | **Project-lead working direction; team confirmation and response-schema tests pending** | Backend owner: document JSON schemas/status codes and implement tests for dependency failure, upstream timeout isolation and secret-safe responses. |
| DEC-08 | AI and advanced features | AI/provider work is deferred until the first evidence vertical slice is verified; required core source integrations come before MVP sign-off. | **Selected direction; team confirmation required** | Project lead + team: preserve the gate unless an explicit scope change is recorded. |
| DEC-09 | Team roles and capacity | Proposed role tracks are not confirmed assignments; current GitHub issue assignments do not prove current availability or reviewer independence. | **Open** | Whole team: confirm owners, availability and a different reviewer for every active issue. |
| DEC-10 | Schedule | Plan in relative phases first; do not invent dates before the real deadline, availability and capacity are confirmed. | **Selected planning rule; calendar schedule open** | Whole team: confirm deadline, sprint length, class/other commitments and realistic capacity before due dates are created. |
| DEC-11 | Official source candidates | Official metadata has been reviewed for MGB flood/landslide and PHIVOLCS liquefaction/active-fault candidate layers; the active-fault candidate page returned an application error on direct access. | **Metadata research only; live behavior unverified** | GIS/source owner + QA: use docs/source-verification-notes.md, verify the chosen exact layer and execute live test queries before integration. |
| DEC-12 | Requirement release classification | Project lead selected FR-11 and FR-12 post-MVP; FR-13 and FR-21 MVP-required; FR-20 post-MVP; AI FR-15–FR-19 gated until the first evidence slice and all four required sources are verified. | **Project-lead working direction recorded 9 Oct 2026; whole-team approval pending** | Whole team: confirm or request changes; update SRS, traceability and task matrix together. |
| DEC-13 | Required source set and coverage semantics | The four named source families remain mandatory. A layer extent alone does not prove valid coverage; outside-coverage and fault-distance semantics need source-specific evidence. | **Working direction; team confirmation required** | GIS/source owner + QA: verify each source; team must explicitly approve any change to the required-source set. |
| DEC-15 | Project-lead scope decisions (9 Oct 2026) | FR-11 comparison and FR-12 report are post-MVP; FR-13 weather stays in MVP with FR-21 failure isolation; FR-20 area investigation is post-MVP; AI begins only after the first evidence slice and all four sources are verified; FR-02 persistence/history is not required in the first slice but must ship before MVP release; NFR-09 means one adapter plus registry config/rows for a compatible source, without schema migration. | **Recorded as project-lead working direction; whole-team approval pending** | Whole team: review and explicitly confirm or request changes. A compatible-dataset test is still needed to verify NFR-09. |
| DEC-14 | Release classifications and dependency-aware work packages | Project lead selected the working classifications on 9 Oct 2026: FR-11/FR-12/FR-20 post-MVP; FR-13/FR-21 MVP-required; AI after the first evidence slice and verification of all four required sources. The first slice is source → API → evidence UI; FR-02 persistence/history is still required before MVP release. | **Project-lead working direction recorded; whole-team approval pending** | Whole team: confirm or request changes; keep SRS, traceability and matrix consistent. No deadline or teammate availability is inferred. |

| DEC-16 | Weather provider and failure isolation | Use Open-Meteo as the working MVP weather provider, subject to confirming the current non-commercial-use terms, quota and attribution. Weather is supporting context only and is not hazard evidence. Use a configurable bounded timeout (initial default 3 seconds); on timeout, provider error or invalid payload, return a weather-specific `UNAVAILABLE` state without changing hazard results. | **Project-lead working direction; team confirmation and implementation tests pending** | Backend owner: verify current Open-Meteo terms, document attribution and response normalization; test success, timeout, malformed response and isolated provider failure. https://open-meteo.com/en/terms ; https://open-meteo.com/en/docs |
| DEC-18 | Pre-execution gate, delegation matrix & issue standardization | Enforce Gate 0 (no implementation execution begins until planning, issue standardization, and delegations are settled). Establish 3-track 5-person delegation matrix with independent reviewer pairings (Author != Reviewer). All 17 issues standardized with Section 8 structure. | **Approved by project lead; enforced immediately** | Project lead + whole team: verify issue standardization, confirm delegation pairings, complete the two remaining organization invitations reported by the project lead before opening implementation PRs; verify the current organization roster and invitations. |

## DEC-17 — Project-lead approval of implementation recommendations (9 October 2026)

**Decision owner:** Mark (project lead)  
**Status:** Approved by the project lead; whole-team confirmation remains pending. This approval does not represent approval by the other team members or make the SRS baseline canonical.

The project lead approved the following working recommendations for planning and implementation:

- **Database and migrations (DEC-02):** Keep the 14-entity logical model as the design reference and implement physical migrations incrementally. Before each migration, document and review types, nullability, constraints, indexes, geometry/SRID, retention, and deletion behavior. Test migrations against a clean PostgreSQL/PostGIS database.
- **Evidence semantics (DEC-03):** Preserve the statuses `FOUND`, `NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, and `UNSUPPORTED`. A failed or malformed query is not `NO_EVIDENCE`; only use `OUTSIDE_COVERAGE` when a defensible coverage rule exists.
- **Location search (DEC-04):** Keep Geoapify as the working place-search selection, subject to verification of current quota, terms, attribution, and API-key restrictions. Preserve coordinate/map fallback when geocoding is unavailable. Team confirmation and configuration tests remain required.
- **Health contracts (DEC-07):** Separate process-only `GET /health/live` from bounded `GET /health/ready`. Return 503 from readiness only when a required internal dependency prevents core service. Track upstream source/weather health separately; do not expose secrets or stack traces.
- **Weather (DEC-16):** Keep Open-Meteo as the working MVP provider, subject to verification of current terms, quota, and attribution. Use a configurable initial 3-second timeout. Provider errors, timeouts, and malformed payloads must yield weather-specific `UNAVAILABLE` without changing or suppressing hazard findings.
- **Source verification:** Independently verify all four required hazard source families and record service/layer identity, spatial operation and CRS, fields/classifications, attribution, timestamps, sanitized samples, coverage semantics, and timeout/empty/error behavior. Captured fixtures prove only the captured responses, not current service availability or complete coverage.
- **Vertical-slice sequencing (DEC-05/DEC-08):** First prove one verified source → normalized API → evidence UI with deterministic offline tests. Then integrate all four required sources. AI remains gated until the first slice and all four required sources are verified. FR-02 history/persistence is still required before MVP release.
- **NFR-09 extensibility:** Verify a compatible mock dataset can be registered through one adapter plus registry configuration/rows and queried through normal orchestration without a schema migration. If a source's semantics do not fit the normalized model, conduct an explicit schema review rather than forcing compatibility.

**Rationale:** This sequencing prioritizes trustworthy hazard evidence, bounded failures, source provenance, and testable extensibility while avoiding premature schema work and optional-feature expansion.

**Required follow-up:** The whole team must confirm or request changes. Keep formal team approval pending until that confirmation is recorded. Update the SRS, traceability matrix, task matrix, and relevant contracts together if the team changes any requirement or release classification.

## DEC-18 — Pre-execution gate, delegation matrix, and issue standardization policy (9 October 2026)

**Decision owner:** Mark (project lead)  
**Status:** Approved by project lead; enforced immediately across repository and backlog.

The project lead approved the following systematic governance and delegation rules:

1. **Pre-Execution Gate (Gate 0 Enforcement):** No additional feature implementation work shall begin until Gate 0 is formally closed (the execution plan is polished, all backlog issues are standardized with testable criteria, and task delegations are confirmed). Merged PR #11 code is recognized as a limited preview slice; full orchestration and remaining sources remain gated under Gates A, B, and C.
2. **Three-Track, Five-Person Delegation Matrix:**
   - **Data & AI Infrastructure:** `@markalvincadangin` and `@vincenttamano` (FastAPI, PostGIS, adapters, evidence schemas, AI grounding engine).
   - **Interactive GIS & Geolocation:** `@Justin-Ardena` (MapLibre GL viewer, vector layers, reverse geocoding, fault proximity).
   - **Product UI/UX & QA Testing:** `@Lovelly143` and `@faithbn` (Evidence card UI, design system, attribution, accessibility, responsive testing, test suite verification).
3. **Independent Review Pairing Invariant (`Author != Reviewer`):**
   - Every task has a designated Lead Implementer and an Independent Reviewer from a complementary role.
   - Self-approval is strictly forbidden on all pull requests and acceptance criteria sign-offs.
4. **Issue Standardization Schema:** All active GitHub issues must follow the 7-part Section 8 specification: Purpose, Scope (Included/Excluded), Dependencies, Team Delegation, Acceptance Criteria, Verification Evidence, and Completion Rule.
5. **No Unsupported Claims:** An issue cannot be closed by a green CI build alone; reproducible verification evidence (test outputs, fixtures, audit logs) must be linked upon closure.

## How to close a decision

For each decision, distinguish a user/project-lead preference from a team-approved decision. Record:

- agreed outcome and alternatives rejected;
- decision owner and date;
- evidence/source consulted;
- affected SRS requirements, issues and code;
- follow-up work and how the result will be verified.
Do not mark a decision team-approved until the team explicitly confirms it.

For decisions that alter requirements, update the SRS and traceability matrix in the same review cycle. Do not treat comments in a PR as the only permanent record of a product decision.

## DEC-19 — Agile and Sprint operating agreement (9 October 2026)

**Status:** Proposed team working agreement; whole-team approval pending.

HazardLens proposes a lightweight Scrum-based workflow with time-boxed Sprints and GitHub Flow. The delivery gates (Gate 0 and Gates A–E) remain dependency and acceptance controls, not Sprints. The team must confirm the Product Owner, facilitator, Sprint length, real deadline, and individual capacity before calendar dates or Sprint commitments are created. The proposed [Agile and Sprint Management Plan](agile-sprint-management-plan.md) defines Sprint Planning, regular progress inspection, Sprint Review, Retrospective, backlog quality guidance, and a project-specific Definition of Done. This proposal does not claim that the team is already fully practicing Scrum.

**Next action:** Whole team reviews/amends the plan at kickoff, records the agreed accountabilities and cadence, then updates this decision's status. Until then, Gate 0 remains open and feature implementation remains paused.
