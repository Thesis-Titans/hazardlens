# HazardLens Project Execution Plan

**Status:** Proposed for team review  
**Repository baseline:** `main` at the time this plan was prepared  
**Planning basis:** Current SRS, architecture and verification documents; existing GitHub issues #1–#8  
**Scope:** Requirements alignment, delivery sequencing, team delegation, verification and sprint control

> This plan is a working agreement proposal, not evidence that any feature is implemented. Do not mark requirements complete until the implementation and its verification evidence are present.

## 1. Current baseline and recovery objective

HazardLens currently has a React/Vite/TypeScript frontend scaffold, a FastAPI application with a health endpoint, and CI checks. The main application journey—select a place, query official hazard sources, normalize results, and render evidence—must be treated as **not delivered until proven by code and tests**. The landing page must not imply that real hazard lookups or grounded AI are working while those capabilities remain unimplemented.

**Recovery objective:** deliver one small, reliable, end-to-end hazard investigation vertical slice first. Expand only after the source query, result semantics, API contract, UI rendering and offline tests all work together.

## 2. Decisions captured for planning; team sign-off still required

The user selected option A for each of the seven setup decisions. These choices now guide the draft plan, but they are **not evidence of agreement by all five students**. Keep PR #9 in draft until the team reviews and records approval or requested changes.

| ID | Selected direction | What is settled for the working plan | What remains open |
|---|---|---|---|
| D-01 | SRS baseline | PR #9 aligns the SRS front matter and architecture/verification headers to v3.1. | Team approval of the SRS and PR #9. |
| D-02 | Full logical schema, incremental implementation | Review the complete 14-table logical inventory and relationships, but add tables/migrations incrementally when the MVP vertical slice needs them. | Column types, nullability, indexes, constraints, uniqueness, delete/retention rules and the exact first migration still need review. |
| D-03 | Explicit place search plus coordinate fallback | No keystroke-by-keystroke autocomplete against public Nominatim. Keep coordinate entry/map selection usable if search is unavailable; if public Nominatim is chosen, obey its request identification, rate limit, caching and attribution rules. | Team must confirm the provider and final UX. |
| D-04 | Verify each official source before integration | Each source must have a documented layer/service contract and reproducible verification. Recorded fixtures may temporarily unblock deterministic development only when clearly labelled as recorded data. | Live query behavior, coverage and empty-result semantics remain source-specific verification tasks. |
| D-05 | Separate liveness and readiness | Liveness reports whether the API process is running; readiness reports whether the app can serve its intended core contract. Optional external source health is reported separately and must not make the process appear dead. | Backend owner must propose bounded checks and tests; team reviews contract. |
| D-06 | Vertical slice before breadth | Complete one verified source → API → database as required → evidence UI slice first; then integrate every required core hazard source before MVP sign-off. Defer AI and advanced features. | Team confirms sprint scope and acceptance evidence. |
| D-07 | Relative phases before calendar dates | Keep the schedule in phases and decision gates until the real deadline and team capacity are confirmed. | Team must confirm project deadline, availability, sprint length and ownership before assigning dates. |

## 3. Delivery principles

1. **Evidence before AI:** hazard facts and classifications come from official sources. AI is optional explanation/navigation, never the authority.
2. **One end-to-end slice before breadth:** first make one verified source work through API → normalized result → UI → tests.
3. **Unknown is not safe:** distinguish `FOUND`, `NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE` and `UNSUPPORTED`. A timeout or source failure must never become `NO_EVIDENCE`.
4. **No invented source semantics:** use source-supported spatial operations. Do not apply point-in-polygon to line data or infer hazard probability from mere proximity without a documented rule.
5. **Deterministic core, optional integrations:** the core investigation must work without AI, geocoding or weather.
6. **Small reviewed changes:** one issue per branch where practical; pull requests must describe evidence, tests, risks and limitations.
7. **Honest status reporting:** distinguish implemented, tested, blocked, deferred and not started. CI passing on the scaffold is not feature verification.
8. **No unsupported completion claims:** never close an issue based solely on code being written; require acceptance criteria and reproducible evidence.

## 4. Proposed delivery sequence

Use relative phases and decision gates first. Do not assign or imply calendar dates from the current milestone labels. Confirm the actual project deadline, each student's availability, the sprint length and dependency-aware capacity with the team before creating or revising due dates. If the agreed timeline is unrealistic, reduce optional scope before weakening source verification, tests or review.

### Phase 0 — Align contracts and unblock the team (relative phase; duration to confirm)

**Goal:** prevent parallel work from implementing conflicting specifications.

