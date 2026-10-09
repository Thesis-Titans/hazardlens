# HazardLens Project Setup Readiness Checklist

**Status:** Working checklist for team review  
**Planning baseline:** SRS v3.1 proposed in PR #9; not canonical until the team reviews and merges it  
**Purpose:** Make setup completion observable. A checked box requires evidence, not an intention or a passing scaffold-only CI run.

## Exit gate

The project setup/organization phase is complete when the team has explicitly approved scope and decision owners, the SRS/schema/source contracts are internally consistent, the backlog is traceable, team responsibilities and reviewers are confirmed, GitHub enforcement is checked, and clean-checkout setup is reproducible. The user's selected options are a working plan, not team approval. This does **not** mean application features are complete.

## Checklist

| Gate | Current status | Evidence / next action | Owner to confirm |
|---|---|---|---|
| SRS baseline | **Pending review** | PR #9 reconciles front matter and architecture/verification headers to v3.1. SRS front matter now explicitly says “Proposed review baseline — pending team approval.” Team must review and merge or request changes. | Project lead + reviewer |
| MVP boundary | **Project-lead working direction recorded; team confirmation pending** | First deliver one verified source → API → evidence UI slice; then integrate all four required sources. FR-11/FR-12/FR-20 are post-MVP; FR-13/FR-21 are MVP-required; AI is gated until the first slice and all four sources are verified. FR-02 persistence/history must ship before MVP release, though it need not be in the first slice. No source replacement without explicit team-approved scope change. | Whole team |
| Database contract | **Logical strategy selected; schema details pending** | Review the full 14-table logical design, but implement migrations incrementally as the MVP requires. Settle types, nullability, uniqueness, spatial storage, indexes, retention and deletion semantics before each migration. | Backend/database owner + project lead |
| Source contract | **Partial verification: two captured MGB flood responses; coverage semantics pending** | PR #11 records a Central Iloilo response with one `MF` feature and an offshore Panay Gulf response with an empty `features` array. Regression tests replay both captured payloads offline. This is evidence of the captured responses, not proof of current service availability, full coverage, or valid `NO_EVIDENCE` semantics. Independently repeat the query and verify each official source before integration. Keep fixtures clearly labelled as recorded data. | GIS/source owner + QA |
| Other three hazard sources | **Metadata candidates researched; live behavior not verified** | docs/source-verification-notes.md records candidate official MGB landslide, PHIVOLCS liquefaction and active-fault layers. The ActiveFaultGeneric page returned an ArcGIS application error during this review. Confirm exact layer, geometry/SRID, class/date fields, query operation, attribution, coverage and failure behavior; capture sanitized fixtures and separately record live checks. | GIS/source owner + QA |
| Geocoding | **Interaction selected; provider pending** | Use explicit user-submitted search, not autocomplete against public Nominatim. Preserve coordinate entry/map selection when geocoding is unavailable. If public Nominatim is used, implement its identifying User-Agent, caching, attribution and max 1 request/second/app. | Backend + frontend owners |
| Health endpoint semantics | **Direction selected; contract pending** | Separate liveness and readiness. Optional external source health must be reported separately and must not make the API process appear dead. Specify bounded checks and test behavior. | Backend owner + project lead |
| Requirements traceability | **Draft prepared** | Review `docs/requirements-traceability.md`; every SRS FR/NFR should point to an issue or explicitly identified backlog gap and have verifiable acceptance evidence. | Project lead + QA |
| Risks and decisions | **Draft prepared** | Review `docs/risk-register.md` and `docs/decision-log.md`; assign owners and due points at the team kickoff. | Whole team |
| Issue quality | **Partially organized** | Existing issues #1–#8 have implementation focus, but each active item needs a confirmed assignee, a different reviewer, dependencies and acceptance criteria. Do not infer availability from a proposed role table. | Project lead + issue owners |
| GitHub templates | **Proposed in PR #9** | Review the issue templates; they become available only after merged to the default branch. | Project lead |
| Git and review workflow | **Documented; enforcement not verified** | CONTRIBUTING.md describes branch/PR/review rules. Confirm repository rules actually require PRs and CI before merge; documentation alone does not enforce settings. | Repository admin |
| Local environment | **Not independently verified here** | A team member should follow README setup from a clean checkout, use a unique random `SECRET_KEY`, verify Docker Compose health, migration path and API/frontend startup; record OS and command results. | One backend + one frontend teammate |
| CI baseline | **CI exists; PR #11 latest reported run passed; scope limited** | The run linked from PR #11 commit `873fabf` reports backend Ruff lint/format and 11 tests passing, plus frontend lint, TypeScript and production build. This is branch CI evidence only; it does not establish live-source repeatability, source coverage semantics, database migration readiness, or merge approval. Add DB/PostGIS migration integration checks when migrations exist. | Backend + frontend owners |
| Sprint capacity and dates | **Relative schedule selected; team confirmation required** | Keep phases relative. Confirm actual start/deadline, each student's availability, class/other commitments and sprint length before assigning calendar dates or due dates. | Whole team |
| Board/milestones | **Not verified through the available repo actions** | README links to the organization project and milestones. Verify the board is active, issue fields/statuses match the team's workflow, and milestone dates reflect real capacity. | Project lead / board owner |

## Recommended kickoff (30–45 minutes)

1. Confirm the project goal and the core-versus-advanced boundary.
2. Review and decide the open items in `docs/decision-log.md`.
3. Review the schema reconciliation before anyone writes a migration.
4. Confirm issue owners, reviewers, blockers and the first sprint goal.
5. Confirm the repository rules and run the clean-checkout setup.
6. Record decisions in GitHub/this repository; do not leave decisions only in chat.

## Rules for updating this checklist

- Use `PASS` only when evidence is linked or recorded.
- Use `BLOCKED` when a decision, access, dependency or upstream behavior prevents work.
- Use `PARTIAL` when only a limited slice has been verified.
- Use `NOT VERIFIED` rather than guessing.
- Revisit this checklist at the start of each sprint and whenever the SRS or source contract changes.


## Additional tracked gates

- [ ] Verify the project-lead working definition of NFR-09 through [issue #19](https://github.com/Thesis-Titans/hazardlens/issues/19): register and query a compatible test/mock dataset without a schema migration; keep whole-team approval pending until confirmed.
- [ ] Complete the clean-checkout and repository-rule evidence in [issue #20](https://github.com/Thesis-Titans/hazardlens/issues/20); a CI pass alone does not satisfy this gate.
