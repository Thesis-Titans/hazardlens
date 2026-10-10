# HazardLens — Agent Instructions

This file defines the conventions and constraints that all contributors and AI coding agents must follow.

## Stack

| Area | Technology |
|---|---|
| Frontend | React + TypeScript + Vite |
| Styling | Tailwind CSS |
| Server state | TanStack Query |
| Map | MapLibre GL JS via `react-map-gl/maplibre` |
| Backend | FastAPI + Pydantic |
| HTTP client | HTTPX (async) |
| Database | PostgreSQL + PostGIS |
| ORM / migrations | SQLAlchemy 2 + Alembic |
| AI providers | Gemini, OpenRouter, Ollama |
| Packaging | Docker Compose (`web`, `api`, `db`) |

## Folder Layout

### 1. Current Repository Layout (Active Baseline Scaffold)

The following structure represents the actual files present on the current `main` baseline:

```text
hazardlens/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── task.md
│   │   └── config.yml
│   ├── workflows/
│   │   └── ci.yml
│   ├── CODEOWNERS
│   └── PULL_REQUEST_TEMPLATE.md
├── api/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── adapters/
│   │   │   └── mgb_flood.py
│   │   ├── routers/
│   │   │   └── flood_preview.py
│   │   └── schemas/
│   │       └── flood_preview.py
│   ├── tests/
│   │   ├── fixtures/
│   │   │   ├── mgb_flood_iloilo_mf.json
│   │   │   └── mgb_flood_sea_empty.json
│   │   ├── test_flood_preview.py
│   │   └── test_health.py
│   ├── pyproject.toml
│   └── uv.lock
├── web/
│   ├── public/
│   │   ├── favicon.svg
│   │   └── robots.txt
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css
│   │   └── vite-env.d.ts
│   ├── package.json
│   └── vite.config.ts
├── docs/
│   ├── audits/
│   │   └── task-and-requirements-audit.md
│   ├── SRS.md
│   ├── architecture.md
│   ├── project-execution-plan.md
│   ├── release-scope-and-task-matrix.md
│   ├── requirements-traceability.md
│   ├── project-readiness-checklist.md
│   ├── agile-sprint-management-plan.md
│   ├── decision-log.md
│   ├── risk-register.md
│   ├── schema-reconciliation.md
│   ├── source-verification-notes.md
│   ├── source-verification-evidence-matrix.md
│   └── verification.md
├── scripts/
│   └── verify.sh
├── Makefile
├── docker-compose.yml
└── README.md
```

### 2. Intended Feature Layout (Planned Implementation Modules)

Modules to be created incrementally as the corresponding delivery work packages begin (do not speculative create empty modules prematurely):

```text
api/app/
├── main.py
├── config.py
├── routers/
│   ├── investigations.py      # Gate B (Task T3.1)
│   ├── locations.py           # Gate D (Task T10)
│   ├── datasets.py            # Gate C (Task T8)
│   ├── comparison.py          # Post-MVP (Task T18)
│   ├── reports.py             # Post-MVP (Task T18)
│   └── ai.py                  # Post-MVP (Task T17)
├── services/
│   ├── investigation.py
│   ├── evidence.py
│   ├── comparison.py
│   ├── report.py
│   ├── weather.py             # Gate D (Task T11)
│   └── ai.py
├── adapters/
│   ├── arcgis_query.py        # Gates A & C
│   ├── arcgis_identify.py     # Gate C (PHIVOLCS Active Fault)
│   ├── wms_feature_info.py    # Backup / secondary
│   ├── open_meteo.py          # Gate D (Task T11)
│   └── geocoder.py            # Gate D (Task T10)
├── ai/
│   ├── base.py
│   ├── gemini.py
│   ├── openrouter.py
│   ├── ollama.py
│   └── tools.py
├── db/
│   ├── models.py              # Gate D (Task T9)
│   └── session.py             # Gate D (Task T9)
├── schemas/
└── domain/

web/
├── public/
└── src/
    ├── api/                   # Generated API client and types
    ├── components/            # Reusable UI components
    ├── features/
    │   ├── search/            # Gate D: Place search
    │   ├── map/               # Gate D: MapLibre canvas & coordinate fallback
    │   ├── evidence/          # Gates B & C: Evidence cards & explanations
    │   ├── weather/           # Gate D: Weather context
    │   ├── history/           # Gate D: Investigation history
    │   ├── comparison/        # Post-MVP: Side-by-side comparison
    │   ├── report/            # Post-MVP: Print/report view
    │   └── ai/                # Post-MVP: AI explanation & grounded chat
    ├── pages/
    ├── hooks/
    └── lib/                   # Formatters, query client, config helpers
```

## Evidence Statuses

Every evidence result uses exactly one of these statuses:

