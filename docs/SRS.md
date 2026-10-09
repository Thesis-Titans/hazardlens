# HazardLens

## Project Specification

| | |
|---|---|
| **Version** | 3.1 |
| **Date** | 9 October 2026 |
| **Status** | Build baseline |
| **Supersedes** | v3.0 |
| **Project type** | Web systems technology project (React, APIs, database, AI) |
| **Team and timeline** | 5 students, about 8 weeks, with AI coding agents as a force multiplier |

---

## 1. Overview

### 1.1 What it is

HazardLens is a web app where a user picks a place in the Philippines and sees what official hazard datasets say about it: flood, landslide, liquefaction and active faults. Results appear on an interactive map and in an evidence panel, with an AI assistant that explains and answers questions about them.

### 1.2 Goals

1. Deliver a polished, modern product that looks like a real app, not a data viewer.
2. Show solid web engineering: React frontend, REST API, relational database with geospatial support, external API integration, and resilience when those APIs fail.
3. Deliver advanced AI features that use free services: evidence explanation, evidence-grounded chat, and natural-language lookup through tool calling.
4. Stay buildable by five students in eight weeks.

### 1.3 Core principle

**Evidence first, AI second.** Official source data is authoritative. AI only explains and navigates it. The app never says "safe" because data is missing, and it keeps working when AI is down.

### 1.4 Out of scope

Hazard forecasting, personal risk scores, user accounts, training custom models, a national data warehouse, microservices, message queues, vector databases and agent frameworks. HazardLens is not an official hazard assessment.

### 1.5 Constraints and assumptions

- The project is a web-systems technology practice project, not a research study.
- The implementation target is five students over about eight weeks, using AI coding agents as a development force multiplier.
- Free or zero-cost services are preferred for development and demonstration. External free-tier quotas, model availability and service terms may change.
- Government hazard services are external dependencies and may be slow, unavailable, modified or removed without notice.
- No authentication is required for the MVP. Anonymous sessions are sufficient for history and comparisons.
- HazardLens shall not bulk-replicate or host government hazard geometries unless the applicable source permits it in writing.
- AI is an enhancement layer. Core hazard retrieval and evidence presentation shall function without an AI provider.

---

## 2. Features

| Tier | Feature |
|---|---|
| **Core** | Place search and map click to select a point |
| **Core** | Hazard lookup across four datasets, run in parallel, each with source, class, date and status |
| **Core** | Evidence panel with clear states for found, no evidence, outside coverage, unavailable, unsupported |
| **Core** | Anonymous investigation history stored in PostgreSQL |
| **Core** | Compare two or more past investigations side by side |
| **Core** | Printable evidence report (print-styled page, save as PDF from the browser) |
| **Core** | Deterministic plain-language explanation built from source class definitions |
| **Core** | Current weather card (separate from hazard evidence) |
| **Advanced** | AI explanation of the investigation, with structured output |
| **Advanced** | AI chat grounded in the current investigation ("What does this class mean?") |
| **Advanced** | Natural-language lookup: "Is there a fault near Jaro, Iloilo?" The AI calls approved backend tools to search the place and fetch evidence |
| **Advanced** | Draw a simple polygon on the map and query datasets whose APIs support polygon queries. The UI states clearly when a dataset does not support area queries |
| **Stretch** | Map hazard overlays |
| **Stretch** | Image input: upload a photo of a site and ask about it, grounded in the evidence |
| **Stretch** | Tsunami and earthquake-induced landslide datasets |

**Datasets (core four):** MGB flood susceptibility, MGB rain-induced landslide susceptibility, PHIVOLCS liquefaction, PHIVOLCS active fault.

---

## 3. Requirements

### 3.1 Functional

