# HazardLens Project Execution Plan

**Status:** Project-lead working direction approved on 9 October 2026; formal team review and baseline approval pending  
**Repository baseline:** `main` (incorporating PR #11 MGB flood preview slice and SRS v3.1)  
**Planning basis:** SRS v3.1; [Release Scope and Task Matrix](release-scope-and-task-matrix.md); [Source Verification Evidence Matrix](source-verification-evidence-matrix.md); GitHub issues #1–#8 and #12–#20  
**Scope:** Requirements alignment, delivery sequencing, team delegation, verification, and milestone gates  

> **Evidence Grounding Rule:** This plan is a working agreement proposal, not evidence that any feature is implemented. Do not mark requirements complete until the implementation and its verifiable acceptance evidence are present.

---

## 1. Current Baseline and Recovery Objective

HazardLens has a React/Vite/TypeScript frontend scaffold, a FastAPI application, PostGIS Docker configuration, and verified CI checks. PR #11 added a bounded MGB flood preview API/adapter, status normalization, truncation safeguards, and offline fixture regression tests on `main`.

While the flood preview adapter and mocked fixtures are in place, live-source repeatability and coverage boundaries remain pending under Gate A and Issue #2. The full investigation journey—location selection, multi-source orchestration, persistence, session isolation, and evidence UI—remains to be delivered and proven by code and tests.

**Recovery objective:** Deliver one small, reliable, end-to-end hazard investigation vertical slice first (Gate B). Expand to multi-source orchestration (Gate C) and complete MVP workflows (Gate D) only after the source queries, result semantics, API contracts, UI rendering, and offline tests all work together.

---

## 2. Working Scope Boundary

| Scope Area | Working Direction |
|---|---|
| **First Delivery Slice** | One verified source (MGB Flood) → normalized API result → evidence UI card (Gates A & B). |
| **Required MVP Hazard Sources** | MGB flood, MGB rain-induced landslide, PHIVOLCS liquefaction, PHIVOLCS active faults (Gate C). |
| **MVP Workflows after First Slice** | Multi-source orchestration, session history/persistence, place search & map fallback, weather with failure isolation, rate limits, and accessibility (Gate D). |
| **AI Integration** | Gated until the first slice and all four sources are verified; final release placement requires whole-team confirmation (Post-MVP / Gate E). |
| **Post-MVP Candidates** | FR-11 comparison, FR-12 printable report, FR-20 polygon/area investigation. |
| **Extensibility (NFR-09)** | A compatible new dataset must be addable through one adapter and registry configuration without a schema migration, demonstrated through normal orchestration. |

---

## 3. Delivery Principles

1. **Evidence before AI:** Hazard facts and classifications come from official sources. AI is an optional explanation layer, never the authority.
2. **One end-to-end slice before breadth:** First make one verified source work through API → normalized result → UI → tests.
3. **Unknown is not safe:** Distinguish `FOUND`, `NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, and `UNSUPPORTED`. A timeout or source error must never become `NO_EVIDENCE`.
4. **No invented source semantics:** Use source-supported spatial operations. Do not apply point-in-polygon to line data or infer hazard probability from mere proximity without a documented rule.
5. **Deterministic core, optional integrations:** The core investigation must work without AI, geocoding, or weather.
6. **Small reviewed changes:** One issue per branch where practical; pull requests must describe evidence, tests, risks, and limitations.
7. **Honest status reporting:** Distinguish implemented, tested, blocked, deferred, and not started. CI passing on fixtures is not live-source verification.
8. **No unsupported completion claims:** Never close an issue based solely on code being written; require acceptance criteria and reproducible evidence.

---

## 4. Delivery Sequence and Exit Criteria

Delivery is organized into six dependency-ordered gates rather than premature calendar dates:

```
[ Gate 0: Planning, Governance & Delegation Baseline ]
                       │
                       ▼
[ Gate A: First-Source Verification & Contract ]
                       │
                       ▼
[ Gate B: First End-to-End Evidence Slice ]
                       │
                       ▼
[ Gate C: Verify Complete Required Source Set ]
                       │
                       ▼
[ Gate D: Complete Remaining MVP Workflows & Safeguards ]
                       │
                       ▼
[ Gate E: MVP Acceptance & Gated Extensions ]
```

### Gate 0 — Planning, Governance and Delegation Baseline
Establish the shared delivery baseline, standardize all backlog issues, settle team invitations and role delegations, and ensure no implementation begins without clear acceptance criteria and independent reviewer pairings.

**Exit criteria:**
- Polished project execution plan, task matrix, and traceability baseline are accepted.
- All 17 active backlog issues are formatted using the Section 8 standard structure with explicit lead implementers and independent reviewers (`Author != Reviewer`).
- Pending organization invitations are accepted so GitHub native assignees match the delegation matrix.
- Verification commands (`ruff`, `pytest`, `eslint`, `tsc`, `vite build`) pass hermetically on `main`.
- **Zero feature implementation code is executed until Gate 0 is formally closed.**

### Gate A — First-Source Verification and Contract
Verify the chosen first source (MGB Flood Susceptibility) for the intended point-query operation, record request/response evidence, and establish how the application represents matches, empty results, errors, and truncation.

**Exit criteria:**
- Exact service and layer identity, geometry, CRS, query parameters, fields, and class definitions are recorded in `docs/source-verification-evidence-matrix.md`.
- Fresh request evidence includes timestamp, parameters, HTTP status, latency, and sanitized response.
- Query behavior is independently repeated across test sessions.
- Empty-result and coverage semantics are either verified or conservatively represented as `UNAVAILABLE`.
- Deterministic tests cover success, empty response, timeout, malformed payload, and truncation.

### Gate B — First End-to-End Evidence Slice
Complete the first usable workflow through the API and UI using the verified source contract from Gate A, keeping the slice small enough to test end-to-end.

**Exit criteria:**
- Coordinates can be submitted through the initial input path.
- API returns a documented, normalized evidence contract matching SRS v3.1.
- Frontend UI renders the source result, original classification, provenance, and limitations.
- All five evidence states are handled without conflating source failure with a negative finding.
- Deterministic plain-language explanation works without AI.
- Recorded fixtures are labelled honestly; core test suite runs completely offline.
- End-to-end workflow and failure cases have reproducible verification evidence.
- *Persistence is not required for this first slice.*

### Gate C — Verify Complete Required Source Set
Independently verify and integrate all four mandatory source families through the agreed orchestration and normalization contract.

**Exit criteria:**
- MGB flood and rain-induced landslide layers are verified.
- PHIVOLCS liquefaction and active-fault layers are verified.
- Each source has evidence for geometry, CRS, fields, classification, spatial operation, attribution, source-date limitations, and failure behavior.
- Source-specific coverage and empty-result semantics are documented; no unsupported coverage claims are made.
- One source's failure does not suppress valid findings from other sources.
- Multiple matches and differing source classifications are preserved rather than reduced to a synthetic universal score.
- Integration tests exercise successful and failed source combinations.

### Gate D — Complete Remaining MVP Workflows and Safeguards
Deliver required product behavior that was intentionally excluded from the first slice.

**Exit criteria:**
- Investigation history and anonymous session isolation work with required persistence, 30-day retention, and cross-session access denial.
- Place search and map/coordinate fallback support the agreed location workflow without public Nominatim autocomplete.
- Weather is displayed separately from hazard evidence, with bounded timeout and failure isolation.
- API rate limits (HTTP 429) and privacy-safe diagnostics (no raw IPs or secrets) are verified.
- Attribution and planning-data disclaimers are present throughout the relevant UI.
- Accessibility (keyboard, screen reader announcements) and supported-browser checks have recorded results.
- NFR-09 passes a compatible mock-dataset test through normal orchestration without a schema migration.
- Required PostGIS migrations and session-isolation behavior have automated verification.

### Gate E — MVP Acceptance and Gated Extensions
Confirm that the implementation matches team-approved requirements and that all MVP acceptance evidence is traceable.

**Exit criteria:**
- Every MVP requirement maps to a completed task and reproducible acceptance evidence in `docs/requirements-traceability.md`.
- Clean-checkout setup, migrations, frontend/backend startup, and CI pass hermetically.
- Source provenance, known gaps, and limitations are documented accurately.
- Whole team reviews release readiness and explicitly accepts remaining risks.
- AI work starts only after Gates B and C pass, with final release placement confirmed by the team.
- Comparison/reporting and polygon investigation remain deferred unless the team explicitly changes scope.

---

## 5. Evidence and Status Rules Across All Phases

| Result Status | Permitted Interpretation | Invariant Rule |
|---|---|---|
| **`FOUND`** | A relevant feature was returned and validated. | Preserves official source classifications verbatim (`VHF`, `HF`, `MF`, `LF`, etc.). Never maps to a universal score. |
| **`NO_EVIDENCE`** | The query succeeded within verified survey coverage and returned no relevant features. | **Valid only inside verified coverage.** Errors, timeouts, and unmapped areas must never become `NO_EVIDENCE`. |
| **`OUTSIDE_COVERAGE`** | A defensible source-supported coverage rule establishes that the location is outside the covered area. | Cannot be inferred from a broad service bounding box alone. |
| **`UNAVAILABLE`** | The source failed, timed out, returned malformed/truncated data, or the empty result cannot be interpreted reliably. | Upstream outages, 5xx errors, timeouts, or unverified survey boundaries default to `UNAVAILABLE`. |
| **`UNSUPPORTED`** | The requested operation cannot be performed by that source or is not supported by the implementation. | Applied when geometry operations (e.g. area polygon) are not supported by the layer. |

---

## 6. Product Task Breakdown (T1–T18)

| Task | Deliverable / Task Scope | Depends On | Completion Evidence | Target Gate | Mapped Issue |
|:---:|---|:---:|---|:---:|:---:|
| **T1** | Verify first source (MGB Flood) and document live contract | Source selection | Complete request record, repeatability evidence, documented result semantics, offline fixtures | **Gate A** | **[#2](https://github.com/Thesis-Titans/hazardlens/issues/2)** |
| **T2** | Finalize first-slice API and evidence response contract | T1 | Reviewed Pydantic schema, status definitions, provenance fields, and contract tests | **Gate B** | **[#3](https://github.com/Thesis-Titans/hazardlens/issues/3)** |
| **T3** | Implement first investigation endpoint and evidence UI | T2 | Reproducible end-to-end test from coordinate input to rendered evidence card | **Gate B** | **[#3](https://github.com/Thesis-Titans/hazardlens/issues/3)** |
| **T4** | Implement deterministic explanations and honest empty states | T2–T3 | Unit/UI tests proving explanations require no AI and do not invent findings | **Gate B** | **[#3](https://github.com/Thesis-Titans/hazardlens/issues/3)** |
| **T5** | Verify MGB rain-induced landslide source | T1 procedure | Complete source evidence record, live query verification, and source-specific fixtures | **Gate C** | **[#2](https://github.com/Thesis-Titans/hazardlens/issues/2)** |
| **T6** | Verify PHIVOLCS liquefaction source | T1 procedure | Exact layer identity, live query record, classifications, coverage, and failure semantics | **Gate C** | **[#2](https://github.com/Thesis-Titans/hazardlens/issues/2)** |
| **T7** | Verify PHIVOLCS active-fault source | T1 procedure | Exact layer identity, geometry-appropriate spatial operation, query record, and distance semantics | **Gate C** | **[#2](https://github.com/Thesis-Titans/hazardlens/issues/2)** |
| **T8** | Integrate four verified sources through normal orchestration | T1, T5–T7, T2 | Concurrent-query tests, bounded deadlines, partial-failure isolation, and multi-match preservation | **Gate C** | **[#6](https://github.com/Thesis-Titans/hazardlens/issues/6)** |
| **T9** | Implement required persistence and anonymous session history | Logical schema review | Migration tests, history retrieval, retention/expiry tests, and cross-session isolation tests | **Gate D** | **[#1](https://github.com/Thesis-Titans/hazardlens/issues/1)** / **[#13](https://github.com/Thesis-Titans/hazardlens/issues/13)** |
| **T10** | Implement full location workflow (Search + Map fallback) | T2–T3, provider decision | Place search, coordinate/map fallback, validation, attribution, and provider-failure tests | **Gate D** | **[#5](https://github.com/Thesis-Titans/hazardlens/issues/5)** / **[#7](https://github.com/Thesis-Titans/hazardlens/issues/7)** |
| **T11** | Add independent weather context | Core investigation API | Weather success and failure tests prove hazard evidence is completely unaffected | **Gate D** | **[#15](https://github.com/Thesis-Titans/hazardlens/issues/15)** |
| **T12** | Implement API rate limits and privacy-safe diagnostics | API contracts | HTTP 429 tests, bounded behavior, and log review for secrets/raw IP exposure | **Gate D** | **[#17](https://github.com/Thesis-Titans/hazardlens/issues/17)** |
| **T13** | Complete evidence provenance, attribution, and disclaimers | Evidence UI & contracts | Page-level review, disclaimer banner, and automated checks where practical | **Gate D** | **[#8](https://github.com/Thesis-Titans/hazardlens/issues/8)** |
| **T14** | Complete accessibility and supported-browser acceptance | Main MVP workflows | Keyboard/focus/contrast checks, automated accessibility scan, and browser/device matrix | **Gate D** | **[#18](https://github.com/Thesis-Titans/hazardlens/issues/18)** |
| **T15** | Demonstrate compatible-source extensibility (NFR-09) | T8 orchestration | A mock dataset is registered via adapter + registry configuration and queried without schema migration | **Gate D** | **[#19](https://github.com/Thesis-Titans/hazardlens/issues/19)** |
| **T16** | Complete MVP release verification and readiness gates | T1–T15 | Requirement traceability, clean-checkout test, migrations, CI evidence, and team sign-off | **Gate E** | **[#12](https://github.com/Thesis-Titans/hazardlens/issues/12)** / **[#20](https://github.com/Thesis-Titans/hazardlens/issues/20)** |
| **T17** | Begin gated AI implementation spike (if approved for release) | Gates B & C passing | Structured evidence grounding, schema validation, bounded tool use, fallback, and provenance tests | **Post-MVP** | **[#4](https://github.com/Thesis-Titans/hazardlens/issues/4)** |
| **T18** | Implement comparison, printable report & polygon investigation | Explicit post-MVP planning | Separate scope and acceptance criteria; no dependency blocking core MVP | **Post-MVP** | **[#14](https://github.com/Thesis-Titans/hazardlens/issues/14)** / **[#16](https://github.com/Thesis-Titans/hazardlens/issues/16)** |

---

## 7. Team Responsibilities & Peer-Review Delegation Matrix

Every task pairs a Lead Implementer with an Independent Peer Reviewer across our three specialized tracks to ensure code review integrity (`Author != Reviewer`):

| Track | Engineers | Primary Ownership |
|---|---|---|
| **Data & AI Infrastructure** | `@markalvincadangin`, `@vincenttamano` | FastAPI, PostGIS, ArcGIS/WMS adapters, AI Grounding Engine |
| **Interactive GIS & Geolocation** | `@Justin-Ardena` | MapLibre GL map viewport, vector layers, pin reverse-geocoding |
| **Product UI/UX & QA Testing** | `@lovelii-me`, `@faithbn` | Design system, comparison view, print reports, evidence card QA, accessibility |

### Delegation Pairing Table

| Task | Title | Lead Implementer | Independent Reviewer | Target Milestone |
|:---:|---|:---:|:---:|---|
| **T1** | MGB Flood verification | `@markalvincadangin` | `@vincenttamano` | Gate A & B |
| **T2** | Evidence response contract | `@markalvincadangin` | `@vincenttamano` | Gate A & B |
| **T3** | First vertical slice API & UI | `@vincenttamano` (API)<br>`@lovelii-me` (UI) | `@markalvincadangin` (API)<br>`@faithbn` (UI) | Gate A & B |
| **T4** | Deterministic explanation | `@vincenttamano` | `@markalvincadangin` | Gate A & B |
| **T5** | MGB Landslide verification | `@markalvincadangin` | `@vincenttamano` | Gate C |
| **T6** | PHIVOLCS Liquefaction verification | `@vincenttamano` | `@markalvincadangin` | Gate C |
| **T7** | PHIVOLCS Active Fault verification | `@Justin-Ardena` | `@markalvincadangin` | Gate C |
| **T8** | Multi-source adapter orchestration | `@vincenttamano` | `@markalvincadangin` | Gate C |
| **T9** | PostGIS schema & session history | `@vincenttamano` | `@markalvincadangin` | Gate D |
| **T10** | Map viewer & geocoding search | `@Justin-Ardena` | `@lovelii-me` | Gate D |
| **T11** | Weather failure isolation | `@markalvincadangin` | `@vincenttamano` | Gate D |
| **T12** | API rate limits & safe diagnostics | `@vincenttamano` | `@markalvincadangin` | Gate D |
| **T13** | Provenance, attribution & disclaimers | `@lovelii-me` | `@faithbn` | Gate D |
| **T14** | Accessibility & browser acceptance | `@faithbn` | `@lovelii-me` | Gate D |
| **T15** | NFR-09 compatible-source extensibility | `@markalvincadangin` | `@vincenttamano` | Gate D |
| **T16** | MVP release verification & readiness | Whole Team | `@markalvincadangin` | Gate E |
| **T17** | Gated AI evaluation spike | `@markalvincadangin` | `@vincenttamano` | Post-MVP |
| **T18** | Comparison, report & polygon area | `@lovelii-me` / `@Justin-Ardena` | `@faithbn` | Post-MVP |

---

## 8. Standard Acceptance Criteria Structure

All implementation issues must adhere to this standardized structure:

```markdown
## Purpose
What user need or requirement does this task satisfy?

## Scope
- Included: [Specific bounded deliverables]
- Excluded: [Explicitly out of scope]

## Dependencies
Which verified contract, decision, or earlier deliverable must exist first?

## Team Delegation
- Lead Implementer: @[username]
- Independent Reviewer: @[username]

## Acceptance Criteria
- [ ] Observable expected behavior under normal operation
- [ ] Explicit behavior for errors, timeouts, or empty results
- [ ] Provenance, security, or accessibility requirements
- [ ] Clear conditions for success and failure

## Verification Evidence
Required automated tests, reproducible test runs, or manual evidence.

## Completion Rule
Do not close until criteria pass and verifiable evidence is attached. Passing CI alone is insufficient.
```

---

## 9. Definition of Ready & Definition of Done

### Definition of Ready (DoR)
An issue is ready to start only when:
- Its requirement and approved SRS version are identified.
- Acceptance criteria are testable and cover failure/empty cases.
- External source, schema, and API assumptions are stated.
- Dependencies are complete or explicitly managed.
- The lead implementer and independent reviewer are confirmed.

### Definition of Done (DoD)
A feature is done only when:
- [ ] Acceptance criteria are met in code.
- [ ] Unit/contract/integration tests cover success, empty, and failure cases.
- [ ] Tests run deterministically offline using recorded fixtures.
- [ ] Linting, type checking, and production build pass.
- [ ] API contracts and documentation match actual behavior.
- [ ] No secrets or raw IP addresses are introduced into storage or logs.
- [ ] Attribution, source provenance, and limitations are displayed.
- [ ] An independent reviewer other than the author has reviewed and approved the change.
- [ ] Verification evidence is linked before closing the issue.