| Status | Meaning |
|---|---|
| `FOUND` | Source returned one or more matching features |
| `NO_EVIDENCE` | Successful query inside source coverage found nothing |
| `OUTSIDE_COVERAGE` | Point is outside the source's published extent |
| `UNAVAILABLE` | Upstream error, timeout or network failure |
| `UNSUPPORTED` | Requested operation is not supported for this dataset/selection type |

### Critical rules

- `NO_EVIDENCE` is valid **only** after a successful query inside coverage. Errors and timeouts are **always** `UNAVAILABLE`, never `NO_EVIDENCE`.
- Source classifications are shown exactly as published. Never map them to a universal hazard scale or safety score.
- Missing evidence is never displayed as "safe."

## Naming Conventions

- **Python:** `snake_case` for modules, functions, variables. `PascalCase` for classes.
- **TypeScript:** `camelCase` for variables and functions. `PascalCase` for components and types.
- **Database:** `snake_case` for tables and columns.
- **API paths:** Lowercase without hyphens; plural nouns for resources (e.g., `/v1/investigations`, `/v1/datasets`, `/v1/comparisons`). Path parameters use snake_case (e.g., `/v1/investigations/{investigation_id}`).
- **Files:**
  - Python: lowercase with underscores (e.g., `arcgis_query.py`, `evidence_result.py`).
  - React components: `PascalCase.tsx` (e.g., `EvidenceCard.tsx`, `MapViewer.tsx`).
  - React hooks and utilities: `camelCase.ts` (e.g., `useInvestigation.ts`, `formatters.ts`).

## Verification Commands

AI agents and contributors must run these exact commands to verify code changes before submitting PRs:

### Backend (`cd api`)

- **Linting:** `ruff check .`
- **Formatting check:** `ruff format --check .`
- **Unit and contract tests:** `pytest`

### Frontend (`cd web`)

- **Linting:** `npm run lint`
- **TypeScript type checking:** `npx tsc --noEmit`
- **Production bundle build:** `npm run build`

## AI Safety Rules — Never Do

These rules are non-negotiable. Every contributor and AI agent must enforce them:

1. **The model only sees the structured evidence the backend gives it.** Never pass unvalidated external data as authoritative evidence.
2. **Missing evidence is stated as missing.** Never fill gaps from model knowledge or assumptions.
3. **The model cannot change classes, statuses or dates.** Source data is read-only for AI.
4. **Tool calls use an allow-list** (`search_place`, `run_investigation`, `get_dataset_info`, `compare`). No model access to SQL, shell, arbitrary HTTP or filesystem.
5. **Outputs are schema-validated.** Invalid structured output retries once, then falls back to deterministic explanation.
6. **All AI text carries a "generated" label.** AI content is always visually distinguished from source evidence.
7. **User prompts, tool results and source text are untrusted data.** They cannot override grounding rules, tool allow-lists or safety constraints.

## Security Boundaries

- The browser never supplies upstream URLs, SQL or tool definitions.
- LLM API keys remain server-side only.
- CORS is restricted to the application origin.
- Session data is isolated by session identifier.
- Tool arguments are schema-validated before execution.
- The natural-language lookup loop is bounded at 5 tool calls.

## AI Coding Agent Scope & Boundaries

HazardLens uses AI coding assistants as a development force multiplier. All AI coding assistants working in this repository must operate strictly within these boundaries (aligned with [CONTRIBUTING.md](CONTRIBUTING.md)):

### Agents May

- Inspect code, documentation, and tests across the repository.
- Implement assigned GitHub issues and their acceptance criteria.
- Write, update, and run unit, integration, and contract tests.
- Refactor code within the scope of the assigned issue.
- Update relevant documentation and comments.
- Assist in debugging failing tests and build errors.

### Agents Must NOT Independently

- Push or merge directly to `main`.
- Redesign architecture or alter SRS requirements without explicit human approval.
- Change hazard-data semantics, evidence statuses, or status transition rules.
- Replace or omit official government hazard data sources.
- Modify database schemas without review and proper Alembic migrations.
- Weaken security boundaries, CORS policies, or AI grounding rules.
- Disable, skip, or bypass automated tests and CI workflows.
- Add external infrastructure (e.g., Redis, Kafka, Celery, microservices).
- Expose or commit secrets or API keys.

### Human Responsibility

- Humans own all core decisions: requirements, architecture, data meaning, source selection, database semantics, security, AI safety, and merge approval.
- AI-generated code is subject to the same review standards and testing rigor as human-written code.
- The AI agent is an implementation multiplier, not the project decision-maker.

## General Rules

- Write the contract first: database models, normalized result schema and the OpenAPI spec.
- Save real service responses as fixtures so adapter tests run offline.
- One feature per branch, one small pull request, tests required.
- Humans review every merge.
- Humans own decisions: statuses, source choices, AI safety rules, and anything that touches data meaning.