| ID | Requirement |
|---|---|
| FR-01 | The user can select a location by place search or map click. Coordinates are validated and rounded to 5 decimals. |
| FR-02 | Each lookup is saved as an investigation in the database and appears in the session's history. No login is required. |
| FR-03 | A lookup queries all active datasets concurrently under one deadline (default 10 seconds). One dataset failing never fails the lookup. |
| FR-04 | Each result has one status: `FOUND`, `NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, or `UNSUPPORTED`. |
| FR-05 | `NO_EVIDENCE` is returned only after a successful query inside the source's coverage finds nothing. Errors and timeouts are `UNAVAILABLE`, never `NO_EVIDENCE`. |
| FR-06 | Each dataset shall use a configured spatial operation appropriate to its geometry and the selected investigation type. Point and area queries may use different operations. Fault-line datasets shall use proximity where supported. Area queries shall use only operations supported by the source; otherwise the result is `UNSUPPORTED`. |
| FR-07 | Each result shows agency, dataset, source class and definition, source date text, retrieval time, whether live, cached or recorded, and attribution. |
| FR-08 | Source class labels are shown as published. The app never maps them to a universal hazard scale or safety score. |
| FR-09 | If a point matches several features, all material matches are kept. If two sources disagree, both are shown. |
| FR-10 | The app builds a deterministic explanation from stored class definitions and states what is missing. |
| FR-11 | The user can compare two or more past investigations side by side. The comparison never produces a ranking. |
| FR-12 | The user can open a print-styled report with context, findings, provenance, limitations and the AI summary (if any), labelled as not an official assessment. |
| FR-13 | The app shows current weather for the point, visually separate from hazard evidence. |
| FR-14 | The evidence panel renders from API data alone, so it still works if map tiles or the geocoder fail. |
| FR-15 | AI explanation uses only structured evidence supplied by the backend and returns a validated JSON schema. |
| FR-16 | AI chat answers using the current investigation as context and refuses to invent hazard facts it was not given. |
| FR-17 | Natural-language lookup runs a bounded tool-calling loop (maximum 5 tool calls) over an allow-list of backend functions. |
| FR-18 | Every AI output is visually labelled as generated and stores provider, model, prompt version, evidence hash and time. |
| FR-19 | If AI fails or hits quota, the app falls back to the next provider, then to the deterministic explanation. Core evidence never depends on AI. |
| FR-20 | An area investigation shall accept a valid simple polygon within the supported study area. Invalid, self-intersecting, empty or excessively large polygons shall be rejected with a controlled validation error. The implementation shall use a configurable vertex and area limit. |
| FR-21 | If the weather service fails, the app shall show an `UNAVAILABLE` weather state without failing, altering or suppressing the hazard investigation. |

### 3.2 Non-functional

| ID | Requirement |
|---|---|
| NFR-01 | A cached lookup returns in under 1 second. A live lookup finishes or times out within the deadline. |
| NFR-02 | Each upstream call has a timeout and one retry on timeout or 5xx. No retry on 4xx. |
| NFR-03 | Upstream URLs come only from configuration or the dataset registry. The browser cannot supply URLs, SQL or AI tool definitions. |
| NFR-04 | CORS allows only the app's origin. LLM keys stay on the server. |
| NFR-05 | Sessions use a random ID in an `HttpOnly` cookie. Raw IP addresses are not stored. Investigations expire after 30 days. |
| NFR-06 | Geocoding follows the Nominatim policy: 1 request per second, identifying User-Agent, caching, no autocomplete. Users are told not to enter home addresses. |
| NFR-07 | Recorded demo fixtures exist for several Iloilo points and are clearly labelled when used. |
| NFR-08 | Every page shows source attribution and a limitation statement: maps are long-term planning data, not personal safety determinations, and absence of data does not mean safety. |
| NFR-09 | A new dataset needs one small adapter plus registry rows, with no schema change. |
| NFR-10 | Dependencies are pinned in lockfiles. The API contract is generated from the backend and shared with the frontend. |
| NFR-11 | HazardHunterPH is not scraped, embedded or framed. |
| NFR-12 | A session shall access only investigations and comparisons associated with that session. An investigation identifier alone shall not grant access to another session's data. |
| NFR-13 | Public endpoints that trigger upstream services, especially investigation and AI endpoints, shall use configurable application-level rate limits and return HTTP 429 when exceeded. |
| NFR-14 | Each AI provider call shall have a configurable timeout. Timeout, transport failure, rate limiting, unavailable model, or invalid structured output may trigger the configured fallback provider. |
| NFR-15 | User-provided text, tool results and external source content shall be treated as untrusted data and shall not override the AI grounding rules, tool allow-list or safety constraints. |
| NFR-16 | The application shall support keyboard navigation, visible focus states, accessible labels and status messaging, and shall target WCAG 2.2 AA expectations where practical for the prototype. |
| NFR-17 | The prototype shall support the latest two major versions of Chrome, Edge and Firefox, with responsive operation on common mobile viewport sizes. |
| NFR-18 | Server logs shall record enough information to diagnose a request without storing raw IP addresses, including request/investigation ID, dataset/source, status, latency and relevant error type. |

---

## 4. Design

### 4.1 Stack

| Area | Choice | Why |
|---|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS, TanStack Query | Fast to build and well known to AI coding agents |
| Map | MapLibre GL JS via `react-map-gl/maplibre` | Free, no token, supports overlays and drawing |
| Backend | FastAPI, Pydantic, HTTPX (async) | Concurrent upstream calls, automatic OpenAPI |
| Database | PostgreSQL with PostGIS, JSONB for raw payloads | Real relational model plus spatial types in one product |
| ORM | SQLAlchemy 2 and Alembic | Migrations and typed models |
| AI | Small provider interface: Gemini, OpenRouter, Ollama | Replaceable, with fallback chain |
| Packaging | Docker Compose: `web`, `api`, `db` | One-command setup |

Architecture is a **modular monolith**: one backend process with clear folders for routers, services, adapters and AI. Pin exact versions during Week 1 from the official sources.

### 4.2 Architecture

```text
Browser (React + MapLibre)
        | HTTPS / JSON
        v
