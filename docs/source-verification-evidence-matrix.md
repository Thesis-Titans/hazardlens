# HazardLens — Source Verification Evidence Matrix

**Project:** HazardLens  
**Baseline:** SRS v3.1  
**Related Issue:** [Issue #2 — Verify official hazard sources and capture fixtures](https://github.com/Thesis-Titans/hazardlens/issues/2)  
**Related Documents:** [Official Source Verification Notes](source-verification-notes.md), [Verification Record](verification.md), [Decision Log](decision-log.md)  
**Status:** Working evidence matrix — pending whole-team review and independent verification sign-off  

> **Evidence Grounding Rule:** This document records only verified, reproducible technical evidence from official Philippine government geospatial services. An unverified endpoint, an HTTP error, or a metadata-only inspection must never be marked as a verified live source. Missing evidence must never be interpreted or displayed as proof of safety.

---

## 1. Purpose and Scope

This matrix tracks the verification lifecycle of the four mandatory Philippine government hazard data sources required for the HazardLens Minimum Viable Product (MVP).

Per `AGENTS.md` and SRS v3.1, before an official source can be integrated into the multi-source orchestration pipeline:

1. Its service identity, spatial operation, and coordinate reference system (CRS) must be confirmed.
2. Live queries must be observed and proven repeatable from an authorized environment.
3. Empty-result and boundary semantics must be established.
4. Offline fixtures with clear provenance must be captured for deterministic regression testing.

Secondary or backup access paths (such as GeoRiskPH WMS/identify endpoints) are exploratory alternatives and do **not** substitute for the verification of the primary source families without explicit team-approved scope changes.

---

## 2. Four-Stage Verification Lifecycle

To prevent conflating metadata inspection with live query reliability, every source is evaluated against four distinct, non-interchangeable milestones:

```text
[ Stage 1: Metadata Verified ]
               │
               ▼
[ Stage 2: Live Request Observed ]
               │
               ▼
[ Stage 3: Repeatable Query Verified ]
               │
               ▼
[ Stage 4: Coverage & Empty Semantics Verified ]
```

| Verification Stage | Meaning & Entry Criteria | Completion Evidence Required |
|---|---|---|
| **Stage 1: Metadata Verified** | Layer capabilities, geometry type, coordinate system, and attribute schemas confirmed against official service metadata. | Service URL, layer ID, spatial reference WKID, published classification fields, and official attribution terms. |
| **Stage 2: Live Request Observed** | At least one successful live HTTP request executed against the query endpoint. | Timestamp, request URL/parameters, response code, latency, and sanitized payload. |
| **Stage 3: Repeatable Query Verified** | Multiple independent live requests executed across different sessions/environments, confirming consistent response behavior and latencies without relying on cached or replayed fixtures. | Documented log of multiple live request runs with timestamps, coordinates, latencies, and confirmation that responses match expected schema and behavior. |
| **Stage 4: Coverage & Semantics Verified** | Clear technical distinction between "inside coverage, no hazard mapped" (`NO_EVIDENCE`) and "unmapped/outside survey boundary" (`UNAVAILABLE` / `OUTSIDE_COVERAGE`). | Documented boundary extent or polygon coverage layer; verified rule that distinguishes empty query from lack of survey. |

---

## 3. Official Hazard Source Verification Matrix

| Required Source Family | Official Agency & Service | Stage 1: Metadata | Stage 2: Live Request | Stage 3: Repeatable Query | Stage 4: Coverage & Empty Semantics | Current Disposition |
|---|---|:---:|:---:|:---:|:---:|:---|
| **Flood Susceptibility** | **MGB**<br>`GDI_Detailed_Flood_Susceptibility/FeatureServer/0` | **VERIFIED**<br>Polygon (EPSG:3857), fields `OBJECTID`, `FloodSusc` (`VHF`, `HF`, `MF`, `LF`). | **PENDING**<br>Historical captured responses exist (Iloilo `MF`, Panay Gulf empty), but the complete live-request record required by Stage 2—timestamp, exact request/parameters, HTTP status, latency, and sanitized response—is not attached here. Do not interpret the fixtures as a fresh or independently confirmed request. | **PENDING**<br>Initial live responses were historically captured; multi-run repeatability across independent sessions/environments remains unverified. | **PENDING**<br>ArcGIS query does not publish a verified survey boundary. Empty responses remain `UNAVAILABLE`. | **Partial — historical response captures only**<br>Metadata and recorded payloads exist; Stage 2 evidence record, multi-run repeatability, and coverage semantics remain pending. |
| **Rain-Induced Landslide Susceptibility** | **MGB**<br>`GDI_Detailed_Rain_induced_Landslide_Susceptibility/FeatureServer/0` | **VERIFIED**<br>Polygon (EPSG:3857), fields `OBJECTID`, `LndslideSusc` (`VHL`, `HL`, `ML`, `LL`, `DF`). | **PENDING**<br>Fresh live-query behavior not independently confirmed in review session. | **PENDING**<br>Repeatable positive and negative coordinates not captured. | **PENDING**<br>Boundary, de-vegetated zone, and debris-flow (`DF`) semantics unestablished. | **Metadata Only**<br>Live-source verification required. |
| **Liquefaction Susceptibility** | **PHIVOLCS**<br>`Liquefaction_ohas/FeatureServer/0` | **PENDING**<br>Earlier metadata URL retrieval returned application error. Direct client inspection pending. | **PENDING**<br>Not verified. | **PENDING**<br>Not verified. | **PENDING**<br>Layer identity, class codes, and empty response semantics unverified. | **Blocked**<br>Endpoint accessibility & layer verification required. |
| **Active Fault Proximity** | **PHIVOLCS**<br>`ActiveFaultGeneric` candidate (`AF_2025_asofJanuary`) | **PENDING**<br>Earlier metadata retrieval returned application error. Current active layer identity pending. | **PENDING**<br>Not verified. | **PENDING**<br>Not verified. | **PENDING**<br>Distance-band calculation, buffer units, and line proximity rules unverified. | **Blocked**<br>Endpoint accessibility & layer verification required. |

---

## 4. Evidence Semantics & Invariant Rules

Every adapter and investigation result must adhere strictly to the evidence status transition rules defined in `AGENTS.md`:

1. **`FOUND`**:
   - Requires at least one intersecting feature match.
   - Preserves official source classifications verbatim (e.g., `VHF`, `HF`, `MF`, `LF`).
   - Never maps source ratings to an invented universal hazard scale or numeric risk score.
2. **`NO_EVIDENCE`**:
   - Valid **only** after a successful query inside confirmed source survey coverage.
   - An empty response (`features: []`) where survey coverage has not been independently proven **must remain `UNAVAILABLE`**.
3. **`OUTSIDE_COVERAGE`**:
   - Valid only when the query coordinate falls outside the officially published geographic extent or surveyed boundaries.
4. **`UNAVAILABLE`**:
   - Applied to any upstream HTTP error, network timeout, malformed payload, truncation limit reached (`exceededTransferLimit`), or query with unestablished survey coverage.
   - **Never convert `UNAVAILABLE` to `NO_EVIDENCE`.**
5. **`UNSUPPORTED`**:
   - Applied when a requested geometry type (e.g., polygon area query) is not supported by the specific dataset adapter.

---

## 5. Source Evidence Record Template

For each official source family, contributors must document a completed evidence record following this structure before marking Stage 2, Stage 3, or Stage 4 complete:

```markdown
### Evidence Record: [Source Name]

- **Date of Verification:** YYYY-MM-DD
- **Verifier:** [Name / Role]
- **Reviewer:** [Independent Reviewer Name]
- **Execution Mode:** [Fresh Independently Repeated Live Request | Historical Fixture Playback]
- **Independent Confirmation Status:** [Unconfirmed in current review session | Confirmed by independent reviewer: Name]
- **Environment & Network:** [e.g., Local shell script / CI runner / direct httpx query]

#### 1. Official Identity & Contract
- **Agency:** [e.g., Mines and Geosciences Bureau (MGB)]
- **Service Endpoint:** [URL]
- **Layer ID & Name:** [e.g., 0 — GDI_Detailed_Flood_Susceptibility]
- **Spatial Reference:** Input: EPSG:4326 | Native Layer: EPSG:[XXXX]
- **Geometry Type:** [Polygon / Polyline / Point]
- **Attributes Requested:** [e.g., OBJECTID, FloodSusc]
- **Official Attribution:** [Verbatim attribution text]
- **Terms of Use / Policy URL:** [URL]

#### 2. Live Request Evidence (Fresh Live Requests Only)
> *Note: Fixture playback or adapter unit tests do not satisfy this section.*
- **Repetition Details:** [Number of runs, timestamps, environments tested]
- **Test Coordinate 1 (Positive Feature Hit):**
  - Latitude, Longitude: [e.g., 10.7202, 122.5621]
  - HTTP Status: [200 OK]
  - Latency: [XXXX ms]
  - Returned Features: [Sanitized JSON attribute payload]
  - Derived Status: [FOUND]
- **Test Coordinate 2 (Empty / Offshore Hit):**
  - Latitude, Longitude: [e.g., 10.5000, 122.8000]
  - HTTP Status: [200 OK]
  - Latency: [XXXX ms]
  - Returned Features: `{"features": []}`
  - Derived Status: [UNAVAILABLE — pending verified boundary polygon]

#### 3. Error & Truncation Handling
- **Timeout Behavior:** [Observed latency, retry count, fallback to UNAVAILABLE]
- **Truncation Guard:** [Behavior when exceededTransferLimit is true or feature count reaches limit]
- **HTTP 5xx Recovery:** [Verified retry once on transient server errors]

#### 4. Offline Fixture Provenance
> *Note: Offline fixtures establish repeatable offline regression testing; they do NOT prove current live service availability.*
- **Capture Date & Commit:** [YYYY-MM-DD, Commit SHA when recorded]
- **Positive Fixture Path:** `api/tests/fixtures/[source]_[location]_[class].json`
- **Empty Fixture Path:** `api/tests/fixtures/[source]_[location]_empty.json`
- **Regression Test Coverage:** [Test function names in api/tests/]
```

---

## 6. Verification Roadmap & Next Steps

1. **Review the merged PR #11 preview implementation:**
   - Review the MGB flood preview implementation on `main` against the criteria in Sections 3 and 4. PR #11 is already merged; this review does not replace the pending live-source verification under Issue #2.
2. **Issue #2 Execution (Live Source Connectivity):**
   - Conduct network-level connectivity and metadata verification for the PHIVOLCS Liquefaction and Active Fault endpoints.
   - Record positive and empty test coordinates for MGB Landslide Susceptibility.
   - Capture sanitized offline fixtures in `api/tests/fixtures/` with provenance documentation.
3. **Issue #3 Implementation (Vertical Slice Integration):**
   - Connect the verified flood adapter and subsequent hazard adapters to the unified investigation orchestration pipeline.