- Review the proposed SRS v3.1 and all governance artifacts; the user's selections are a planning baseline, not team approval.
- Review the complete 14-table logical schema, but implement only the tables needed by the first vertical slice; add later tables in follow-up migrations as their workflows enter scope.
- Verify each official source before integrating it. Fixtures may be used as clearly labelled recorded-data fallbacks, never as proof of live availability.
- Choose a compliant place-search provider/interaction. Keep manual coordinate entry and map selection independent of the geocoder.
- Specify separate liveness and readiness endpoints/contracts; report optional upstream-source health independently.
- Confirm one accountable owner and a different reviewer for each active issue; add issue dependencies.
- Run the documented setup and CI checks. A green scaffold CI run is not a clean-checkout or PostGIS migration result.

**Exit criteria:** team-approved SRS and first-slice acceptance criteria; source and schema contracts reviewed enough for the first slice; known blockers, owners and reviewers recorded.

### Phase 1 — One verified vertical slice

**Phase goal:** A user submits coordinates and receives a truthful, normalized evidence card for one verified official hazard layer, including correct behavior for a match, a valid empty result, an upstream failure and invalid input. Include only the database tables and persistence required by the approved slice; do not force all 14 logical entities into the first migration.

**In scope**
- Verify and document one suitable official source and its exact query semantics.
- Define Pydantic request/response schemas and the five evidence statuses.
- Implement the smallest adapter/service/API path for that source.
- Render the API response in the frontend with source attribution and honest status text.
- Capture sanitized representative fixtures and test offline.
- Keep the database scope to the approved minimum needed for the slice; create migrations only after D-02 is resolved.

**Defer unless the goal is already met**
- Multi-provider AI, natural-language tool calling, weather, polygon analysis, comparison/reporting and extra source coverage.
- Broad UI polish that does not unblock or verify the slice.

**Acceptance tests**
- Valid coordinates + fixture representing a source match → `FOUND` and the source classification is preserved.
- Valid coordinates + valid empty source response within supported coverage → `NO_EVIDENCE`.
- Timeout, network error, malformed payload or 5xx → `UNAVAILABLE`.
- Coordinates outside the declared supported area → `OUTSIDE_COVERAGE`, but only where coverage can be justified.
- Invalid latitude/longitude → validation error; no upstream call.
- Unsupported hazard/source → `UNSUPPORTED`.
- UI never labels missing/failed evidence as “safe”; agency, source/layer and relevant provenance are shown.
- Backend tests run without network access; CI passes.

**Exit criteria:** a reviewer can clone the branch, run documented commands, execute tests and reproduce the slice from fixtures. A live endpoint check is recorded separately from deterministic offline tests.

### Phase 2 — Complete required MVP source coverage

**Phase goal:** Integrate every required core hazard source (MGB flood, MGB rain-induced landslide, PHIVOLCS liquefaction and PHIVOLCS active fault) only after each source's exact layer, spatial operation, coverage behavior, class/date fields, attribution and failure semantics are verified. Keep source fixtures clearly labelled as recorded fallback data.

- Add each source only after its contract is reviewed and its live query behavior has been separately verified; mock tests alone are not source verification.
- Use the correct spatial operation per geometry and service (point/polygon containment, identify, or documented distance rule).
- Add interactive map click selection and coordinate-input synchronization.
- Implement explicit place search only after provider/UX confirmation; preserve manual coordinate fallback.
- Add session/history persistence only after its schema and privacy/retention rules are approved, implementing the logical schema incrementally.
- Add per-source timeout and failure isolation; one failed provider must not erase successful results from others.
- If a source cannot be verified, report UNAVAILABLE or UNSUPPORTED as appropriate and document the blocker; never reinterpret uncertainty as no hazard.

**Exit criteria:** all four core source integrations have reviewed contracts and fixture-based tests; live verification records are distinct from offline tests; map selection drives the same API contract as coordinate input; provider failure is isolated; evidence provenance is visible. The MVP is not signed off while any required source is represented only by unverified live behavior or unlabelled fixtures.

### Sprint 3 — Reliability and user workflows

**Sprint Goal:** make investigation history and core evidence workflows dependable.

- Add anonymous session isolation, expiry and deletion behavior if confirmed in the approved SRS.
- Add comparison and printable report only after stored investigation contracts are tested.
- Add cache behavior, rate limiting, structured diagnostics and security checks appropriate to the deployment.
- Verify responsive layout and accessibility against the stated target.

**Exit criteria:** session isolation and expiry tests pass; error handling and operational limits are documented; user-facing workflows work without AI.

### Sprint 4 — Optional AI and release hardening

**Sprint Goal:** add only the AI capability that can be safely grounded in already verified evidence, then prepare a defensible demo/release.

- Run a bounded provider spike only after core evidence retrieval is stable.
- Use a strict tool allow-list, validated structured outputs, timeouts, bounded retry and deterministic fallback.
- Keep API keys server-side; do not expose prompts or credentials in client code/logs.
- Test prompt injection, unsupported questions, provider outage and malformed output.
- Freeze the demo dataset/fixtures and document limitations, setup, known issues and release verification.