FastAPI  routers -> services -> adapters
        |                |-- MGB / PHIVOLCS ArcGIS services
        |                |-- Open-Meteo, Nominatim
        |                '-- AI providers (Gemini / OpenRouter / Ollama)
        v
PostgreSQL + PostGIS
```

### 4.3 Backend layout

```text
api/app/
  main.py  config.py
  routers/     investigations, locations, datasets, comparison, reports, ai
  services/    investigation, evidence, comparison, report, weather, ai
  adapters/    arcgis_query, arcgis_identify, wms_feature_info, open_meteo, geocoder
  ai/          base, gemini, openrouter, ollama, tools
  db/          models, session
  schemas/  domain/
```

### 4.4 Source adapters

Three access methods cover all datasets. Each adapter returns the same normalized result.

| Adapter | Use |
|---|---|
| ArcGIS query | Layer `/query` with a point or polygon geometry |
| ArcGIS identify | `/identify` with a tolerance, useful for proximity |
| WMS GetFeatureInfo | For map-only services. Use `CRS:84` to avoid the lat/lon axis-order trap |

**Candidate sources** (service existence and published capabilities checked in October 2026; actual application-level live retrieval and response parsing are validated in the Week 1 test):

| Dataset | Primary candidate | Backup candidate |
|---|---|---|
| Flood | MGB detailed flood service (ArcGIS query) | GeoRiskPH Flood service (WMS) |
| Rain-induced landslide | MGB detailed landslide service (identify) | GeoRiskPH landslide service (WMS) |
| Liquefaction | GeoRiskPH Liquefaction layer (ArcGIS query) | Identify on the same service |
| Active fault | PHIVOLCS ActiveFault service (identify with tolerance bands) | GeoRiskPH ActiveFault (WMS) |

**Target:** MGB flood, MGB rain-induced landslide, PHIVOLCS liquefaction and PHIVOLCS active fault.

**Contingency:** if one of these cannot be made to work after its backup candidate is tried, replace it with tsunami or earthquake-induced landslide so the project still ships four working hazard datasets. The swap is a fallback, not a free choice of hazards.

**Spatial operation registry.** Each dataset source shall declare the supported operation for each selection type. The initial target is: polygon intersection/containment for flood, rain-induced landslide and liquefaction; proximity/tolerance for active faults; and source-supported polygon operations only for area investigations. Exact operations and boundary behavior are confirmed in Week 1. A published service extent is only an extent precheck; being inside that extent does not guarantee that a feature exists at the selected location.

### 4.5 Normalized evidence result

```json
{
  "dataset_key": "flood",
  "source_key": "mgb_detailed_flood",
  "status": "FOUND",
  "result_type": "containment",
  "matches": [
    {
      "class_code": "HF",
      "class_label": "High Susceptibility",
      "distance_band_m": null
    }
  ],
  "source_date": { "text": "as of July 2018", "basis": "service_statement" },
  "retrieved_at": "2026-10-01T03:12:44Z",
  "origin": "live",
  "latency_ms": 840,
  "raw": {}
}
```

A single evidence result represents the query evaluation for one dataset source.
- **Invariant:** `FOUND` requires a non-empty `matches` array (up to a configurable cap, default 20). All other statuses (`NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, `UNSUPPORTED`) require an empty `matches: []` array.
- **Deterministic ordering:** Matches are ordered deterministically (first by `class_code`, then by `distance_band_m` ascending) to ensure stable evidence hashes for AI prompt caching.
- **Coverage extent:** The service's coverage extent is stored per source. A point outside it returns `OUTSIDE_COVERAGE` without a network call. Source dates are stored as text plus a basis, because services publish dates as integers or free text.
- **Multiple matches & sources (FR-09):** When a location intersects multiple features within a dataset source (such as multiple nearby fault traces), all matching features are preserved in `matches[]`. When multiple candidate sources are queried or disagree, each source produces its own distinct `EvidenceResult`.

