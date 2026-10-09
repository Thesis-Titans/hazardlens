# HazardLens Project Setup Readiness Checklist

**Status:** Working checklist for team review  
**Planning baseline:** SRS v3.1 merged on `main` (PR #9); pending formal whole-team kickoff confirmation  
**Purpose:** Make setup completion observable. A checked box requires evidence, not an intention or a passing scaffold-only CI run.

## Exit gate

The project setup/organization phase (Gate 0, Issue #12) is complete when the team has explicitly approved scope and decision owners, the SRS/schema/source contracts are internally consistent, the backlog is traceable, team responsibilities and reviewers are confirmed, GitHub enforcement is checked, and clean-checkout setup is reproducible. Additional feature implementation work is strictly paused until Gate 0 closes. Gate 0 is a governance prerequisite, not a delivery task in T1–T18; T16 is reserved for Gate E release verification (Issue #20). Issue #1 is an architectural foundation for Gate D persistence and does not block the stateless Gate B slice.

## Checklist

| Gate | Current status | Evidence / next action | Owner to confirm |
|---|---|---|---|
| SRS baseline | **Merged on `main`; team confirmation pending** | PR #9 merged on `main`, reconciling front matter and architecture/verification headers to v3.1. SRS front matter explicitly notes merged review baseline. Whole-team confirmation pending. | Project lead + reviewer |
| MVP boundary | **Project-lead working direction recorded; team confirmation pending** | First deliver one verified source → API → evidence UI slice; then integrate all four required sources. FR-11/FR-12/FR-20 are post-MVP; FR-13/FR-21 are MVP-required; AI is gated until the first slice and all four sources are verified. FR-02 persistence/history must ship before MVP release, though it need not be in the first slice. No source replacement without explicit team-approved scope change. | Whole team |
| Database contract | **Logical strategy selected; schema details pending** | Review the full 14-table logical design, but implement migrations incrementally as the MVP requires. Settle types, nullability, uniqueness, spatial storage, indexes, retention and deletion semantics before each migration. | Backend/database owner + project lead |
| Source contract | **Partial verification: two captured MGB flood responses; coverage semantics pending** | PR #11 is merged on `main`, recording a Central Iloilo response with one `MF` feature and an offshore Panay Gulf response with an empty `features` array. Regression tests replay both captured payloads offline. This is evidence of the captured responses, not proof of current service availability, full coverage, or valid `NO_EVIDENCE` semantics. Independently repeat the query and verify each official source before integration under Gate A. Keep fixtures clearly labelled as recorded data. | GIS/source owner + QA |
| Other three hazard sources | **Metadata candidates researched; live behavior not verified** | `docs/source-verification-notes.md` records candidate official MGB landslide, PHIVOLCS liquefaction and active-fault layers. The ActiveFaultGeneric page returned an ArcGIS application error during this review. Confirm exact layer, geometry/SRID, class/date fields, query operation, attribution, coverage and failure behavior; capture sanitized fixtures and separately record live checks under Gate C. | GIS/source owner + QA |
| Geocoding | **Interaction selected; Geoapify working selection** | Use explicit user-submitted search, not autocomplete against public Nominatim. Preserve coordinate entry/map selection when geocoding is unavailable. Geoapify selected as working MVP provider with server-side key containment; if public Nominatim is used as alternative, implement its identifying User-Agent, caching, attribution and max 1 request/second/app. | Backend + frontend owners |
| Health endpoint semantics | **Direction selected; contract pending** | Separate liveness and readiness. Optional external source health must be reported separately and must not make the API process appear dead. Specify bounded checks and test behavior. | Backend owner + project lead |
| Requirements traceability | **Draft prepared; FR-10 mapped to #3** | Review `docs/requirements-traceability.md`; every SRS FR/NFR points to an issue or explicitly identified backlog gap and has verifiable acceptance evidence. | Project lead + QA |
| Risks and decisions | **Draft prepared; DEC-18 added** | Review `docs/risk-register.md` and `docs/decision-log.md`; assign owners and due points at the team kickoff. | Whole team |
| Issue quality | **Standardized to Section 8 format** | All 17 active backlog issues standardized with Purpose, Scope, Dependencies, Delegation, Acceptance Criteria, Verification Evidence, and Completion Rule. Team availability remains to be confirmed; the project lead reports that only two organization invitations remain pending. Verify the current organization roster and invitation list before Gate 0 closure. | Project lead + issue owners |
| GitHub templates | **Merged on `main`** | Issue templates merged to `main` via PR #9 and active in repository. | Project lead |
| Git and review workflow | **Verified active on `main`** | Verified via GitHub REST API (`/branches/main/protection`): 1 approving review required (`required_approving_review_count = 1`), strict status checks requiring `backend` and `frontend` CI jobs, force pushes and branch deletions disabled. Recorded on Issue #12. Formal team sign-off pending kickoff. | Repository admin |
| Local environment | **Not independently verified here** | A team member should follow README setup from a clean checkout, use a unique random `SECRET_KEY`, verify Docker Compose health, migration path and API/frontend startup; record OS and command results. | One backend + one frontend teammate |
| CI baseline | **CI active and hermetic** | CI runs on `main` and PR branches verify backend Ruff lint/format check, 11 pytest tests, frontend ESLint, TypeScript tsc strict mode, and Vite production bundle build. This is branch CI evidence; it does not establish live-source repeatability or source coverage semantics. Add DB/PostGIS migration integration checks when migrations exist. | Backend + frontend owners |
| Agile/Sprint operating agreement | **Proposed; whole-team approval pending** | Review `docs/agile-sprint-management-plan.md`; confirm Product Owner/facilitator, Sprint length, team availability, and the Sprint Planning / progress inspection / Review / Retrospective cadence. Delivery gates are not Sprints. | Whole team |
| Sprint capacity and dates | **Relative schedule selected; team confirmation required** | Keep phases relative. Confirm actual start/deadline, each student's availability, class/other commitments and sprint length before assigning calendar dates or due dates. Do not create calendar commitments before confirmation. | Whole team |
| Board/milestones | **Milestones organized by Gates 0–E** | README links to the organization project and milestones. Board reflects Delivery Gates without arbitrary calendar dates. | Project lead / board owner |

## Recommended kickoff (30–45 minutes)

1. Confirm the project goal and the core-versus-advanced boundary.
2. Review and decide the open items in `docs/decision-log.md`.
3. Review the schema reconciliation before anyone writes a migration.
4. Review the Agile/Sprint Management Plan; confirm the Sprint length, facilitator, available capacity, issue owners/reviewers, blockers and the first Sprint Goal.
5. Confirm the repository rules and run the clean-checkout setup.
6. Record decisions in GitHub/this repository; do not leave decisions only in chat.

## Rules for updating this checklist

- Use `PASS` only when evidence is linked or recorded.
- Use `BLOCKED` when a decision, access, dependency or upstream behavior prevents work.
- Use `PARTIAL` when only a limited slice has been verified.
- Use `NOT VERIFIED` rather than guessing.
- Revisit this checklist at the start of each Sprint and whenever the SRS or source contract changes.
- Use the current GitHub login `@Lovelly143` for the teammate previously referenced as `@lovelii-me` in project notes; the project lead reports that two other organization invitations remain pending. Verify live organization state before marking invitation work complete.


## Additional tracked gates

- [ ] Verify the project-lead working definition of NFR-09 through [issue #19](https://github.com/Thesis-Titans/hazardlens/issues/19): register and query a compatible test/mock dataset without a schema migration; keep whole-team approval pending until confirmed.
- [ ] Complete the clean-checkout and repository-rule evidence in [issue #20](https://github.com/Thesis-Titans/hazardlens/issues/20); a CI pass alone does not satisfy this gate.
