# HazardLens Release Scope and Dependency-Aware Task Matrix

**Status:** Project lead approved this working direction on 9 October 2026; formal team approval remains pending. This is not a claim that the whole team approved the baseline.  
**SRS basis:** v3.1 proposed review baseline in PR #9.  
**Scheduling basis:** Relative phases only. The actual deadline, sprint length, student availability and weekly capacity have not been confirmed; no calendar commitments are implied.  
**Repository rule:** This matrix does not assert implementation completion. Close work only with linked, reproducible evidence and independent review.

## 1. Decisions and non-negotiable constraints

1. The four required MVP source families are MGB flood susceptibility, MGB rain-induced landslide susceptibility, PHIVOLCS liquefaction and PHIVOLCS active faults. A substitute requires an explicit team-approved scope change.
2. The first end-to-end slice should prove one verified source → normalized API → evidence UI → deterministic offline tests. Persistence/history is not required in that first slice, but FR-02 remains required before MVP release, including session ownership, expiry/deletion and persistence tests.
3. All four required sources must be integrated and verified before MVP sign-off.
4. An empty response is not automatically `NO_EVIDENCE`; source errors/timeouts are not `NO_EVIDENCE`. `OUTSIDE_COVERAGE` requires a documented, source-specific coverage rule. Do not infer coverage from a layer extent alone.
5. The 14-entity logical schema must be reviewed as a whole, but the first physical migration should include only entities needed by the approved workflow.
6. The deterministic explanation path must work without AI. Weather is in the MVP but must remain separate from hazard evidence and fail independently. Comparison, reporting and polygon investigation are post-MVP. AI work starts only after the first evidence slice and all four required sources are verified.
7. No calendar due dates, final assignments or claims of capacity until the team confirms the real deadline, commitments, and reviewer availability.

## 2. Requirement classification proposal

“Post-MVP” classifications below record the project lead's working direction, not formal team approval. FR-11/FR-12 are selected post-MVP, while FR-13/FR-21 remain MVP-required. The team must confirm or request changes before this becomes the canonical baseline; until then, do not claim whole-team approval.

### Functional requirements

| Requirement | Proposed classification | Rationale / release condition |
|---|---|---|
| FR-01 Location selection | MVP-required | Search/map/coordinate input contract; coordinate fallback must remain usable if geocoding fails. |
| FR-02 Investigation history | MVP-required; after first vertical slice | First slice may be source → API → evidence UI without persistence. Before MVP release, implement persistence, same-session ownership, expiry/deletion and tests. |
| FR-03 Concurrent source queries | MVP-required | Core four-source workflow and independent source failure handling. |
| FR-04 Five evidence statuses | MVP-required | Required evidence contract. |
| FR-05 Valid empty-result semantics | MVP-required | Prevents failed/unknown queries from appearing hazard-free. |
| FR-06 Geometry-appropriate operations | MVP-required | Point/fault operations must be source-specific; area operations only where supported. |
| FR-07 Provenance and attribution | MVP-required | Source, source-date basis, retrieval time, origin and attribution are essential. |
| FR-08 Preserve source classifications | MVP-required | No invented universal score or safety ranking. |
| FR-09 Multiple matches and disagreements | MVP-required | Preserve material results and source disagreement. |
| FR-10 Deterministic explanation | MVP-required | Evidence explanation must not depend on an AI provider. |
| FR-11 Compare saved investigations | Post-MVP (project-lead working direction; team approval pending) | Do not block MVP. |
| FR-12 Printable evidence report | Post-MVP (project-lead working direction; team approval pending) | Do not block MVP. |
| FR-13 Current weather | MVP-required (project-lead working direction; team approval pending) | Include FR-21 failure isolation; weather failure cannot change hazard results. |
| FR-14 Evidence UI independent of map/geocoder | MVP-required | The primary evidence workflow must still work when map tiles or geocoding fail. |
| FR-15 AI explanation | Proposed post-MVP | Start after the deterministic evidence slice passes and AI scope is approved. |
| FR-16 Evidence-grounded AI chat | Proposed post-MVP | Requires refusal, grounding and adversarial tests. |
| FR-17 Natural-language tool calling | Proposed post-MVP | Adds bounded orchestration and tool-security risks. |
| FR-18 AI output provenance | Proposed post-MVP | Required if AI is approved; not a reason to include AI in MVP. |
| FR-19 AI provider fallback | Proposed post-MVP | Applies when AI is in scope; deterministic explanation remains core. |
| FR-20 Polygon/area investigation | Post-MVP (project-lead working direction; team approval pending) | Requires source capability, geometry validation and configurable limits. |
| FR-21 Weather failure isolation | MVP-required, paired with FR-13 | Weather provider failure returns `UNAVAILABLE` without failing, altering or suppressing hazard results. |