### 4.6 Data model

| Table | Key columns |
|---|---|
| `dataset` | key, name, description |
| `data_source` | agency, attribution, terms_url |
| `dataset_source` | dataset (FK), source (FK), access_path, base_url, layer, extent, priority, active, last_checked |
| `hazard_class` | dataset_source (FK), code, label, definition_text |
| `location` | geography point, snapped lat and lon |
| `session` | id, created_at, expires_at |
| `investigation` | location nullable, session (FK ON DELETE CASCADE), selection_type (`POINT`/`AREA`), geometry, created_at, duration_ms |
| `evidence_result` | investigation (FK ON DELETE CASCADE), dataset_source (FK), status, source_date_text, retrieved_at, origin, latency_ms, raw (jsonb) |
| `evidence_match` | evidence_result (FK ON DELETE CASCADE), hazard_class (FK), distance_band_m |
| `weather_snapshot` | investigation (FK ON DELETE CASCADE), temperature, humidity, precipitation, wind, valid_time |
| `ai_generation` | investigation (FK ON DELETE CASCADE), kind, provider, model, prompt_version, evidence_hash, output, created_at |
| `geocode_cache` | normalized_query, response, expires_at |
| `saved_comparison` | session (FK ON DELETE CASCADE), name, created_at |
| `comparison_investigation` | comparison (FK ON DELETE CASCADE), investigation (FK ON DELETE CASCADE), position |

For an area investigation, `investigation.geometry` stores the user-drawn polygon as the canonical selection geometry. `selection_type` identifies whether the geometry represents a point or area. The polygon is validated before upstream queries. The initial implementation limit is configurable; the default maximum is 100 vertices.

### 4.7 Caching and lifecycle

Hazard results are cached by dataset and rounded coordinate for 24 hours (this can be extended after agency permission). Weather is cached for 15 minutes. Geocoding is cached for 30 days. Cache reuse is exact-key only, because a nearby point may sit in a different polygon. Hazard and weather cache lookups reuse existing `evidence_result` and `weather_snapshot` records within their active TTL windows, requiring no dedicated cache tables or external Redis store.

**Data lifecycle (NFR-05):** Session data and geocode cache records expire after 30 days. Cleanup is handled via an in-process scheduled task or startup hook in FastAPI that deletes records where `expires_at < NOW()`, triggering `ON DELETE CASCADE` across child investigation and evidence records without external worker infrastructure.

### 4.8 API

| Method | Path | Purpose | Router |
|---|---|---|---|
| POST | `/v1/investigations` | Create a point or area investigation | `investigations.py` |
| GET | `/v1/investigations` | Session history | `investigations.py` |
| GET | `/v1/investigations/{investigation_id}` | One investigation with evidence | `investigations.py` |
| POST | `/v1/comparisons` | Compare investigation ids and create saved comparison | `comparison.py` |
| GET | `/v1/comparisons` | List saved comparisons for current session | `comparison.py` |
| GET | `/v1/comparisons/{comparison_id}` | Retrieve saved comparison details | `comparison.py` |
| GET | `/v1/investigations/{investigation_id}/report` | Report data | `reports.py` |
| GET | `/v1/geocode?q=` | Cached place search | `locations.py` |
| GET | `/v1/datasets` | Sources, dates, coverage | `datasets.py` |
| POST | `/v1/ai/explain` | AI explanation for an investigation | `ai.py` |
| POST | `/v1/ai/chat` | Grounded Q&A | `ai.py` |
| POST | `/v1/ai/lookup` | Natural-language lookup via tools | `ai.py` |
| GET | `/v1/health` | Database and source status | `main.py` |

