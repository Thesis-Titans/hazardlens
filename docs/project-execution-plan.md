# HazardLens Project Execution Plan

**Status:** Proposed for team review  
**Repository baseline:** `main` at the time this plan was prepared  
**Planning basis:** Current SRS, architecture and verification documents; existing GitHub issues #1–#8  
**Scope:** Requirements alignment, delivery sequencing, team delegation, verification and sprint control

> This plan is a working agreement proposal, not evidence that any feature is implemented. Do not mark requirements complete until the implementation and its verification evidence are present.

## 1. Current baseline and recovery objective

HazardLens currently has a React/Vite/TypeScript frontend scaffold, a FastAPI application with a health endpoint, and CI checks. The main application journey—select a place, query official hazard sources, normalize results, and render evidence—must be treated as **not delivered until proven by code and tests**. The landing page must not imply that real hazard lookups or grounded AI are working while those capabilities remain unimplemented.

**Recovery objective:** deliver one small, reliable, end-to-end hazard investigation vertical slice first. Expand only after the source query, result semantics, API contract, UI rendering and offline tests all work together.

## 2. Decisions required before implementation

These are blocking product-contract questions. Record the agreed answer in the SRS and update related issues before coding against either interpretation.

| ID | Decision | Why it blocks work | Required resolution |
|---|---|---|---|
| D-01 | What is the canonical SRS version? | The checked-in SRS revision history records v3.1 dated 9 Oct 2026, but the front matter and architecture/verification headers still said v3.0. | Reconciled in this branch: SRS front matter, architecture and verification headers now identify v3.1. Issue #1 uses the exact §4.6 table names and all 14 listed tables. This is a documentation reconciliation; project lead/reviewer must still approve the PR before it becomes the team baseline. |
| D-02 | What is the canonical schema? | Issue #1 lists `hazard_dataset` but the SRS data model uses `dataset`; the issue also omits SRS entities such as `location` and `comparison_investigation`. | Reconcile every table, key, relationship, retention rule and deletion behavior against the approved SRS before creating migrations. |
| D-03 | What place-search provider and interaction are allowed? | Issue #7 proposes Nominatim autocomplete, while the SRS NFR-06 prohibits Nominatim autocomplete. | Choose a policy-compliant provider/interaction, document attribution, rate limits, caching and fallback. Do not implement Nominatim autocomplete against the public service. |
| D-04 | Which exact source layers and query semantics are supported in MVP? | Source services can differ in geometry type, SRID, attributes, date/provenance and supported query operations. | Approve one exact layer per MVP hazard, source URL, layer ID, geometry/query method, classification field, source date and attribution. |
| D-05 | What must `/v1/health` mean? | SRS expects dependency/source health while current code returns a static application status. | Define liveness versus readiness and dependency checks; keep health checks bounded and do not let a failed optional hazard provider imply the whole app is dead. |
| D-06 | What is in Sprint 1? | Current issue set includes database, source verification, vertical slice and an AI spike, which risks splitting a five-person team before a working core exists. | Make the evidence-backed vertical slice the sprint goal; defer optional AI provider work unless the core goal is already on track. |

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

Use the existing two-week milestones as planning boundaries, but confirm dates and capacity with the team. If the milestone dates are already unrealistic, re-plan openly rather than silently carrying unfinished work.

### Phase 0 — Align contracts and unblock the team (first 1–2 working days)

**Goal:** prevent parallel work from implementing conflicting specifications.

- Resolve D-01 through D-06.
- Produce a requirements-to-code traceability table for MVP requirements: requirement ID, acceptance test, owning issue, code location, verification evidence and status.
- Confirm one accountable owner and a separate reviewer for every active issue.
- Add issue dependencies and mark work that cannot start until the source/schema/geocoding decisions are resolved.
- Confirm local setup and a reproducible CI baseline.

**Exit criteria:** approved SRS baseline; reconciled schema and source contracts; no unresolved contradiction in the next sprint's acceptance criteria; owners and reviewers recorded.

### Sprint 1 — One verified vertical slice

**Sprint Goal:** A user submits coordinates and receives a truthful, normalized evidence card for one verified official hazard layer, including correct behavior for a match, a valid empty result, an upstream failure and invalid input.

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

### Sprint 2 — Expand the verified core

**Sprint Goal:** Add the remaining MVP source adapters and map-based coordinate selection without weakening status semantics or provenance.

- Add sources only after the source contract and fixture are reviewed.
- Use the correct spatial operation per geometry and service (point/polygon containment, identify, or documented distance rule).
- Add interactive map click selection and coordinate-input synchronization.
- Implement place search only after D-03 is resolved.
- Add session/history persistence only after schema and privacy/retention rules are approved.
- Add per-source timeout and failure isolation; one failed provider must not erase successful results from others.

**Exit criteria:** all MVP source adapters have fixture-based contract tests; map selection drives the same API contract as coordinate input; provider failure is isolated; evidence provenance is visible.

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

1. Review and approve this documentation PR (or request corrections); it aligns the front matter with the existing v3.1 revision-history entry. Then resolve remaining schema details, geocoding, source-query and health-check contradictions.
2. GIS/backend owner verifies one source end-to-end and supplies a reviewed fixture plus source contract.
3. Backend/frontend pair implements the first vertical slice against the shared contract.
4. QA owner adds acceptance tests for match, empty result, unavailable source, unsupported source and invalid coordinates.
5. Team reviews this plan, confirms availability and updates issue owners/dependencies before committing to sprint scope.

**Project status after this plan:** planning artifact proposed; no feature is marked complete by this document. The next status update must be based on merged code and verification evidence, not this plan alone.
