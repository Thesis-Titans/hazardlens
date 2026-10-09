# HazardLens Requirements Traceability

**Baseline:** SRS v3.1 proposed in PR #9; confirm version before treating this matrix as canonical.  
**Status:** Initial traceability baseline, not a completion report.  
**Rule:** “Partial” means a limited implementation exists but does not meet the whole requirement. “Not verified” means there is no sufficient reproducible evidence in the reviewed repository/CI. An issue link does not prove implementation.

## Functional requirements

| Requirement | Short intent | Issue / work item | Current evidence status | Verification needed |
|---|---|---|---|---|
| FR-01 | Select location by search or map; validate and round coordinates | #3, #5, #7, #11 | **PARTIAL** — PR #11 validates/rounds coordinates for the flood preview only; place search and map selection are not delivered. | API validation tests plus map/search-to-investigation acceptance test. |
| FR-02 | Persist each investigation and show session history | #1, #3 | **NOT VERIFIED** | PostGIS migration, persistence integration test, session history and expiry test. |
| FR-03 | Query active datasets concurrently under a deadline; isolate failures | #3, #6 | **NOT VERIFIED** — single-source preview is not multi-source orchestration. | Concurrent service test proving one upstream failure does not suppress other results and total deadline is bounded. |
| FR-04 | Every evidence result uses exactly one of five statuses | #3, #8, #11 | **PARTIAL** — preview schema defines statuses, but the full investigation pipeline is absent. | Contract tests for all statuses and all active datasets. |
| FR-05 | Return NO_EVIDENCE only after successful query inside known coverage | #2, #3, #6, #11 | **PARTIAL** — preview avoids claiming empty means no evidence while coverage is unverified. | Verified coverage semantics and tests for valid empty, outside coverage, timeout and malformed response. |
| FR-06 | Use geometry-appropriate spatial operations for point/area/fault data | #2, #6 | **NOT VERIFIED** | Per-source contract record and spatial-operation tests; area queries only where supported. |
| FR-07 | Show agency, dataset/class definition, source date, retrieval time, origin and attribution | #2, #8, #11 | **PARTIAL** — preview carries some provenance; production evidence UI is not implemented. | API schema plus UI acceptance test for all required provenance fields. |
| FR-08 | Preserve source class labels; never create universal hazard score | #8, #11 | **PARTIAL** — flood preview preserves published class labels; end-to-end UI behavior not verified. | Fixture contract tests and UI test that displays source wording without synthetic score. |
| FR-09 | Preserve multiple material matches and show source disagreements | #6, #11 | **PARTIAL** — preview preserves multiple matching features; multi-source comparison not implemented. | Fixtures with multiple features/classes and two sources with differing results. |
| FR-10 | Deterministic explanation based on stored class definitions | #4 | **NOT VERIFIED** | Unit tests proving explanation uses known definitions and explicitly states missing information. |
| FR-11 | Compare two or more past investigations without ranking | Issue #14; schema support in #1 | **NOT VERIFIED** | Tracked in #14; test same-session authorization and non-ranking comparison UI. |
| FR-12 | Printable report with provenance, limitations and optional AI summary | Issue #14 | **NOT VERIFIED** | Tracked in #14; verify print output, disclaimer, source attribution and no fabricated findings. |
| FR-13 | Current weather card separate from hazard evidence | Issue #15 | **NOT VERIFIED** | Tracked in #15; weather failure must not alter hazard result. |
| FR-14 | Evidence panel works without map tiles or geocoder | #3, #8 | **NOT VERIFIED** | Frontend/API integration test with map/geocoder disabled. |
| FR-15 | AI explanation consumes structured evidence and validates output schema | #4 | **DEFERRED** | Start only after core evidence slice is verified; malformed output tests and deterministic fallback. |
| FR-16 | AI chat grounded in current investigation; refuses unsupported facts | #4 | **DEFERRED** | Grounding tests including missing evidence and out-of-context questions. |
| FR-17 | Natural-language lookup uses bounded allow-listed tool calls | #4 | **DEFERRED** | Tool allow-list tests, maximum-five-call test and no arbitrary HTTP/SQL/shell capability. |
| FR-18 | Label AI output and store provider/model/prompt version/evidence hash/time | #4, #1 | **DEFERRED** | Provenance persistence and generated-content UI tests. |
| FR-19 | AI provider failure falls back; core evidence remains usable | #4 | **DEFERRED** | Simulate quota, timeout, transport and invalid-output failure. |
| FR-20 | Validate simple area polygons and configurable limits | Issue #16; schema support proposed in #1 | **NOT VERIFIED** | Tracked in #16; geometry validity, self-intersection, vertex and area-limit tests. |
| FR-21 | Weather failure returns UNAVAILABLE without changing hazard investigation | Issue #15 | **NOT VERIFIED** | Weather adapter failure integration test. |

