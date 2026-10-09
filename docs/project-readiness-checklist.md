# HazardLens Project Setup Readiness Checklist

**Status:** Working checklist for team review  
**Planning baseline:** SRS v3.1 proposed in PR #9; not canonical until the team reviews and merges it  
**Purpose:** Make setup completion observable. A checked box requires evidence, not an intention or a passing scaffold-only CI run.

## Exit gate

The project setup/organization phase is complete when the team has agreed on the scope and decision owners, the approved SRS/schema/source contracts are internally consistent, the backlog is traceable to requirements, team responsibilities are confirmed, and the development workflow is reproducible. This does **not** mean the application features are complete.

## Checklist

| Gate | Current status | Evidence / next action | Owner to confirm |
|---|---|---|---|
| SRS baseline | **Pending review** | PR #9 reconciles front matter and architecture/verification headers to v3.1. Team must review and merge or request changes. | Project lead + reviewer |
| MVP boundary | **Proposed** | SRS tiers exist. Team should explicitly agree that a verified source-to-API-to-UI vertical slice comes before optional AI, area analysis, weather, comparisons and report polish. | Whole team |
| Database contract | **Blocked on review** | Review `docs/schema-reconciliation.md`; settle types, nullability, uniqueness, spatial storage, retention, and deletion semantics before migrations. | Backend/database owner + project lead |
| Source contract | **Partially verified** | PR #11 checks published MGB flood layer metadata and has mocked tests. A live point-query response and coverage/empty-result semantics were not independently confirmed. Complete source verification with reproducible records before using the source as a production evidence contract. | GIS/source owner + QA |
| Other three hazard sources | **Not verified** | Confirm exact official layer/service, geometry, SRID, class/date fields, query operation, attribution, coverage and failure behavior. Capture sanitized fixtures. | GIS/source owner + QA |
| Geocoding | **Blocked by policy decision** | Issue #7's autocomplete behavior conflicts with public Nominatim policy. Choose a compliant interaction/provider and document limits, caching, attribution and fallback before implementation. | Backend + frontend owners |
| Health endpoint semantics | **Decision required** | Current `/v1/health` returns static application status. Decide whether to expose liveness and readiness separately; do not make optional hazard-provider failure appear as application death. | Backend owner + project lead |
| Requirements traceability | **Draft prepared** | Review `docs/requirements-traceability.md`; every SRS FR/NFR should point to an issue or explicitly identified backlog gap and have verifiable acceptance evidence. | Project lead + QA |
| Risks and decisions | **Draft prepared** | Review `docs/risk-register.md` and `docs/decision-log.md`; assign owners and due points at the team kickoff. | Whole team |
| Issue quality | **Partially organized** | Existing issues #1–#8 have implementation focus, but each active item needs a confirmed assignee, a different reviewer, dependencies and acceptance criteria. Do not infer availability from a proposed role table. | Project lead + issue owners |
| GitHub templates | **Proposed in PR #9** | Review the issue templates; they become available only after merged to the default branch. | Project lead |
| Git and review workflow | **Documented; enforcement not verified** | CONTRIBUTING.md describes branch/PR/review rules. Confirm repository rules actually require PRs and CI before merge; documentation alone does not enforce settings. | Repository admin |
| Local environment | **Not independently verified here** | A team member should follow README setup from a clean checkout, use a unique random `SECRET_KEY`, verify Docker Compose health, migration path and API/frontend startup; record OS and command results. | One backend + one frontend teammate |
| CI baseline | **CI exists; scope limited** | Current workflow checks backend lint/format/tests and frontend lint/type/build. Add DB/PostGIS migration integration checks when migrations exist. A green run proves only the checks it actually runs. | Backend + frontend owners |
| Sprint capacity and dates | **Team confirmation required** | Plan uses relative phases and does not invent calendar due dates. Confirm actual project start, deadline, class/other commitments, and sprint length before assigning dates. | Whole team |
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
