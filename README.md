# HazardLens

[![CI](https://github.com/Thesis-Titans/hazardlens/actions/workflows/ci.yml/badge.svg)](https://github.com/Thesis-Titans/hazardlens/actions/workflows/ci.yml)

A web application planned to help users explore what official hazard datasets report about a selected place in the Philippines, covering flood, landslide, liquefaction and active faults.

**Current status:** HazardLens is an early prototype scaffold. Live hazard lookups, verified official-source integrations, investigation history, evidence panels, weather and AI features are not yet implemented. The feature lists below describe intended scope, not capabilities available in the current prototype. The release boundary and proposed FR/NFR classifications are still pending team approval; see the [release scope and dependency-aware task matrix](docs/release-scope-and-task-matrix.md).

**Evidence first, AI second.** The intended design treats official source data as evidence and AI as an optional explanation layer. Missing or unavailable data must never be presented as proof of safety.

## Features

### MVP Core (Release Scope — Gates A through E)

- Point location selection via Philippine place search and map click fallback (FR-01, FR-14)
- Concurrent point hazard query across four official datasets with failure isolation (FR-03, FR-05, FR-06)
- Transparent evidence panel with 5 strict statuses, exact published labels, and provenance (FR-04, FR-07, FR-08, FR-09)
- Deterministic plain-language explanation without LLM reliance (FR-10)
- Anonymous session persistence and 30-day investigation history (FR-02)
- Current weather card with bounded timeout and independent failure isolation (FR-13, FR-21)
- Security & compliance: No HazardHunterPH scraping, rate limits, HttpOnly cookies, WCAG 2.2 AA accessibility (NFR-04, NFR-05, NFR-11, NFR-13, NFR-16)

### Post-MVP (Deferred Scope — Working Direction)

- Side-by-side comparison of past investigations without synthetic scoring (FR-11 / Issue #14)
- Printable hazard briefing summary with attribution and watermarking (FR-12 / Issue #14)
- Simple area investigation with polygon validation and capability gates (FR-20 / Issue #16)
- Gated AI explanations, grounded chat, and tool calling (FR-15–FR-19 / Issue #4; strictly gated behind Gates B & C)

### Stretch Goals (Future Exploration)

- Map hazard layer vector/raster overlays
- Multimodal image input for contextual explanation
- Additional hazard datasets (tsunami, earthquake-induced landslide)

## Datasets

The following are candidate official datasets for integration; their live querying, coverage and interpretation must be verified before the application presents results.

| Dataset | Agency |
|---|---|
| Flood susceptibility | MGB |
| Rain-induced landslide susceptibility | MGB |
| Liquefaction | PHIVOLCS |
| Active fault | PHIVOLCS |

## Stack

| Area | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS, TanStack Query |
| Map | MapLibre GL JS via `react-map-gl/maplibre` |
| Backend | FastAPI, Pydantic, HTTPX (async) |
| Database | PostgreSQL with PostGIS |
| ORM | SQLAlchemy 2, Alembic |
| AI | Gemini, OpenRouter, Ollama |
| Packaging | Docker Compose |

## Project Structure

```text
hazardlens/
├── api/                 Backend (FastAPI)
│   └── app/
│       ├── routers/     API endpoints
│       ├── services/    Business logic
│       ├── adapters/    External source integrations
│       ├── ai/          AI provider interface
│       ├── db/          Database models and session
│       ├── schemas/     API schemas
│       └── domain/      Domain types
├── web/                 Frontend (React + Vite)
│   ├── public/          Static assets (favicon, robots.txt)
│   └── src/
│       ├── api/         Generated API client
│       ├── components/  Reusable UI components
│       ├── features/    Feature modules
│       ├── pages/       Page components
│       ├── hooks/       Custom hooks
│       └── lib/         Utilities and config
├── docs/                Project documentation
│   ├── SRS.md           Software requirements specification
│   ├── architecture.md  Technical architecture
│   └── verification.md  Verification record
├── docker-compose.yml   Container orchestration
├── AGENTS.md            AI agent instructions
├── CONTRIBUTING.md      Contribution guidelines
└── README.md            This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (version pinned in `.nvmrc`)
- Python 3.12+ (version pinned in `pyproject.toml`)

### Setup

```bash
# Clone the repository
git clone https://github.com/Thesis-Titans/hazardlens.git
cd hazardlens

# Copy environment template and configure keys if needed
cp .env.example .env

# Start all services
docker compose up
```

The application will be available at:

- **Frontend:** http://localhost:5173
- **API:** http://localhost:8000
- **API docs:** http://localhost:8000/docs

### Development & Verification Commands

HazardLens provides a root [Makefile](Makefile) and [scripts/verify.sh](scripts/verify.sh) to unify developer and CI workflows matching [AGENTS.md](AGENTS.md):

```bash
# Run full verification suite before pushing (backend lint, format check, tests; frontend lint, typecheck, build)
make verify

# Run individual verification targets
make verify-backend   # ruff check, ruff format --check, pytest
make verify-frontend  # eslint, tsc --noEmit, npm run build

# Auto-format Python backend code
make format

# Local development services
make dev-db           # Start PostGIS container
make dev-api          # Start FastAPI dev server on port 8000
make dev-web          # Start Vite dev server on port 5173
```

Manual development workflow:

```bash
# Backend
cd api
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd web
npm install
npm run dev
```

## Team & Agile Project Management

HazardLens is developed by **Thesis Titans** (West Visayas State University — BSIT Batch 2028) using a proposed lightweight Scrum-based Agile workflow and GitHub Flow; the sprint cadence and roles require whole-team confirmation.

- **Organization:** [Thesis Titans](https://github.com/Thesis-Titans)
- **Sprint Board:** [HazardLens — Sprint Board](https://github.com/orgs/Thesis-Titans/projects/1)
- **Delivery Gate Milestones:** [HazardLens Milestones](https://github.com/Thesis-Titans/hazardlens/milestones)

### Team Tracks & Specializations

| Track | Engineers | Focus & Ownership |
|---|---|---|
| **Data & AI Infrastructure** | `@markalvincadangin`<br>`@vincenttamano` | FastAPI, PostGIS, ArcGIS/WMS adapters, AI Grounding Engine |
| **Interactive GIS** | `@Justin-Ardena` | MapLibre GL map viewport, vector layers, pin reverse-geocoding |
| **Product UI/UX & QA** | `@Lovelly143` (previously referenced as `@lovelii-me` in existing backlog text)<br>`@faithbn` | Design system, comparison view, print reports, evidence card QA |

## Standards Adopted

HazardLens adheres to established industry and engineering standards to keep the team aligned without bureaucracy:

| Area | Standard / Practice |
|---|---|
| Requirements | ISO/IEC/IEEE 29148:2018-aligned principles |
| Development | Lightweight Agile / Scrum-inspired (GitHub Projects) |
| Version control | Git + GitHub Flow (PRs and branch-per-task; repository enforcement must be verified by an admin) |
| Commit messages | [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) (`feat:`, `fix:`, etc.) |
| API | OpenAPI (auto-generated by FastAPI) |
| Database | PostgreSQL + PostGIS + Alembic migrations |
| Code quality | Ruff, pytest (Backend) / ESLint, TypeScript strict mode (Frontend) |
| CI | GitHub Actions |
| Releases | Semantic Versioning |

For team workflow rules, pull request expectations, and AI agent boundaries, see [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md).

## Documentation

- [Software Requirements Specification](docs/SRS.md)
- [Technical Architecture](docs/architecture.md)
- [Verification Record](docs/verification.md)
- [Project Execution Plan](docs/project-execution-plan.md)
- [Agile and Sprint Management Plan](docs/agile-sprint-management-plan.md)
- [Release Scope and Dependency-Aware Task Matrix](docs/release-scope-and-task-matrix.md)
- [Project Setup Readiness Checklist](docs/project-readiness-checklist.md)
- [Requirements Traceability](docs/requirements-traceability.md)
- [Decision Log](docs/decision-log.md)
- [Risk Register](docs/risk-register.md)
- [Database Schema Reconciliation](docs/schema-reconciliation.md)
- [Official Source Verification Notes](docs/source-verification-notes.md)
- [Official Source Verification Evidence Matrix](docs/source-verification-evidence-matrix.md)

## Documentation Authority & Governance by Domain

To prevent ambiguity when resolving discrepancies across planning and technical files, HazardLens governs authority strictly by domain (detailed in [CONTRIBUTING.md](CONTRIBUTING.md#documentation-authority-by-domain)):

- **Requirements & Constraints:** [`docs/SRS.md`](docs/SRS.md) (governs requirements, IDs, and constraints)
- **Decisions & Rationale:** [`docs/decision-log.md`](docs/decision-log.md) (governs trade-offs & approvals; cannot override SRS)
- **Release Placement:** [`docs/release-scope-and-task-matrix.md`](docs/release-scope-and-task-matrix.md) (governs MVP vs Post-MVP boundaries)
- **Delivery Sequence & Gates:** [`docs/project-execution-plan.md`](docs/project-execution-plan.md) (governs gate prerequisites and exit criteria)
- **Traceability:** [`docs/requirements-traceability.md`](docs/requirements-traceability.md) (governs requirement-to-evidence mappings)
- **Technical Design:** [`docs/architecture.md`](docs/architecture.md) & [`docs/schema-reconciliation.md`](docs/schema-reconciliation.md) (governs technical architecture & schemas)
- **Empirical Evidence & Fixtures:** [`docs/verification.md`](docs/verification.md) & [`docs/source-verification-evidence-matrix.md`](docs/source-verification-evidence-matrix.md) (governs observed test results & proof; cannot be overridden by planning documents)
- **Baseline Health & Audits:** [`docs/project-readiness-checklist.md`](docs/project-readiness-checklist.md) & [`docs/audits/`](docs/audits/task-and-requirements-audit.md) (governs commit-specific audit findings)

## Disclaimer

HazardLens is a web-systems technology practice project, not an official hazard assessment. The planned application may display data from government services after integrations and source behavior are verified. The current prototype does not yet provide live hazard results. Absence of evidence does not mean absence of hazard or indicate safety.
