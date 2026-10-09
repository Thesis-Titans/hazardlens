# HazardLens — Technical Architecture

**Project:** HazardLens  
**Baseline:** SRS v3.0  
**Project type:** Web systems technology project  
**Team:** 5 students  
**Target timeline:** About 8 weeks

## 1. Purpose

This document describes the implementation architecture of HazardLens. It is intentionally lightweight and complements the SRS rather than replacing it.

The SRS defines what the system must do. This document describes how the main application components work together.

## 2. Architecture Principles

### 2.1 Evidence first, AI second

Official hazard-source data is authoritative. AI only explains and navigates retrieved evidence. Core hazard investigation continues to work when AI is unavailable.

### 2.2 Modular monolith

HazardLens uses one FastAPI backend process with clear modules for routing, business services, database access, external-source adapters and AI providers. Separate microservices, message queues and distributed infrastructure are intentionally out of scope.

### 2.3 External sources remain the source of truth

HazardLens queries the configured MGB and PHIVOLCS services instead of maintaining a national hazard-data warehouse. Returned evidence may be cached according to the source-access rules defined by the project.

### 2.4 One normalized evidence contract

Different external services use different protocols and data structures. Backend adapters convert their responses into a common normalized evidence result before the frontend consumes them.

## 3. High-Level Architecture

```text
                         ┌─────────────────────────────┐
                         │       Browser / Client      │
                         │                             │
                         │  React + TypeScript + Vite │
                         │  MapLibre + TanStack Query │
                         └──────────────┬──────────────┘
                                        │ HTTPS / JSON
                                        ▼
                         ┌─────────────────────────────┐
                         │        FastAPI Backend      │
                         │                             │
                         │ routers → services          │
                         │           ↓                 │
                         │       adapters              │
                         │           ↓                 │
                         │       AI providers          │
                         └───────┬───────────┬─────────┘
                                 │           │
                         SQL / spatial       │ HTTPS
                                 │           │
                                 ▼           ▼
                      ┌────────────────┐   ┌──────────────────────┐
                      │ PostgreSQL +   │   │ External Services    │
                      │ PostGIS        │   │                      │
                      │                │   │ MGB / PHIVOLCS       │
                      │ investigations │   │ Open-Meteo           │
                      │ evidence       │   │ Nominatim            │
                      │ AI generations │   │ Gemini / OpenRouter  │
                      │ cache          │   │ Ollama (local)       │
                      └────────────────┘   └──────────────────────┘
```

## 4. Technology Stack

| Area | Technology | Role |
|---|---|---|
| Frontend | React + TypeScript + Vite | User interface |
| Styling | Tailwind CSS | UI styling |
| Server state | TanStack Query | API fetching and cache management |
| Map | MapLibre GL JS via `react-map-gl/maplibre` | Interactive map and spatial interaction |
| Backend | FastAPI + Pydantic | REST API, validation and orchestration |
| HTTP client | HTTPX async | Concurrent upstream API requests |
| Database | PostgreSQL + PostGIS | Relational persistence and spatial data |
| ORM/migrations | SQLAlchemy 2 + Alembic | Database access and schema migration |
| AI | Gemini, OpenRouter, Ollama | Optional explanation, chat and tool calling |
| Packaging | Docker Compose | Local development and reproducible setup |

Exact dependency versions are pinned during Week 1 after checking the current official releases.

## 5. Frontend Architecture

```text
web/src/
├── api/            generated API client and shared types
├── components/     reusable UI components
├── features/
│   ├── search/     place search
│   ├── map/        map and selection
│   ├── evidence/   evidence cards and explanations
│   ├── weather/    current weather
│   ├── history/    investigation history
│   ├── comparison/ comparison interface
│   ├── report/     print/report view
│   └── ai/         AI explanation and chat
├── pages/
├── hooks/
└── lib/            configuration and formatting helpers
```

### Frontend rules