**Exit criteria:** AI can fail without breaking the core; generated content is clearly identified and traceable to retrieved evidence; release checklist and demo path are reproducible.

## 5. Team responsibilities

Use the current issue delegation as a starting point, not a substitute for explicit team agreement. One person is accountable for delivery of an issue; another person reviews it. Everyone should review work outside their main area at least occasionally.

| Role | Proposed accountability | Expected outputs |
|---|---|---|
| Project lead / architecture — Mark | SRS decisions, API/schema contracts, scope, risk/dependency tracking, PR review and release decisions | Approved decisions, traceability, accepted PRs, accurate project status |
| GIS/source + backend — Vincent | Official-source verification, adapter contracts, fixture capture, backend integration | Source records, adapters, error semantics, contract tests |
| Frontend + QA — Faith | Evidence states and UI integration, test cases, acceptance verification | UI behavior, test checklist, reproducible acceptance evidence |
| Interactive GIS — Justin | Map and coordinate selection after the API contract stabilizes | Map interaction, coordinate synchronization, map-related tests |
| UI styling — Lovelii | Accessible visual system, evidence-card presentation, search UI after provider decision | Responsive components, status styling, accessibility checks |

**Capacity rule:** if a person is assigned both implementation and review of the same change, nominate a different reviewer. Do not assign every open issue to the project lead simply because the lead created it. Confirm current availability before treating this table as a final assignment.

## 6. Issue hygiene and GitHub workflow

Every implementation issue must include:

- Requirement IDs and exact links/sections in the approved SRS.
- One accountable assignee and a different reviewer.
- Dependencies and a clear in-scope / out-of-scope boundary.
- Acceptance criteria phrased as observable behavior.
- Test commands and evidence required for closure.
- A definition of done that includes docs and failure cases, not only the happy path.

**Branch and PR convention**
- Branch: `feat/<issue-number>-short-name`, `fix/<issue-number>-short-name` or `docs/<short-name>`.
- PR title references the issue, e.g. `feat(api): add first evidence vertical slice (#3)`.
- PR body explains requirements covered, design decisions, test commands/results, source verification and known limitations.
- Link PR to issue; request review from someone who did not author the change.
- Do not merge with failing required checks or unresolved safety/data-integrity concerns.
- Keep PRs focused and reviewable; split work rather than creating one large cross-stack PR.

## 7. Definition of Ready

An issue is ready to start only when:
- Its requirement and approved SRS version are identified.
- Acceptance criteria are testable.
- External source, schema and API assumptions are stated.
- Dependencies are complete or explicitly managed.
- The assignee and reviewer are confirmed.
- The work fits the sprint goal and the team's capacity.

## 8. Definition of Done

A feature is done only when all applicable items are true:
- [ ] Acceptance criteria are met in code.
- [ ] Unit/contract/integration tests cover success, empty and failure cases.
- [ ] Tests are deterministic offline where external services are involved.
- [ ] Lint, type checking and build/test CI pass.
- [ ] API contracts and docs match actual behavior.
- [ ] No secrets, default production credentials or unsafe configuration were introduced.
- [ ] Attribution, source date/provenance and limitations are present where applicable.
- [ ] UI states are accessible and do not imply unsupported certainty.
- [ ] A reviewer other than the author has approved the change.
- [ ] Verification record cites commands, results, date and commit/PR.
- [ ] The issue is closed only after the reviewer confirms the acceptance evidence.

## 9. Minimum verification evidence record

For every source adapter, record: official service URL; exact layer ID; geometry type; spatial reference; query method and parameters; classification and date fields; attribution; query timestamp; sanitized sample response; known coverage; latency; timeout behavior; empty-result behavior; error behavior; fixture path; contract-test path.

For every release candidate, record: commit SHA; environment/setup; migration result; test/lint/build commands and results; smoke-test path; browser/device notes; known defects; demo limitations.

## 10. Immediate next actions

1. Review the documentation and governance artifacts linked from `README.md` (execution plan, readiness checklist, traceability matrix, decision log, risk register and schema reconciliation); approve or request corrections before treating them as the team baseline.
2. Confirm sprint capacity, issue owners/reviewers and repository rules; resolve the blocking decisions in `docs/decision-log.md` before migrations or geocoding work.
3. GIS/backend owner verifies one source end-to-end and supplies a reviewed fixture plus source contract.
4. Backend/frontend pair implements the first vertical slice against the shared contract; QA adds acceptance tests for match, valid empty result, unavailable source, unsupported source and invalid coordinates.
5. Review the newly tracked backlog items #13–#18, confirm their dependencies and sprint placement, and assign owners/reviewers only after capacity is agreed; keep AI and other advanced features deferred until the core slice passes.

**Project status after this plan:** planning artifact proposed; no feature is marked complete by this document. The next status update must be based on merged code and verification evidence, not this plan alone.