#### API contract minimum

Investigation requests use either a point or a polygon:

```json
{
  "selection_type": "POINT",
  "latitude": 10.72,
  "longitude": 122.56
}
```

```json
{
  "selection_type": "AREA",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[122.55, 10.70], [122.57, 10.70], [122.57, 10.72], [122.55, 10.72], [122.55, 10.70]]]
  }
}
```

AI endpoints reference an existing investigation and load its evidence from the server-side database. The browser shall not supply authoritative evidence directly to the AI endpoints. Errors use one shape:

```json
{
  "error": {
    "code": "UNAVAILABLE",
    "message": "The requested upstream source is currently unavailable."
  }
}
```

Important API error codes include `INVALID_INPUT`, `NOT_FOUND`, `UNAVAILABLE`, `RATE_LIMITED`, `UNSUPPORTED` and `FORBIDDEN`.

The server is authoritative for AI context: `/v1/ai/explain`, `/v1/ai/chat` and `/v1/ai/lookup` identify the investigation or location through server-side records and never accept client-supplied authoritative hazard evidence.

### 4.9 Frontend

Single-page layout: search bar and map on one side, evidence panel on the other, weather card, history drawer, comparison view and report page. Evidence cards use clear status chips and a footer showing source, date and live or cached origin. AI content sits in its own labelled panel.

---

## 5. AI Design and Feasibility

### 5.1 Verdict

**All planned AI features have a viable zero-cost development and demo path, using free-tier hosted models and/or local Ollama inference.** Availability, quotas, model capabilities and terms may change, so AI is designed as replaceable and non-critical.

| Provider | What it gives for free | Limits to plan around |
|---|---|---|
| **Gemini API** (Google AI Studio) | Selected free-tier models support function calling, structured JSON output and image input. Verify the exact model and current quota in AI Studio during Week 1 | Per-project rate limits that vary by model, from tens to about 1,500 requests/day. Quotas change often. Free-tier prompts may be used to improve Google products |
| **OpenRouter** | Free-model variants (`:free`), many with tool calling and structured output | Roughly 50 requests/day without credit, models come and go |
| **Ollama** (local) | Unlimited local use, tool calling, structured output, vision models | Needs a laptop with enough RAM. Tool-calling reliability depends on the local model, so test at least one tool-capable model in Week 1. Slower than hosted |

Check current model names and quotas in AI Studio and the OpenRouter model list in Week 1. Do not hard-code any model in the schema or API.

### 5.2 Feature feasibility

| Feature | Feasibility | Notes |
|---|---|---|
| Evidence explanation (JSON) | High | Small prompt, structured output, validated with Pydantic |
| Grounded chat | High | Context is the investigation's evidence rows. Short answers |
| Natural-language lookup (tool calling) | High | Tools: `search_place`, `run_investigation`, `get_dataset_info`, `compare`. Loop capped at 5 calls |
| Image question (stretch) | Medium-high, model-dependent | Needs a vision-capable model on the chosen provider. Keep to one photo, grounded in evidence |
| RAG, vector DB, agent framework | Not needed | Evidence is already structured. Add only if a feature demands it |
| Custom model training | Not needed | Excluded |

### 5.3 Initial provider strategy

This is the starting plan, adjustable after Week 1 testing.

```text
Development:   Ollama  ->  Gemini  ->  OpenRouter
Demo / hosted: Gemini  ->  OpenRouter  ->  Ollama
Always last:   deterministic explanation
```

Development starts with Ollama so repeated prompt and tool-loop testing does not burn hosted quota. Gemini is the hosted validation target.

- Each provider implements one small interface: `generate(messages, schema?, tools?)`.
- The first provider with quota answers. A failed call moves to the next.
- Identical requests are cached by evidence hash, prompt version, provider and model, which makes demos repeatable, saves quota and lets different models keep distinct outputs.
- Each team member uses their own free API key during development. The demo uses cached AI results plus one live provider.