### Non-functional requirements

| Requirement | Proposed classification | Rationale / release condition |
|---|---|---|
| NFR-01 Performance/deadline | MVP-required | Define reproducible cache-hit and bounded-live-query acceptance tests. |
| NFR-02 Timeout/retry policy | MVP-required | Bound upstream calls and retry only the specified failure classes. |
| NFR-03 Trusted upstream URLs | MVP-required | Prevent client-controlled arbitrary URL/SQL/tool inputs. |
| NFR-04 CORS and secret handling | MVP-required | Verify deployment-origin policy and server-side secret storage. |
| NFR-05 Anonymous session privacy/expiry | MVP-required if FR-02 remains MVP | Session cookie, no raw IP storage and 30-day expiry/deletion behavior must be tested. |
| NFR-06 Geocoding policy | MVP-required | Geoapify is the project-lead working selection, subject to team confirmation and verification of current terms, quota, attribution, and server-side key restrictions. If public Nominatim is used as fallback/alternative, enforce max 1 request/second, identifying User-Agent, and caching. No keystroke autocomplete; coordinate/map fallback must remain functional. |
| NFR-07 Recorded demo fixtures | MVP-required | Recorded fixtures must be reproducible and visibly labelled when used. |
| NFR-08 Attribution/limitations | MVP-required | Avoid implying that missing data means safety or that the app is an official assessment. |
| NFR-09 Dataset extensibility without schema changes | MVP-required; project-lead working definition, team approval pending | A compatible source fits existing normalized fields and supported spatial operations, and can be enabled by one adapter plus registry config/rows without a migration. Verify with a registered test/mock dataset and normal orchestration test. Sources that need new semantics require an explicit schema review; do not force compatibility. |
| NFR-10 Pinned dependencies/shared API contract | MVP-required | Clean-install and generated-contract workflow must be reproducible. |
| NFR-11 No HazardHunterPH scraping/embedding/framing | MVP-required | Compliance boundary; verify through code/config review. |
| NFR-12 Session ownership/access isolation | MVP-required if persistence is in scope | Test cross-session read/write denial without leaking existence. |
| NFR-13 Public endpoint rate limits | MVP-required | Agree limits/defaults and verify HTTP 429 behavior for expensive public operations. |
| NFR-14 AI timeout/fallback | Proposed post-MVP | Required before any approved AI release. |
| NFR-15 Prompt-injection resistance | Proposed post-MVP | Required before AI consumes untrusted user/source content. |
| NFR-16 Accessibility | MVP-required | Keyboard operation, visible focus, labels and status announcements; WCAG 2.2 AA is a target, not a claimed certification. |
| NFR-17 Browser/responsive support | MVP-required | Test agreed browser versions and common mobile viewports. |
| NFR-18 Privacy-safe diagnostics | MVP-required | Useful request/source/status/latency/error diagnostics without raw IPs or secrets. |

**Cross-dependency:** FR-02 remains MVP-required but may follow the first source → API → UI slice; NFR-05 and NFR-12 must ship with persistence/history before MVP release. FR-13 is MVP-required, so FR-21 failure isolation is also required. AI FR-15–FR-19 and NFR-14–NFR-15 remain gated until the first evidence slice and all four required sources are verified. FR-11, FR-12 and FR-20 are post-MVP in the project-lead working direction; team approval remains pending.

