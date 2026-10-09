# HazardLens Decision Log

**Status:** Proposed decisions for team review  
**Baseline:** SRS v3.1 in draft PR #9; the team must approve the baseline before it becomes canonical.  
**Rule:** A decision is not final merely because it appears in this file. Record the decision owner, date, rationale, and affected requirements when the team agrees.

## Decision register

| ID | Topic | Current proposal / known fact | Status | Decision owner / next action |
|---|---|---|---|---|
| DEC-01 | SRS version | The SRS revision history already contains a v3.1 entry dated 9 Oct 2026, while front matter and architecture/verification headers on `main` still identify v3.0. PR #9 aligns the headers. | **Pending team review** | Project lead + reviewer: approve or correct PR #9. |
| DEC-02 | Database schema and migration strategy | SRS §4.6 names 14 logical tables, including dataset, location, and comparison_investigation; issue #1 previously used hazard_dataset and omitted two tables. | **Selected direction; details pending review** | Database owner + project lead: review the full logical design, then implement migrations incrementally as the MVP needs them. Settle types, nullability, constraints, indexes, uniqueness and deletion semantics before each migration. |
| DEC-03 | Evidence status semantics | Use FOUND, NO_EVIDENCE, OUTSIDE_COVERAGE, UNAVAILABLE, UNSUPPORTED. A source error or timeout is not NO_EVIDENCE. OUTSIDE_COVERAGE requires a defensible coverage rule. | **SRS rule; source-specific verification pending** | Project lead + source owner + QA: confirm semantics against each layer. |
| DEC-04 | Geocoding interaction | User selected explicit user-submitted search plus coordinate fallback; no autocomplete against public Nominatim. Public Nominatim requires an identifying User-Agent/Referer, attribution, caching and no more than one request per second per application. | **Interaction selected; provider pending team confirmation** | Backend + frontend owners: choose the provider, document caching/rate limits/attribution and test coordinate fallback. https://operations.osmfoundation.org/policies/nominatim/ |
| DEC-05 | First delivery goal | Build a verified source → normalized API result → evidence UI vertical slice first; then integrate all required core sources before MVP sign-off. Defer AI and advanced features. | **Selected by project lead/user; team confirmation required** | Whole team: confirm at planning and agree observable exit criteria. |
| DEC-06 | MGB flood preview | PR #11 contains a limited preview adapter plus two captured response fixtures from live endpoint queries: a Central Iloilo query returned one `MF` feature, and an offshore Panay Gulf query returned an empty `features` array. The layer metadata describes polygon geometry in EPSG:3857 and `FloodSusc` classes VHF/HF/MF/LF, with no publication-date field shown. The fixtures are replayed in mocked/offline tests; they do not prove current endpoint availability, complete coverage, or that an empty response is valid `NO_EVIDENCE`. | **Metadata verified; captured live responses; coverage semantics pending** | Source owner + QA: independently repeat the query, preserve request/response provenance, verify coordinate/query behavior and coverage, and document source-date limitations. |
| DEC-07 | Health semantics | Use separate liveness and readiness behavior; optional external-source health is reported separately and does not make the API process appear dead. | **Selected direction; implementation contract pending** | Backend owner: define bounded checks, response schema and tests; team reviews before implementation. |
| DEC-08 | AI and advanced features | AI/provider work is deferred until the first evidence vertical slice is verified; required core source integrations come before MVP sign-off. | **Selected direction; team confirmation required** | Project lead + team: preserve the gate unless an explicit scope change is recorded. |
| DEC-09 | Team roles and capacity | Proposed role tracks are not confirmed assignments; current GitHub issue assignments do not prove current availability or reviewer independence. | **Open** | Whole team: confirm owners, availability and a different reviewer for every active issue. |
| DEC-10 | Schedule | Plan in relative phases first; do not invent dates before the real deadline, availability and capacity are confirmed. | **Selected planning rule; calendar schedule open** | Whole team: confirm deadline, sprint length, class/other commitments and realistic capacity before due dates are created. |
| DEC-11 | Official source candidates | Official metadata has been reviewed for MGB flood/landslide and PHIVOLCS liquefaction/active-fault candidate layers; the active-fault candidate page returned an application error on direct access. | **Metadata research only; live behavior unverified** | GIS/source owner + QA: use docs/source-verification-notes.md, verify the chosen exact layer and execute live test queries before integration. |
| DEC-12 | Requirement release classification | `docs/release-scope-and-task-matrix.md` proposes a classification for every FR/NFR. FR-11–FR-13 are proposed post-MVP candidates but are still marked Core in SRS v3.1; NFR-09 remains unresolved. | **Proposed; team decision required** | Whole team: explicitly approve or reject each proposed classification. If FR-11–FR-13 move out of MVP, update SRS and traceability in the same review cycle. |
| DEC-13 | Required source set and coverage semantics | The four named source families remain mandatory. A layer extent alone does not prove valid coverage; outside-coverage and fault-distance semantics need source-specific evidence. | **Working direction; team confirmation required** | GIS/source owner + QA: verify each source; team must explicitly approve any change to the required-source set. |

## How to close a decision

For each decision, distinguish a user/project-lead preference from a team-approved decision. Record:
- agreed outcome and alternatives rejected;
- decision owner and date;
- evidence/source consulted;
- affected SRS requirements, issues and code;
- follow-up work and how the result will be verified.
Do not mark a decision team-approved until the team explicitly confirms it.

For decisions that alter requirements, update the SRS and traceability matrix in the same review cycle. Do not treat comments in a PR as the only permanent record of a product decision.