- The browser communicates with the HazardLens backend, not directly with hazard-data services.
- Evidence cards render from API data alone.
- Map failure must not prevent evidence-panel rendering.
- AI content is displayed separately from source evidence and visibly labelled as generated.
- Loading, empty, unavailable and unsupported states are explicit UI states.

## 6. Backend Architecture

```text
api/app/
├── main.py
├── config.py
├── routers/
│   ├── investigations.py
│   ├── locations.py
│   ├── datasets.py
│   ├── comparison.py
│   ├── reports.py
│   └── ai.py
├── services/
│   ├── investigation.py
│   ├── evidence.py
│   ├── comparison.py
│   ├── report.py
│   ├── weather.py
│   └── ai.py
├── adapters/
│   ├── arcgis_query.py
│   ├── arcgis_identify.py
│   ├── wms_feature_info.py
│   ├── open_meteo.py
│   └── geocoder.py
├── ai/
│   ├── base.py
│   ├── gemini.py
│   ├── openrouter.py
│   ├── ollama.py
│   └── tools.py
├── db/
│   ├── models.py
│   └── session.py
├── schemas/
└── domain/
```

### Request flow

1. A frontend request reaches a FastAPI router.
2. The router validates the request using the API schema.
3. A service performs the application-level operation.
4. The service reads/writes PostgreSQL where required.
5. Hazard services call the configured adapters concurrently.
6. Adapters query the configured external source and normalize the result.
7. The service persists the investigation/evidence snapshot.
8. The backend returns a stable API response to React.

## 7. External Source Integration

The four target hazard datasets are:

1. MGB detailed flood susceptibility
2. MGB rain-induced landslide susceptibility
3. PHIVOLCS liquefaction
4. PHIVOLCS active fault

### Access methods

| Adapter | Main use | Protocol/operation |
|---|---|---|
| `ArcGISQueryAdapter` | Queryable ArcGIS FeatureServer/MapServer layers | ArcGIS `/query` |
| `ArcGISIdentifyAdapter` | Identify/tolerance-based retrieval, including proximity behavior | ArcGIS `/identify` |
| `WmsFeatureInfoAdapter` | Map-only services | WMS `GetFeatureInfo` |
| `OpenMeteoAdapter` | Weather | Open-Meteo JSON API |
| `Geocoder` implementation | Place search | Nominatim or configured alternative |

The target source configuration is:

| Dataset | Primary candidate | Backup candidate |
|---|---|---|
| Flood | MGB detailed flood | GeoRiskPH flood WMS |
| Rain-induced landslide | MGB detailed landslide | GeoRiskPH landslide WMS |
| Liquefaction | GeoRiskPH liquefaction | Identify on same service |
| Active fault | PHIVOLCS ActiveFault identify | GeoRiskPH ActiveFault WMS |

The four listed datasets are the target. If one cannot be made to work after its backup is tested, the SRS permits replacing it with tsunami or earthquake-induced landslide so the project can still ship four working hazard datasets.

## 8. Spatial Processing

HazardLens does not impose one universal spatial rule on every dataset.

The selected spatial operation is configured per dataset and investigation type.

Typical planned behavior:

```text
Point investigation
 ├── polygon hazard → spatial relationship supported by source
 └── fault line     → proximity where supported

Area investigation
 └── use polygon query only when the source supports it
```

Unsupported operations return `UNSUPPORTED` rather than being approximated silently.

Area selections are simple polygons and are stored as spatial investigation geometry in PostGIS.

## 9. Evidence Contract

All hazard adapters return the same normalized structure.

```json
{
  "dataset_key": "flood",
  "source_key": "mgb_detailed_flood",
  "status": "FOUND",
  "result_type": "containment",
  "class_code": "HF",
  "class_label": "High Susceptibility",
  "distance_band_m": null,
  "source_date": {
    "text": "as of July 2018",
    "basis": "service_statement"
  },
  "retrieved_at": "2026-10-01T03:12:44Z",
  "origin": "live",
  "latency_ms": 840,
  "raw": {}
}
```

