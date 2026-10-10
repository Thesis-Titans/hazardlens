# Contributing to HazardLens

Thank you for contributing to HazardLens. This guide defines the team's Git, GitHub, code-review, testing, and AI-assisted development practices.

The goal is simple: keep `main` stable, keep changes reviewable, and let five people work in parallel without unnecessary process.

## Table of Contents

* [1. Getting Started](#1-getting-started)
* [2. Collaboration Model](#2-collaboration-model)
* [3. Issues and Work Items](#3-issues-and-work-items)
* [4. Branch Strategy](#4-branch-strategy)
* [5. Commit Conventions](#5-commit-conventions)
* [6. Pull Request Process](#6-pull-request-process)
* [7. Code Review Standards](#7-code-review-standards)
* [8. GitHub Repository Rules](#8-github-repository-rules)
* [9. Coding Standards](#9-coding-standards)
* [10. Testing and Quality Gates](#10-testing-and-quality-gates)
* [11. Database and API Changes](#11-database-and-api-changes)
* [12. Secrets and Configuration](#12-secrets-and-configuration)
* [13. AI-Assisted Development](#13-ai-assisted-development)
* [14. Definition of Done](#14-definition-of-done)
* [15. Releases and Tags](#15-releases-and-tags)
* [16. Decision Authority & Documentation Hierarchy](#16-decision-authority--documentation-hierarchy)
* [17. Documentation Standards & Controlled Metadata](#17-documentation-standards--controlled-metadata)

---

## 1. Getting Started

### Repository access

Team members work directly in the shared GitHub repository. Forks are intended for external contributors and are not the normal workflow for the project team.

1. Make sure you have been added to the repository as a collaborator.
2. Clone the repository.
3. Follow the setup instructions in [`README.md`](README.md).
4. Verify the development environment works. `docker compose up` should start the agreed local services (`web`, `api`, `db`).
5. Read [`AGENTS.md`](AGENTS.md) before using an AI coding agent.
6. Create a branch from the latest `main` for the issue you are working on.

Example:

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/42-mgb-flood-adapter
```

If the repository uses a different bootstrap command later, update `README.md` and this guide together.

---

## 2. Collaboration Model

HazardLens uses a lightweight **GitHub Flow-style** workflow:

```text
Issue / work item
      ↓
Create branch from main
      ↓
Implement + test locally
      ↓
Pull Request
      ↓
CI checks
      ↓
1 teammate review
      ↓
Resolve feedback
      ↓
Squash merge into main
      ↓
Delete branch
```

### Core rules

1. `main` is the protected integration branch.
2. Do not push directly to `main`.
3. Meaningful feature, bug, API, database, security, or architecture work should start from a GitHub issue or existing backlog item.
4. Keep branches short-lived and focused on one coherent change.
5. Every pull request must pass required checks and receive at least one teammate approval.
6. Use squash merge for feature and fix branches.
7. Delete the branch after it is merged.
8. Humans review and approve all changes, including AI-generated code.

The repository may use GitHub Issues and GitHub Projects for planning. The project board is the team's working backlog; this file does not duplicate it.

---

## 3. Issues and Work Items

GitHub Issues are used for meaningful work, including features, bugs, technical tasks, and changes that need discussion. GitHub issue templates should be used where available.

### Create an issue before work when the change is

* a new feature;
* a bug requiring investigation;
* an API or database change;
* a security or privacy change;
* an architecture or dependency change;
* a source/integration change.

Minor documentation or maintenance edits may go directly to a pull request when their intent is obvious.

### Issue titles

Use concise, searchable titles. Include the requirement ID when useful.

```text
[FR-05] Distinguish NO_EVIDENCE from UNAVAILABLE
[AI] Add grounded investigation chat
[DB] Add investigation area geometry
[BUG] Prevent cross-session investigation access
```

### Issue content

A meaningful issue should state:

```text
## Goal

## Context / Requirement

## Acceptance Criteria
- [ ] ...
- [ ] ...

## Notes / Constraints
```

Bug reports should include reproduction steps, expected behavior, actual behavior, environment, and relevant logs or screenshots.

One issue should represent one coherent concern. Split unrelated work instead of creating a large catch-all issue.

---

## 4. Branch Strategy

HazardLens uses a single long-lived branch:

```text
main
```

All development work uses short-lived topic branches.

### Branch prefixes

| Prefix      | Use                                                 |
| ----------- | --------------------------------------------------- |
| `feat/`     | New functionality                                   |
| `fix/`      | Bug fixes                                           |
| `refactor/` | Code restructuring without intended behavior change |
| `test/`     | Test additions or test-only changes                 |
| `docs/`     | Documentation-only changes                          |
| `chore/`    | Tooling, dependencies, configuration, maintenance   |
| `perf/`     | Performance improvements                            |

Use lowercase kebab-case after the prefix. Including the GitHub issue number is recommended:

```text
feat/42-mgb-flood-adapter
fix/57-session-isolation
feat/61-ai-grounded-chat
test/73-evidence-status-contract
docs/80-api-contract
chore/84-pin-dependencies
```

### Branch rules

* Branch from the latest `main`.
* Keep branches focused and reasonably small.
* Do not keep a feature branch open for an entire sprint when it can be split into smaller pieces.
* Do not rewrite shared branches that other team members are actively using.
* Before opening or merging a PR, update the branch from `main` using the team's agreed method (`rebase` or a merge from `main`).
* Resolve conflicts on the topic branch before merge.

---

## 5. Commit Conventions

HazardLens follows **Conventional Commits 1.0.0**. The format is:

```text
<type>(<optional-scope>): <description>
```

### Allowed types

```text
feat
fix
docs
test
refactor
chore
perf
style
```

Examples:

```text
feat(adapters): add MGB flood adapter
fix(evidence): return UNAVAILABLE on upstream timeout
test(evidence): cover no-evidence status mapping
feat(ai): add grounded investigation chat
docs(api): document investigation request schema
refactor(db): simplify evidence persistence
chore(deps): pin MapLibre version
```

### Commit rules

* Keep the subject concise and specific.
* Use imperative wording where practical.
* Keep each commit focused on one logical change.
* Add a body when the reason or important context is not obvious from the subject.
* Do not put unrelated work in one commit merely because it was convenient.
* Do not commit generated secrets, local configuration, or temporary files.

Conventional Commits is a lightweight convention for human- and machine-readable commit history. It is a project convention, not a requirement imposed by Git itself.

---

## 6. Pull Request Process

Every change entering `main` goes through a pull request unless repository administration requires an emergency procedure.

### Before opening the PR

1. Make sure the branch contains only the intended work.
2. Run the relevant tests and quality checks locally.
3. Update documentation or contracts when behavior changed.
4. Update the branch from `main` and resolve conflicts.
5. Review your own diff before requesting review.

### Pull request description

Use the repository PR template. At minimum, include:

* what changed;
* why it changed;
* linked issue(s);
* affected SRS requirement(s), when applicable;
* acceptance criteria and their status;
* how the change was tested;
* screenshots or recordings for meaningful UI changes;
* database/API migration notes, when applicable;
* whether AI assistance was used.

Use GitHub closing keywords such as `Closes #42` when the PR completely resolves an issue.

### Required before merge

* [ ] CI checks pass.
* [ ] At least one teammate approves the PR.
* [ ] Review conversations are resolved.
* [ ] No known critical defect is introduced.
* [ ] Acceptance criteria are satisfied.
* [ ] Tests are added or updated when behavior changes.
* [ ] No secrets are included.
* [ ] Database/API changes are documented and tested when applicable.

### Merge method

Use **Squash and merge** for normal feature, fix, refactor, test, docs, and chore pull requests.

The goal is a readable `main` history with one meaningful commit per completed change.

---

## 7. Code Review Standards

Reviewers should focus on correctness and maintainability rather than personal coding style.

Check, in roughly this order:

1. **Correctness** — Does the change satisfy the requirement and acceptance criteria?
2. **Data meaning** — Does it preserve HazardLens evidence/status/source semantics?
3. **Security and privacy** — Does it introduce unsafe access, secrets, or unintended data exposure?
4. **Tests** — Is important new behavior covered?
5. **API/database compatibility** — Will existing consumers and migrations still work?
6. **Maintainability** — Is the solution unnecessarily complex?
7. **UX** — For frontend changes, are loading, empty, error, accessibility, and responsive states handled?

### Review comments

* Explain the problem and, when useful, the reason behind the requested change.
* Distinguish blocking issues from suggestions.
* Resolve comments after they are addressed.
* Do not use code review to redesign unrelated parts of the system.

One approval is the normal project requirement. Additional reviewers may be requested for changes involving security, database schema, source semantics, or architecture.

---

## 8. GitHub Repository Rules

The repository maintainers should configure `main` as a protected branch.

Recommended protection:

```text
Pull request required
At least 1 approving review
Required CI status checks
Require conversation resolution
Require branch to be up to date before merge (when practical)
Block force pushes
Block branch deletion
Do not allow routine bypass of protections
```

GitHub supports protected-branch rules for required reviews, status checks, conversation resolution, force-push/deletion restrictions, and related controls.

### Repository templates

Use repository-managed templates for:

```text
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── feature_request.md
│   ├── task.md
│   └── config.yml
└── PULL_REQUEST_TEMPLATE.md
```

GitHub supports issue and pull request templates to standardize the information contributors provide.

### CODEOWNERS

A small `.github/CODEOWNERS` file may identify the primary reviewer for sensitive areas such as:

```text
/api/app/ai/
/api/app/adapters/
/api/app/db/
/web/src/features/map/
```

CODEOWNERS is a reviewer-routing mechanism, not a substitute for the team's normal one-approval rule.

### Required CI checks

At minimum, the pull request workflow should validate:

```text
Backend: lint + tests
Frontend: lint + typecheck + build
```

Database migration checks should be added once the initial migration workflow is stable.

Required status checks can be enforced on protected branches.

---

## 9. Coding Standards

### Python (Backend)

* Follow PEP 8 conventions.
* Use Ruff for linting and formatting.
* Type-annotate function signatures and important variables.
* Use Pydantic for API schemas and validation.
* Use `async`/`await` for I/O-bound operations.
* Keep FastAPI routers thin; business logic belongs in services/domain code.
* Keep external-service logic inside adapters.
* Do not put database queries directly in unrelated frontend-facing logic.
* Add docstrings where public behavior would otherwise be unclear.

### TypeScript / React (Frontend)

* Use TypeScript strict mode.
* Use functional React components and hooks.
* Use TanStack Query for server state.
* Prefer the shared/generated API client/types over ad-hoc request shapes.
* Keep components focused and composable.
* Do not duplicate backend business rules in the UI when the backend is authoritative.
* Handle loading, empty, unavailable, and error states explicitly.

### General

* Prefer the simplest design that satisfies the requirement.
* Do not introduce infrastructure, dependencies, abstractions, or frameworks without a concrete need.
* Keep external service URLs and configuration outside application code.
* Pin dependencies through lockfiles.
* Never hard-code credentials or API keys.
* Follow naming and architectural rules in [`AGENTS.md`](AGENTS.md).

---

## 10. Testing and Quality Gates

Every behavior-changing PR should add or update relevant tests.

| Test category     | Purpose                                                                 |
| ----------------- | ----------------------------------------------------------------------- |
| Unit tests        | Pure logic, status mapping, validation and business rules               |
| Adapter tests     | Replay saved upstream fixtures and verify normalization                 |
| API tests         | Verify FastAPI behavior against mocked upstream services                |
| Integration tests | Verify database, migrations and major service interactions              |
| Frontend tests    | Verify important UI behavior and states                                 |
| AI contract tests | Schema validity, grounding rules, refusal behavior and tool-call limits |
| Accuracy checks   | Compare representative results with the relevant source viewers         |

### Local checks

Use the commands defined by the repository's package scripts and tooling. The initial expected checks are:

```bash
# Backend
cd api
pytest

# Frontend
cd web
npm run lint
npx tsc --noEmit
npm run build
```

Add `npm test` once a frontend test runner is configured.

### Quality gate

A PR should not merge merely because it compiles. The reviewer should confirm that the acceptance criteria are actually met.

---

## 11. Database and API Changes

### Database

* All schema changes use Alembic migrations.
* Never edit an already-applied migration.
* Test new migrations from a clean database.
* Describe schema changes in the PR.
* Resolve migration-order conflicts before merge.
* Preserve foreign-key and data-integrity rules.
* Do not silently change the meaning of stored evidence fields.

### API

* The OpenAPI contract is the source of truth for API request/response shapes.
* Breaking request, response, field, enum, or endpoint changes must be clearly identified in the PR.
* Update shared/generated frontend types when the API contract changes.
* Use consistent error responses.
* Do not let the browser provide arbitrary upstream URLs, SQL, or AI tool definitions.

---

## 12. Secrets and Configuration

Never commit:

```text
.env
API keys
Gemini/OpenRouter keys
database passwords
access tokens
private certificates
local credential files
```

Commit a safe template such as:

```text
.env.example
```

with placeholder values.

Secrets used by CI belong in GitHub's secret-management facilities rather than source control.

Before opening a PR, check the diff and staged files for accidental secrets.

---

## 13. AI-Assisted Development

AI coding agents are an approved development tool for HazardLens. They do not change the team's ownership of the codebase or its technical decisions.

### Agents may

* inspect the repository;
* implement an assigned issue;
* generate or improve tests;
* refactor code within the issue scope;
* update relevant documentation;
* help debug failing tests.

### Agents must not independently

* push directly to `main`;
* change the SRS requirements without human approval;
* change hazard evidence semantics or status meanings;
* replace an official data source without team approval;
* change database meaning without review;
* weaken security, privacy, or AI grounding rules;
* disable or bypass tests and CI;
* add major infrastructure or frameworks outside the approved architecture;
* expose or commit secrets.

### Human review requirement

AI-generated code receives the same tests and code review as human-written code.

When an agent makes a non-obvious change, the PR author should be able to explain:

* what changed;
* why it is correct;
* what tests prove it;
* what assumptions it relies on.

### Preferred agent workflow

```text
Issue + acceptance criteria
        ↓
Agent inspects repository
        ↓
Agent implements scoped change
        ↓
Agent runs tests/lint/build
        ↓
Human reviews diff and test results
        ↓
Pull Request
        ↓
CI + teammate review
        ↓
Merge
```

Use [`AGENTS.md`](AGENTS.md) as the persistent repository-level context for coding agents.

---

## 14. Definition of Done

A backlog item is **Done** when:

* [ ] its acceptance criteria are satisfied;
* [ ] implementation is complete;
* [ ] relevant tests pass;
* [ ] CI passes;
* [ ] a teammate has reviewed the change;
* [ ] required API, database, or documentation updates are complete;
* [ ] no known critical regression is introduced;
* [ ] the feature works in the agreed development environment.

For changes that affect evidence meaning, security, source selection, or architecture, explicit human approval is required.

---

## 15. Releases and Tags

Use Git tags for meaningful milestones rather than tagging every merge.

Recommended milestones:

```text
v0.1.0  Core backend / foundation
v0.2.0  Core product
v0.3.0  AI features
v1.0.0  Final project release
```

Use **Semantic Versioning** for release versions when a public/versioned release is needed. Development branches do not need release-version tags.

GitHub Releases may be used for demo/final milestones. No release automation is required for the project.

---

## 16. Decision Authority & Documentation Hierarchy

### Decision authority

Humans own decisions about:

* requirements and scope;
* evidence statuses and their semantics;
* source selection and spatial operations;
* database meaning and schema intent;
* API contracts;
* AI safety and grounding constraints;
* security and privacy;
* architecture and major dependencies.

AI coding agents assist with implementation but do not have decision authority over these areas.

When a team member is unsure, prefer the smallest change that satisfies the existing requirement and acceptance criteria. Do not introduce new architecture merely because a more elaborate solution is possible.

### Documentation authority and conflict resolution

To eliminate ambiguity when cross-document inconsistencies arise, the repository enforces an explicit source-of-truth hierarchy:

1. **System Requirements Specification (`docs/SRS.md`):** Canonical functional and non-functional requirements, unique IDs (FR-xx, NFR-xx), and system constraints (ISO/IEC/IEEE 29148:2018).
2. **Decision Log (`docs/decision-log.md`):** Formal records of architectural, engineering, and scope decisions, rationale, owners, and approval status. Decisions explain and refine implementation; they cannot silently override the SRS without an approved specification update.
3. **Release Scope and Task Matrix (`docs/release-scope-and-task-matrix.md`):** Authoritative mapping of approved requirement IDs to release classification (MVP-required vs Post-MVP), dependencies, and delivery tasks.
4. **Project Execution Plan (`docs/project-execution-plan.md`):** Defines work-package sequence, delivery gates (Gates 0 through E), role delegation proposals, and gate exit criteria.
5. **Requirements Traceability (`docs/requirements-traceability.md`):** Maps each requirement to tracking issues and verifiable acceptance evidence.
6. **Architecture and Schema Documents (`docs/architecture.md`, `docs/schema-reconciliation.md`):** Describe how requirements are realized technically (ISO/IEC/IEEE 42010:2022); they cannot unilaterally alter requirements or scope.
7. **Verification and Source-Evidence Records (`docs/verification.md`, `docs/source-verification-evidence-matrix.md`):** Living records of reproducible evidence, captured fixtures, and test results. They document observed and verified technical facts, not aspirations.
8. **Readiness Checklist and Audits (`docs/project-readiness-checklist.md`, `docs/audits/`):** Summarize outstanding work, gate prerequisites, and findings evaluated against a stated commit hash.

**Conflict resolution rule:** If an implementation detail or discussion reveals a conflict between documents, contributors must follow the higher-ranking document in this hierarchy, log the discrepancy in `docs/decision-log.md`, and obtain team approval before changing behavior.

---

## 17. Documentation Standards & Controlled Metadata

### Metadata block for controlled documents

Controlled planning and governance documents should include a standardized metadata header:

```markdown
# Document Title

**Status:** Proposed | Working Direction | Approved | Superseded  
**Owner:** Accountable role or team member  
**Baseline:** Target commit hash or approved specification version  
**Last Reviewed:** YYYY-MM-DD  
**Approval Record:** Link to meeting minutes, decision log entry, or issue  
```

### Markdown conventions

* **Headings:** One H1 per document; logical H2/H3 nesting; sentence case for new headings.
* **Formatting:** UTF-8 encoding, LF line endings, final newline.
* **Lists and tables:** Use `-` for unordered lists, numbered lists for sequential workflows. Use tables for multi-attribute comparisons and matrices.
* **Code blocks:** Always specify the syntax language (`bash`, `python`, `typescript`, `json`, `text`).
* **Dates:** Use ISO 8601 (`YYYY-MM-DD`).
* **Controlled status labels:** Distinguish *Reported* (claimed), *Observed* (inspected live), *Verified* (hermetically reproduced with evidence), and *Approved* (formally signed off).

---

## References

* GitHub Docs — Protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
* GitHub Docs — Issue and pull request templates: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests
* GitHub Docs — Status checks: https://docs.github.com/en/pull-requests/reference/status-checks
* Conventional Commits 1.0.0: https://www.conventionalcommits.org/en/v1.0.0/
