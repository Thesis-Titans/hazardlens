# HazardLens

[![CI](https://github.com/Thesis-Titans/hazardlens/actions/workflows/ci.yml/badge.svg)](https://github.com/Thesis-Titans/hazardlens/actions/workflows/ci.yml)

A web application where a user picks a place in the Philippines and sees what official hazard datasets say about it: flood, landslide, liquefaction and active faults. Results appear on an interactive map and in an evidence panel, with an AI assistant that explains and answers questions about them.

**Evidence first, AI second.** Official source data is authoritative. AI only explains and navigates it. The app never says "safe" because data is missing, and it keeps working when AI is down.

## Features

### Core

- Place search and map click to select a point
- Hazard lookup across four datasets, run in parallel
- Evidence panel with clear states: found, no evidence, outside coverage, unavailable, unsupported
- Anonymous investigation history (no login required)
- Side-by-side comparison of past investigations
- Printable evidence report
- Deterministic plain-language explanation
- Current weather card

### Advanced

- AI explanation with structured output
- AI chat grounded in the current investigation
- Natural-language lookup via tool calling
- Area investigation with polygon drawing

### Stretch

- Map hazard overlays
- Image input for contextual explanation
- Additional hazard datasets (tsunami, earthquake-induced landslide)

## Datasets

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

### Development

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

HazardLens is developed by **Thesis Titans** (West Visayas State University — BSIT Batch 2028) using lightweight Scrum and GitHub Flow.

- **Organization:** [Thesis Titans](https://github.com/Thesis-Titans)
- **Sprint Board:** [HazardLens — Sprint Board](https://github.com/orgs/Thesis-Titans/projects/1)
- **Sprint Milestones:** [HazardLens Milestones](https://github.com/Thesis-Titans/hazardlens/milestones)

### Team Tracks & Specializations

| Track | Engineers | Focus & Ownership |
|---|---|---|
| **Data & AI Infrastructure** | `@markalvincadangin`<br>`@vincenttamano` | FastAPI, PostGIS, ArcGIS/WMS adapters, AI Grounding Engine |
| **Interactive GIS** | `@Justin-Ardena` | MapLibre GL map viewport, vector layers, pin reverse-geocoding |
| **Product UI/UX & QA** | `@lovelii-me`<br>`@faithbn` | Design system, comparison view, print reports, evidence card QA |

## Standards Adopted

HazardLens adheres to established industry and engineering standards to keep the team aligned without bureaucracy:

| Area | Standard / Practice |
|---|---|
| Requirements | ISO/IEC/IEEE 29148:2018-aligned principles |
| Development | Lightweight Agile / Scrum-inspired (GitHub Projects) |
| Version control | Git + GitHub Flow (`main` protected, branch per issue) |
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

## Disclaimer

HazardLens is a web-systems technology practice project. It is **not** an official hazard assessment. Source data is retrieved from government services and displayed as published. Absence of evidence does not mean absence of hazard.