### Evidence statuses

- `FOUND`
- `NO_EVIDENCE`
- `OUTSIDE_COVERAGE`
- `UNAVAILABLE`
- `UNSUPPORTED`

`NO_EVIDENCE` is valid only after a successful query inside the source's published extent finds no applicable evidence. Failure or timeout is never converted into `NO_EVIDENCE`.

Source classifications remain source-scoped and are shown as published. The application does not convert them into a universal safety or hazard score.

When multiple features match at a location (per FR-09), all matching features are returned in the evidence results with their respective classifications and provenance.


## 10. Database Architecture

Core database entities:

```text
dataset
   │
   └──< dataset_source >── data_source
            │
            └──< hazard_class

session
   │
   └──< investigation >── location / selection geometry
            │
            ├──< evidence_result >── dataset_source / hazard_class
            ├──< weather_snapshot
            └──< ai_generation

geocode_cache

saved_comparison
   │
   └──< comparison_investigation >── investigation
```

### Database responsibilities

PostgreSQL/PostGIS stores:

- anonymous sessions;
- selected investigation locations and area geometry;
- investigation records;
- normalized evidence snapshots;
- source and dataset registry information;
- hazard-class definitions;
- weather snapshots;
- AI generation metadata/output;
- geocoding cache;
- saved comparison definitions.

The application does not require a national copy of the government hazard geometries.

## 11. Caching

| Data | Cache strategy |
|---|---|
| Hazard evidence | Dataset + rounded coordinate, default 24-hour TTL |
| Weather | Rounded coordinate, 15-minute TTL |
| Geocoding | Normalized query, 30-day TTL |
| AI output | Evidence hash + prompt version + provider + model |

Hazard-cache reuse is exact-key based. A nearby point is not treated as equivalent to the requested point.

## 12. AI Architecture

AI is an optional secondary layer over deterministic evidence retrieval.

```text
                 ┌───────────────┐
                 │ Evidence DB   │
                 └───────┬───────┘
                         │ structured context
                         ▼
                 ┌───────────────┐
                 │ AI Service    │
                 └───────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Gemini       OpenRouter       Ollama
```

### AI capabilities

**Advanced**

- structured evidence explanation;
- evidence-grounded chat;
- natural-language lookup through bounded tool calling.

**Stretch**

- image-assisted contextual explanation.

### Provider interface

All providers implement one small contract conceptually equivalent to:

```python
generate(messages, schema=None, tools=None)
```

Initial provider strategy:

```text
Development:  Ollama → Gemini → OpenRouter
Demo:         Gemini → OpenRouter → Ollama
Last fallback: deterministic explanation
```

Provider/model availability is checked during Week 1.

### Tool access

AI tools are allow-listed backend operations such as:

- `search_place`
- `run_investigation`
- `get_dataset_info`
- `compare`

The model has no direct SQL, shell, arbitrary HTTP or filesystem access.

The natural-language lookup loop is bounded at five tool calls.

## 13. Security Boundaries

- Browser never supplies upstream URLs.
- Browser never supplies SQL or tool definitions.
- LLM API keys remain server-side.
- CORS is restricted to the application origin.
- Session data is isolated by session identifier.
- Tool arguments are schema-validated.
- User input and external text are treated as untrusted data for AI purposes.
- AI cannot modify source classes, dates or evidence statuses.

## 14. Deployment

Local and demonstration environments use Docker Compose:

```text
web  → React application
api  → FastAPI application
db   → PostgreSQL + PostGIS
```

The project should run from a clean machine with the documented environment setup.

## 15. What Is Intentionally Not Here

HazardLens does not require:

- microservices;
- message queues;
- Kafka;
- Redis as a required dependency;
- Kubernetes;
- vector databases;
- mandatory RAG;
- custom model training;
- a national hazard-data warehouse;
- a separate AI-agent framework.

These are excluded because they do not provide enough value for the project's 5-person, 8-week scope.