## 3. Dependency-aware work packages

Effort sizes below are relative planning estimates only. Confidence is low until source verification, team availability and the rubric/deadline are confirmed.

| WP | Scope / existing issue(s) | Depends on | Deliverable and measurable exit criteria | Suggested accountable track (confirm with team) | Relative effort / confidence |
|---|---|---|---|---|---|
| WP-0 Governance and scope gate (#12, PR #9) | Baseline, requirement classifications, policy and release boundary | None | Team records approval/changes to the proposed classifications; SRS status is explicit; remaining governance decisions, repository rules and course constraints have evidence/owners. | Project lead + whole team | M / low |
| WP-1 Source verification (#2) | Verify four official sources independently | WP-0 scope direction; source access | For each source: official URL and exact layer ID, geometry/SRID, relevant class/date fields, query operation, attribution, timestamped live test, empty/error behavior, coverage basis, sanitized fixture and repeatable tests. No substitute source silently added. | GIS/source track + independent QA | L / low |
| WP-2 Logical schema and first migration plan (#1, NFR-09 clarification in #19) | Reconcile all 14 logical entities; choose first physical migration boundary | WP-0; FR-02 decision; WP-1 source metadata where relevant | Relationship/retention/deletion rules, geometry types/SRID/indexes and constraints documented; migration scope is justified by approved workflow; clean-database migration test passes. | Database track + independent reviewer | M–L / low |
| WP-3 First end-to-end slice (#3, PR #11) | One verified source → normalized API → evidence UI | WP-1 selected source; API/evidence contract; WP-2 if persistence is in slice | A coordinate investigation renders evidence with source/class/status/provenance; source failure is isolated; recorded fixture mode is labelled; tests reproduce offline. No claim that this completes all four-source MVP. | Backend + frontend tracks, named reviewer distinct from author | L / low |
| WP-4 Remaining source adapters (#6) | Integrate other required sources and multi-source orchestration | WP-1; WP-3 contract | All four mandatory sources run under bounded deadline; one failure does not suppress others; class labels and multiple matches preserved; per-source behavior tested against official/recorded evidence. | GIS/backend track + QA | L / low |
| WP-5 History and session lifecycle (#13; #1) | Persist investigations, history and anonymous ownership | WP-2; approved FR-02 scope | Same session can list/read its investigations; another session cannot access guessed IDs; cookie/expiry/deletion behavior tested; no raw IP in storage/logs. | Backend/database track + security reviewer | M–L / low |
| WP-6 Location input and resilient UI (#7, #8) | Search provider, coordinate/map fallback, evidence panel | WP-0 provider decision; WP-3 API contract | Search selection or coordinate fallback reaches investigation; evidence renders when geocoder/map tiles fail; all five statuses and provenance are accessible and accurately worded. | Frontend + backend track + QA | M / low |
| WP-7 Cross-cutting reliability/security (#17) | Rate limits, diagnostics, URL restrictions, CORS and secret review | API routes/contracts; deployment assumptions | Test below/at/above limits, HTTP 429, source timeouts, safe logs, allowed origins and no client-controlled upstream URLs. | Backend track + independent reviewer | M / low |
| WP-8 Release verification (#18 + #12 + #20) | Accessibility/browser checks, clean setup, release traceability | WP-3 through WP-7; approved release scope | Clean-checkout commands recorded; CI results tied to commit; browser/viewport matrix run; keyboard/focus/status checks recorded; each MVP requirement links to evidence or explicit blocker. | QA + one backend and one frontend teammate | M / low |
| WP-9 Conditional post-MVP work (#4, #14, #16) | AI, comparison/report, polygon | First evidence slice and all four required sources verified for AI; team review of post-MVP scope | Each feature has approved scope, owner, reviewer, measurable criteria and failure tests before implementation starts. Weather is MVP scope and must have FR-21 failure isolation. | To be decided after capacity review | Variable / low |

### Suggested execution order

1. **WP-0 governance and scope gate** — resolve SRS/architecture contradictions and confirm the decision path.
2. **WP-1 source verification** — start early because upstream behavior is the highest uncertainty.
3. **WP-2 schema planning in parallel** — review logical design, but do not implement unnecessary physical tables.
4. **WP-3 first slice** — use the source only after its operation and status semantics are sufficiently verified.
5. **WP-4 through WP-7** — broaden the required sources, complete history if still in scope, and harden the app.
6. **WP-8 release verification** — no sign-off without traceable evidence for every approved MVP requirement.
7. **WP-9** — only after explicit team decision and remaining capacity are known.

The order allows source research and schema review to run in parallel, but integration and release acceptance retain their dependencies. If WP-1 finds an official source cannot be queried as expected, document the blocker and return to the team; do not silently substitute another dataset.

## 4. GitHub backlog hygiene

- Keep issue #12 open as the Gate 0 planning and governance gate until whole-team review is complete and organization invites are accepted.
- PR #9 (SRS v3.1 baseline) and PR #11 (MGB flood preview slice) are merged into `main`; live-source repeatability and coverage remain pending under Gate A and Issue #2.
- Issue #4 is moved to Gate E & Post-MVP milestone with label `post-mvp`; AI execution remains strictly gated behind Gates B and C.
- Milestones are organized by Delivery Gates (Gates A–E) without arbitrary calendar deadlines.
- Every backlog issue (#1–#8, #12–#20) is standardized with Section 8 structure, explicit lead implementers, and independent reviewers (`Author != Reviewer`).
- Pre-execution gate is strictly enforced: no feature implementation code is written until Gate 0 is fully closed.

## 5. Evidence gaps that remain open

| Gap | Current state | Required closure evidence |
|---|---|---|
| Four official sources | MGB flood has limited captured-response evidence; other source live behavior and all coverage semantics remain unverified. | Reproducible, timestamped source records and contract tests for each exact layer. |
| Empty/outside-coverage distinction | Not fully established for all sources. | Successful query evidence plus a defensible source-specific coverage rule; do not infer from empty response or extent alone. |
| Fault proximity distances | 1/5/10/20 km are exploratory test bands only. | Source method/units and rationale before any user-facing thresholds are selected. |
| Team deadline, rubric and capacity | Not confirmed. | Team-recorded values and weekly availability. |
| Branch/review enforcement | Integration could not confirm protection state. | Repository administrator verifies active rules and required checks. |
| Clean-checkout setup | Not independently reproduced in this review. | Teammate records OS, commands, migration result, API/frontend startup and commit. |
| Requirement classifications | Proposed, not team-approved. | Explicit team decision; update SRS and traceability in same review cycle. |
| NFR-09 | Working definition recorded; verification pending. | Register a compatible test/mock dataset through one adapter and registry configuration/rows, query it through normal orchestration, and verify no schema migration is required. |

## 6. Team review agenda (30–45 minutes)

1. Confirm the four-source non-substitution rule.
2. Review the project-lead working classifications: FR-11/FR-12/FR-20 post-MVP; FR-13/FR-21 MVP-required; AI gated; NFR-09 adapter/registry acceptance test. Explicitly confirm or request changes.
3. Confirm the sequencing decision: source → API → evidence UI first, then persistence/history; FR-02 and its security/lifecycle dependencies remain required before MVP release.
4. Confirm official-source verification owners and independent QA.
5. Confirm actual deadline, rubric, member availability and weekly capacity.
6. Verify branch protection/review enforcement and agree the clean-checkout verifier.
7. Record approved decisions and changes in the repository; then convert relative work packages into estimates and assignments.

## 7. Definition of planning readiness

Planning is ready for committed scheduling only when:
- the SRS is explicitly approved or returned with named changes;
- each FR/NFR has a proposed release classification accepted by the team, or is explicitly unresolved;
- no required-source substitution is implicit;
- the source verification plan and first-slice persistence boundary are clear;
- owners, independent reviewers, dependencies and capacity are confirmed;
- repository enforcement and clean-checkout setup have evidence;
- acceptance criteria and verification records are linked to each release work package.

Until then, project status remains **planning in progress — baseline approval pending**.
