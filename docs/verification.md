# HazardLens — Technical Verification Record

**Project:** HazardLens  
**Baseline:** SRS v3.1  
**Purpose:** Record technical verification of external services, application behavior, database setup, AI providers and release readiness.

## 1. Verification Principles

Verification answers:

> **Does the implemented system behave as specified?**

The verification record is a living engineering document. The SRS defines the requirements; this file records the evidence that those requirements work in the actual project.

## 2. Verification Status

Use these statuses:

- `NOT_STARTED`
- `PASS`
- `FAIL`
- `BLOCKED`
- `DEFERRED`
- `N/A`

For every failed or blocked item, record the reason and next action.

## 3. Week 1 Technical Verification

### 3.1 Hazard source connectivity

| Check | Target | Status | Evidence / notes |
|---|---|---|---|
| Flood query | MGB detailed flood | NOT_STARTED | |
| Flood backup | GeoRiskPH flood WMS | NOT_STARTED | |
| Rain-induced landslide query | MGB detailed landslide | NOT_STARTED | |
| Landslide backup | GeoRiskPH landslide WMS | NOT_STARTED | |
| Liquefaction query | PHIVOLCS GeoRiskPH | NOT_STARTED | |
| Liquefaction fallback | Identify on same service | NOT_STARTED | |
| Active fault identify | PHIVOLCS ActiveFault | NOT_STARTED | |
| Active fault backup | GeoRiskPH ActiveFault WMS | NOT_STARTED | |

For each source record:

```text
Service URL:
Dataset/layer:
HTTP status:
Query method:
Response format:
Relevant class field:
Relevant date field(s):
Returned evidence:
Empty-result behavior:
Error behavior:
Latency:
Notes:
```

### 3.2 Test locations

At minimum use:

- one inland Iloilo point;
- one sea point or another point expected to exercise an empty/outside-coverage condition.

Record the exact coordinates used.

### 3.3 Fault proximity

Explore the active-fault source at several test distances to characterize the source operation. These distances are exploratory test cases, not approved user-facing thresholds or evidence of a scientifically validated risk buffer. Document the source method, units, geometry/CRS handling and rationale before selecting any user-visible distance bands.

| Test | Tolerance / band | Result | Status |
|---|---:|---|---|
| Fault test 1 | 1 km | | NOT_STARTED |
| Fault test 2 | 5 km | | NOT_STARTED |
| Fault test 3 | 10 km | | NOT_STARTED |
| Fault test 4 | 20 km | | NOT_STARTED |

The team must determine whether the source behavior is sufficient to produce a useful proximity result.

### 3.4 Source comparison

Confirm whether the MGB detailed flood layer is materially different from the GeoRiskPH flood layer.

| Point | MGB result | GeoRiskPH result | Independent? | Notes |
|---|---|---|---|---|
| Point 1 | | | | |
| Point 2 | | | | |

The purpose is to decide whether both should remain in the source strategy or whether the backup is effectively the same dataset.

## 4. Supporting Service Verification

| Service | Test | Expected | Status |
|---|---|---|---|
| Open-Meteo | Current weather request | Required current fields returned | NOT_STARTED |
| Nominatim | Place search with identifying User-Agent | Search works under policy limits | NOT_STARTED |
| Nominatim rate limit | Outbound request rate | At most 1 request per second | NOT_STARTED |
| Nominatim caching | Geocode cache | Results cached per configured TTL | NOT_STARTED |
| Nominatim autocomplete | No autocomplete or keystroke queries | Autocomplete is not used | NOT_STARTED |
| OpenFreeMap | Map style load | Map renders | NOT_STARTED |
| OpenFreeMap fallback | Blank/fallback style | Application still loads without tiles | NOT_STARTED |

## 5. Database Verification

### 5.1 Environment