## Non-functional requirements

| Requirement | Short intent | Issue / work item | Current evidence status | Verification needed |
|---|---|---|---|---|
| NFR-01 | Cached lookup under 1s; live lookup bounded by deadline | #3, #6 | **NOT VERIFIED** | Repeatable latency test with cache hit and bounded upstream timeout. |
| NFR-02 | Upstream timeout and one retry on timeout/5xx; no retry on 4xx | #2, #6, #11 | **PARTIAL** — preview implements retry behavior; all adapters are not implemented. | Adapter contract tests for timeout, 5xx retry and 4xx no-retry across each source. |
| NFR-03 | Upstream URLs from configuration/registry; no browser-supplied URLs/SQL/tools | #6 | **NOT VERIFIED** | API security tests and code review for SSRF/arbitrary query inputs. |
| NFR-04 | Restrictive CORS; AI keys server-side | Existing scaffold + #4 | **PARTIAL / NOT VERIFIED** — local-origin CORS exists; deployment origins and key handling are not end-to-end verified. | Environment-specific CORS test and secret-handling review. |
| NFR-05 | Random HttpOnly session cookie, no raw IP, 30-day expiry | #1 | **NOT VERIFIED** | Cookie flags, entropy, expiry cleanup, and absence of raw IP storage tests. |
| NFR-06 | Nominatim policy compliance, rate limit/cache, no autocomplete | #7 | **BLOCKED** — issue acceptance criteria conflict with public Nominatim policy. | Record provider/UX decision and verify request rate, identifying User-Agent, attribution, caching and no autocomplete if public Nominatim is selected. |
| NFR-07 | Recorded demo fixtures for several Iloilo points, labelled as recorded | #2 | **NOT VERIFIED** | Review fixtures, provenance and visible recorded-data label. |
| NFR-08 | Attribution and planning-data disclaimer on every page | #8, #10 | **PARTIAL** — scaffold disclaimer is proposed in PR #10; all pages not verified. | Page-by-page UI review and automated checks where practical. |
| NFR-09 | New dataset added via adapter and registry rows without schema change | #6 | **NOT VERIFIED** | Add a test/mock dataset through registry and adapter contract without migration. |
| NFR-10 | Dependencies pinned; API contract generated/shared with frontend | #1, #3 | **NOT VERIFIED** | Verify lockfile strategy and generated API type workflow against a clean install. |
| NFR-11 | Do not scrape, embed or frame HazardHunterPH | Issue #12 / code review gate | **NOT VERIFIED** | Code/config review confirms no scraping, embedding or framing. |
| NFR-12 | Session can access only its own investigations/comparisons | #1 | **NOT VERIFIED** | Cross-session authorization tests for every read/write path. |
| NFR-13 | Configurable rate limits on expensive public endpoints; HTTP 429 on limit | Issue #17 | **NOT VERIFIED** | Tracked in #17; concurrency/rate-limit tests and documented defaults. |
| NFR-14 | AI calls have timeouts and fallback on provider/format failure | #4 | **DEFERRED** | Provider tests after evidence slice; bounded timeout/fallback tests. |
| NFR-15 | External/user text cannot override AI rules or tools | #4 | **DEFERRED** | Prompt-injection tests using untrusted source attributes and user text. |
| NFR-16 | Keyboard access, focus, labels, status messaging; target WCAG 2.2 AA where practical | #18 | **NOT VERIFIED** | Keyboard-only review, automated accessibility scan and manual contrast/focus review. |
| NFR-17 | Support latest two major Chrome/Edge/Firefox and common mobile viewports | #18 | **NOT VERIFIED** | Browser/device matrix and responsive acceptance checks. |
| NFR-18 | Structured diagnostic logs without raw IPs | Issue #17 | **NOT VERIFIED** | Log-schema tests and review that identifiers/diagnostics omit raw IPs and secrets. |

## Traceability maintenance

1. Every requirement must map to a GitHub issue or a deliberately deferred item.
2. Each issue must have observable acceptance criteria and a separate reviewer.
3. Update the matrix when requirements, issue ownership or implementation status changes.
4. Mark a requirement complete only after acceptance evidence is linked (tests, CI run, source verification record or reproducible manual check).
5. Do not equate a green CI run with all requirements passing; CI currently runs lint/format/tests and frontend type/build checks, not live source verification or PostGIS migration tests.