### 5.4 Tool contract

The natural-language lookup may call only these server-defined tools:

| Tool | Purpose | Data modification |
|---|---|---|
| `search_place` | Resolve a place name to a supported location | No |
| `run_investigation` | Create/retrieve a HazardLens investigation for the resolved location | Yes, investigation record only |
| `get_dataset_info` | Retrieve source and dataset metadata | No |
| `compare` | Compare existing investigations | No |

Tool arguments shall be schema-validated. Unknown tool names, invalid arguments and calls beyond the five-call limit shall be rejected. Tools shall not expose arbitrary HTTP, SQL, shell, filesystem or tool-definition access.

### 5.5 Safety rules

1. The model only sees the structured evidence the backend gives it.
2. Missing evidence is stated as missing, never filled from model knowledge.
3. The model cannot change classes, statuses or dates.
4. Tool calls use an allow-list. No model access to SQL, shell, arbitrary HTTP or files.
5. Outputs are schema-validated. Invalid output retries once, then falls back.
6. All AI text carries a "generated" label.
7. User prompts, tool results and source text cannot override these rules; they are treated as untrusted data.

---

## 6. Build Plan

### 6.1 Using AI agents effectively

- Keep an `AGENTS.md` (or equivalent) in the repo with the stack, folder layout, status rules, naming and "never do" items from section 5.5.
- Write the contract first: database models, normalized result schema and the OpenAPI spec. Agents work faster and more safely against a typed contract.
- Save real service responses as fixtures in Week 1 so agents can write adapter tests offline.
- One feature per branch, one small pull request, tests required. Humans review every merge.
- Humans own decisions: statuses, source choices, AI safety rules, and anything that touches data meaning.

### 6.2 Team roles

| Member | Focus |
|---|---|
| A | Source adapters, fixtures, resilience |
| B | Database, migrations, investigation, comparison and report services |
| C | Frontend: map, search, evidence panel |
| D | Frontend: history, comparison, report, polish and design |
| E | AI providers, tools, chat and explanation, prompt tests |

Everyone reviews and everyone tests. Roles rotate for the final week.

### 6.3 Schedule

| Week | Goal | Done when |
|---|---|---|
| 1 | Setup and verification | Compose runs on every machine. Each dataset source queried live at one Iloilo point and one sea point. Fixtures saved. Gemini, OpenRouter and Ollama each answer a tool-calling test. Versions pinned |
| 2 | Core backend | Investigation endpoint returns four datasets with statuses, database persistence, caching |
| 3 | Core frontend | Map click, search, evidence panel, history |
| 4 | Core complete | Weather, comparison, report, deterministic explanation. Core demo-ready |
| 5 | AI explanation and chat | Provider interface, fallback chain, structured output, labelled AI panel |
| 6 | Natural-language lookup | Tool-calling loop with the allow-list and visible tool steps in the UI |
| 7 | Advanced and polish | Area query, overlays or image input (pick what fits), design pass, error states |
| 8 | Hardening and demo | Fixtures for demo, test pass, source-accuracy comparison, documentation, rehearsal |

### 6.4 Week 1 checklist

1. Query each source once at central Iloilo City (about 10.72 N, 122.56 E) and once at sea. Record status, class field, date field and latency.
2. Test fault proximity with identify at several tolerances.
3. Confirm whether the MGB detailed flood layer gives different results from the GeoRiskPH flood layer.
4. Open-Meteo, Nominatim and basemap tile checks.
5. Docker Compose with PostGIS on every machine. The image is amd64, so ARM laptops run it under emulation.
6. Get free keys for Gemini and OpenRouter. Confirm the exact Gemini model and current quota in AI Studio. Install Ollama and test one tool-capable model for tool calling and structured output.
7. Email GeoRiskPH, PHIVOLCS and MGB about permission to query and cache. Log replies. Do not wait for them.

If a source fails the check, use its backup candidate or swap in another dataset (section 4.4).

### 6.5 Testing

- **Adapter tests** replay saved fixtures for found, no evidence, error and outside coverage.
- **Status tests** prove errors never become `NO_EVIDENCE`.
- **API tests** run against mocked upstreams.
- **AI tests** check schema validity, refusal to invent facts, and tool-loop limits using a small set of fixed prompts.
- **Accuracy check:** compare 15 to 20 points against the agencies' own viewers and note disagreements.