| Check | Expected | Status |
|---|---|---|
| PostgreSQL starts | Container healthy | NOT_STARTED |
| PostGIS extension | Available | NOT_STARTED |
| FastAPI database connection | Successful | NOT_STARTED |
| Alembic migration from clean DB | Successful | NOT_STARTED |
| Migration rollback/round trip | Successful | NOT_STARTED |
| Spatial column works | Point/polygon geometry can be stored | NOT_STARTED |
| Foreign keys | Enforced | NOT_STARTED |
| Required indexes | Created | NOT_STARTED |

### 5.2 Data integrity

Verify that:

- every investigation belongs to a valid session;
- every evidence result belongs to a valid investigation;
- child `evidence_match` records reference valid `evidence_result` and `hazard_class` rows;
- session deletion triggers `ON DELETE CASCADE` down to child investigations and evidence records;
- dataset/source relationships are valid;
- hazard classes remain source-scoped;
- an investigation stores the original selection geometry;
- AI generations reference the investigation and evidence hash correctly;
- expired session data follows the configured 30-day retention policy.

## 6. Backend Verification

### 6.1 Investigation flow

| Test | Expected result | Status |
|---|---|---|
| Valid point investigation | Investigation stored and returned | NOT_STARTED |
| Invalid coordinate | Controlled validation error | NOT_STARTED |
| Outside study area | Controlled validation error | NOT_STARTED |
| Four datasets run concurrently | Results returned under shared deadline | NOT_STARTED |
| One upstream timeout | Other evidence still returned | NOT_STARTED |
| One upstream HTTP 5xx | Other evidence still returned | NOT_STARTED |
| Successful empty result | `NO_EVIDENCE` with empty `matches: []` | NOT_STARTED |
| Upstream failure | `UNAVAILABLE` with empty `matches: []` | NOT_STARTED |
| Documented source-specific outside-coverage case | `OUTSIDE_COVERAGE` only when an independently justified coverage rule establishes it; otherwise keep the result blocked/unavailable pending semantics | NOT_STARTED |
| Unsupported operation | `UNSUPPORTED` with empty `matches: []` | NOT_STARTED |
| Deterministic explanation | Plain-language summary built from class definitions | NOT_STARTED |
| Deterministic explanation without AI | Explanation renders when AI is unavailable | NOT_STARTED |

### 6.2 Evidence semantics

Verify that:

- `FOUND` status always carries a non-empty `matches` array (capped at 20);
- non-found statuses (`NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, `UNSUPPORTED`) always carry an empty `matches: []` array;
- matches are deterministically sorted (by `class_code`, then `distance_band_m` ascending) for stable evidence hashing;
- source classifications are displayed exactly as published;
- multiple material matches are preserved;
- source disagreement is not hidden by automatic selection;
- source dates remain text plus their documented basis;
- retrieval time is separate from source date;
- live, cached and recorded origins are distinguishable;
- missing evidence is never displayed as “safe.”

## 7. Frontend Verification

| Test | Expected result | Status |
|---|---|---|
| Search a place | Location can be selected | NOT_STARTED |
| Map click | Point can be selected | NOT_STARTED |
| Investigation loading | Clear loading state | NOT_STARTED |
| Evidence found | Evidence card rendered | NOT_STARTED |
| No evidence | Clear `NO_EVIDENCE` state | NOT_STARTED |
| Source unavailable | Clear unavailable state | NOT_STARTED |
| Unsupported area query | UI explains unsupported dataset | NOT_STARTED |
| Map failure | Evidence panel remains usable | NOT_STARTED |
| Geocoder failure | Existing/manual map interaction still works | NOT_STARTED |
| Mobile-width layout | Core investigation remains usable | NOT_STARTED |
| AI content | Clearly labelled generated content | NOT_STARTED |
| Report | Print layout is readable | NOT_STARTED |
| Attribution statement | Every page shows source attribution and limitation statement | NOT_STARTED |
| Keyboard navigation | All interactive elements reachable via keyboard | NOT_STARTED |
| Focus visibility | Focused elements have a visible focus indicator | NOT_STARTED |
| Accessible labels | Interactive elements have accessible names | NOT_STARTED |
| Status messaging | Status changes announced to assistive technology | NOT_STARTED |
| Chrome (latest 2 versions) | Core features work correctly | NOT_STARTED |
| Edge (latest 2 versions) | Core features work correctly | NOT_STARTED |
| Firefox (latest 2 versions) | Core features work correctly | NOT_STARTED |
| Common mobile viewports | Responsive layout is usable | NOT_STARTED |

## 8. Area Investigation Verification

Area queries are an Advanced feature.

### 8.1 Geometry checks

| Test | Expected | Status |
|---|---|---|
| Valid simple polygon | Accepted | NOT_STARTED |
| Self-intersecting polygon | Rejected | NOT_STARTED |
| Empty polygon | Rejected | NOT_STARTED |
| Excessive vertex count | Rejected or constrained | NOT_STARTED |
| Polygon outside supported study area | Rejected/controlled | NOT_STARTED |

### 8.2 Dataset behavior

For every core dataset determine:

```text
Point query supported?       Yes / No
Polygon query supported?    Yes / No
Configured spatial operation:
Returned result shape:
Status behavior:
```

A source that does not support area queries must return `UNSUPPORTED`; the application must not silently substitute a point query.

## 9. Comparison Verification

Verify that two or more previous investigations can be compared and that:

- source-defined findings are displayed side by side;
- provenance and source dates remain visible;
- evidence status is preserved;
- different spatial selection types are handled explicitly;
- the system does not generate a universal ranking or safety result.

## 10. Weather Verification

Verify that:

- current weather is stored with the investigation;
- weather is visually separated from hazard evidence;
- weather retrieval failure does not fail the hazard investigation;
- the weather source is identified;
- cached weather follows the configured TTL.

## 11. AI Verification

### 11.1 Provider tests

| Provider | Structured output | Tool calling | Image capability | Status |
|---|---|---|---|---|
| Gemini | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED |
| OpenRouter free model | NOT_STARTED | NOT_STARTED | MODEL-DEPENDENT | NOT_STARTED |
| Ollama model | NOT_STARTED | NOT_STARTED | MODEL-DEPENDENT | NOT_STARTED |

Record the exact model name tested.

### 11.2 AI behavior tests

| Test | Expected result | Status |
|---|---|---|
| Evidence explanation | Valid schema output | NOT_STARTED |
| Missing evidence | AI states it is missing | NOT_STARTED |
| Unknown hazard fact | AI does not invent it | NOT_STARTED |
| Source class question | Answer uses supplied evidence | NOT_STARTED |
| Source disagreement | Both source findings remain distinct | NOT_STARTED |
| Invalid structured output | Validation/fallback occurs | NOT_STARTED |
| Provider timeout | Next provider or deterministic fallback | NOT_STARTED |
| Provider quota/rate limit | Next provider or deterministic fallback | NOT_STARTED |
| Tool call | Only allow-listed tool executes | NOT_STARTED |
| Unknown tool | Rejected | NOT_STARTED |
| Tool argument validation | Invalid input rejected | NOT_STARTED |
| Five-call limit | Loop stops at five calls | NOT_STARTED |
| Direct SQL request by model | Impossible | NOT_STARTED |
| Arbitrary HTTP request by model | Impossible | NOT_STARTED |
| Prompt-injection attempt | System rules remain enforced | NOT_STARTED |
| AI-generated content label | Visible in UI | NOT_STARTED |

### 11.3 AI cache verification

Verify that identical:

```text
evidence hash
+ prompt version
+ provider
+ model
```

reuses the existing AI result, while changing any of those values can create a distinct generation.

## 12. Performance Verification

Record actual measurements rather than assuming the SRS targets are satisfied.

| Metric | Target | Actual | Status |
|---|---|---|---|
| Cached investigation response | < 1 second | | NOT_STARTED |
| Live investigation | Within configured deadline | | NOT_STARTED |
| Individual upstream timeout | Configured | | NOT_STARTED |
| AI response | Provider-dependent; controlled timeout | | NOT_STARTED |

For Week 1 source tests, record at least several calls per access path and note approximate p50/p95 latency where useful.

## 13. Security and Privacy Verification

| Check | Expected | Status |
|---|---|---|
| Upstream URL injection | Not possible | NOT_STARTED |
| SQL injection through normal API inputs | Prevented by validation/parameterization | NOT_STARTED |
| Cross-session investigation access | Denied | NOT_STARTED |
| AI keys in frontend bundle | None | NOT_STARTED |
| CORS | Only application origin | NOT_STARTED |
| Raw IP persistence | None | NOT_STARTED |
| Tool allow-list bypass | Not possible | NOT_STARTED |
| User text overriding AI rules | Prevented | NOT_STARTED |
| Rate limit | 429 when exceeded | NOT_STARTED |
| Structured logging | Logs contain request ID, dataset, source, status, latency, error type | NOT_STARTED |
| No raw IP in logs | Server logs do not store raw IP addresses | NOT_STARTED |

## 14. Source Accuracy Check

Use 15–20 representative points.

For each point compare HazardLens against the agency's own viewer or published service result.

| Point | Dataset | HazardLens | Agency reference | Match | Notes |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| … | | | | | |

The purpose is to detect integration/parsing mistakes, not to reinterpret the agency's classification.

## 15. Recorded Demo Fixtures

Save successful and representative failure responses as offline fixtures so the final demonstration does not depend entirely on live upstream availability.

Each fixture should record:

```text
source
endpoint/access path
test coordinates
request parameters (excluding secrets)
response
recorded_at
expected normalized result
```

Recorded data must be clearly labelled in the application when used.

## 16. Release Verification Gates

The release gate follows the team-approved requirement classifications in `docs/release-scope-and-task-matrix.md`. Until the team approves that matrix, FR-11–FR-13 remain unresolved because SRS v3.1 currently labels them Core. Do not use the conditional checklist below to silently remove a current Core requirement from scope.

### 16.1 Candidate MVP gate

- [ ] All four required hazard source families have verified adapters and reproducible source records/fixtures.
- [ ] Every evidence status has contract tests; empty, outside-coverage, unavailable and unsupported cases follow verified source-specific semantics.
- [ ] Source classifications, multiple matches, disagreements, provenance and limitations are preserved.
- [ ] The deterministic explanation works without an AI provider.
- [ ] Database migrations work from a clean environment if persistence is in the approved MVP.
- [ ] Session ownership, expiry and deletion are tested if FR-02 remains MVP-required.
- [ ] Evidence UI works when map tiles or geocoding are unavailable.
- [ ] Rate limits, URL restrictions, CORS, secret handling and privacy-safe diagnostics are verified.
- [ ] Accessibility and supported-browser checks are recorded.
- [ ] Clean-checkout setup, pinned dependencies, build/tests and release limitations are documented.
- [ ] Every approved MVP requirement is traceable to reproducible evidence or an explicitly accepted blocker.

### 16.2 Conditional gates — only if the team keeps these features in the release

- [ ] Comparison works without ranking locations (FR-11).
- [ ] Print report includes provenance and limitations (FR-12).
- [ ] Weather failure does not alter hazard results (FR-13 and FR-21).
- [ ] AI explanation, grounded chat, bounded tool calling, provenance and fallback pass the applicable tests (FR-15–FR-19 and NFR-14–NFR-15).
- [ ] Polygon validation and source capability gates pass (FR-20).

### 16.3 Not a release criterion by itself

A green CI run, a successful metadata-page load, or replaying a recorded fixture does not prove current source availability, valid coverage semantics, or a complete end-to-end user workflow. Record exactly what was tested and what remains unverified.

## 17. Week 1 Decision Record

At the end of Week 1, record the final implementation choices:

```text
Final flood source:
Final landslide source:
Final liquefaction source:
Final active fault source:

Fallback dataset used:

Geocoder:
Basemap:

Gemini model:
OpenRouter model:
Ollama model:

PostgreSQL/PostGIS version:
Node version:
Python version:

Known blockers:
Deferred features:
```