### 6.5.1 Requirements traceability sample

The project maintains a lightweight traceability table linking critical requirements to implementation areas and tests. It is not intended to replace the full test suite.

| Requirement | Implementation area | Example verification |
|---|---|---|
| FR-03 | Investigation service | Partial-upstream-failure API test |
| FR-06 | Spatial evaluator | Point/area operation tests |
| FR-15 | AI service | Structured-output validation test |
| FR-17 | AI tool loop | Maximum-five-calls test |
| NFR-12 | Session authorization | Cross-session access test |
| NFR-13 | API middleware | Rate-limit test |
| NFR-18 | Logging | Structured-log inspection |

### 6.6 Advanced-feature acceptance criteria

- An area investigation stores its polygon and visibly marks datasets that do not support the required operation.
- An investigation from one session cannot be retrieved from another session.
- At least one AI provider returns schema-valid evidence explanations and grounded chat responses.
- Fixed AI tests demonstrate that the model does not invent a class, source, date or hazard finding absent from the supplied evidence.
- The natural-language lookup stops after at most five tool calls and rejects unknown tools.
- A weather outage produces an unavailable weather state while hazard evidence remains usable.
- Comparison displays source findings side by side without producing a ranking or safety score.

### 6.7 Definition of done

- Four hazard datasets return real results with correct statuses and provenance.
- Database persists investigations, history, comparisons and AI generations.
- Area investigations store polygon geometry and evaluate dataset operations, returning `UNSUPPORTED` where an operation is not supported.
- AI explanation, chat and natural-language lookup work on at least one free provider, with fallback tested.
- The app survives an upstream outage using fallback or labelled recorded data.
- A polished UI with clear loading, empty and error states.
- Report page prints cleanly.
- One-command setup works on a clean machine.

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| Government services slow or down | Timeouts, one retry, cached results, recorded demo fixtures |
| A source cannot be queried as expected | Backup candidate or swap datasets. Decided in Week 1 |
| No stated licence to cache or copy data | Short cache, no bulk copies, permission emails, attribution everywhere |
| Free AI quotas change | Provider chain, local Ollama, AI result cache, deterministic fallback |
| Local model tool-calling reliability varies | Test at least one tool-capable model in Week 1, keep the tool set small, prefer the hosted free tier for the demo |
| AI hallucination | Evidence-only context, schema validation, labels, refusal rules, prompt tests |
| Scope creep | Core first. Advanced in order. Stretch only if Weeks 1 to 6 finish on time |
| Weak Python skills in team | Week 1 exercise. Agents help, but humans must understand and review |

---

## Appendix A. Class Vocabularies

Classes stay source-scoped and are never merged.

| Source | Field | Examples |
|---|---|---|
| MGB detailed flood | `FloodSusc` | LF Low, MF Moderate, HF High, VHF Very High |
| MGB rain-induced landslide | Service-defined | Low, Moderate, High, Very High, plus debris-flow categories where applicable |
| PHIVOLCS liquefaction | `lccode` | Seven source-defined potential and susceptibility classes |
| PHIVOLCS active fault | `fccode` | Active, Potentially Active |

## Appendix B. Revision History

| Version | Date | Summary |
|---|---|---|
| 3.1 | 9 Oct 2026 | Upgraded normalized evidence result to include `matches[]` array with configurable cap and deterministic sorting for AI hashing; added child table `evidence_match` to preserve relational FK integrity with `hazard_class`; specified `ON DELETE CASCADE` on session relationships; documented cache reuse of evidence/weather tables; unified path parameters to snake_case (`{investigation_id}`, `{comparison_id}`). |
| 3.0 | 1 Oct 2026 | Build baseline updated in place. Preserved the condensed v3.0 structure while tightening spatial operations, area-investigation storage, session isolation, rate limiting, AI provider/tool contracts, prompt-injection handling, accessibility, browser support, logging, API contracts and advanced-feature acceptance criteria. |
| 2.6 | 1 Oct 2026 | Reframed as a web-systems project, added PostGIS, AI sections |
| 2.5 | 1 Oct 2026 | Standard SRS layout |
| 2.2 to 2.4 | Earlier | Earlier drafts |
