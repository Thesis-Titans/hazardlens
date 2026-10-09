# HazardLens Requirements Traceability

**Baseline:** SRS v3.1 proposed in PR #9; confirm version before treating this matrix as canonical.  
**Status:** Initial traceability baseline, not a completion report. Project lead approved the proposed classifications as working direction on 9 October 2026; formal team approval remains pending.  
**Rule:** “Partial” means a limited implementation exists but does not meet the whole requirement. “Not verified” means there is no sufficient reproducible evidence in the reviewed repository/CI. An issue link does not prove implementation.

> **Classification rule:** These classifications are approved as the project lead's working direction, not as formal whole-team approval. Any requirement currently marked Core in the SRS and proposed for post-MVP (FR-11–FR-13) must remain unresolved until the team explicitly approves a scope change. “Proposed post-MVP” is not a completed or removed requirement. NFR-09 remains unresolved pending a concrete, testable interpretation.

## Functional requirements

| Requirement | Proposed release classification | Short intent | Issue / work item | Current evidence status | Verification needed |
|---|---|---|---|---|
| FR-01 | MVP-required | Select location by search or map; validate and round coordinates | #3, #5, #7, #11 | **PARTIAL** — PR #11 validates/rounds coordinates for the flood preview only; place search and map selection are not delivered. | API validation tests plus map/search-to-investigation acceptance test. |
| FR-02 | MVP-required | Persist each investigation and show session history | #1, #3 | **NOT VERIFIED** | PostGIS migration, persistence integration test, session history and expiry test. |
| FR-03 | MVP-required | Query active datasets concurrently under a deadline; isolate failures | #3, #6 | **NOT VERIFIED** — single-source preview is not multi-source orchestration. | Concurrent service test proving one upstream failure does not suppress other results and total deadline is bounded. |
| FR-04 | MVP-required | Every evidence result uses exactly one of five statuses | #3, #8, #11 | **PARTIAL** — preview schema defines statuses, but the full investigation pipeline is absent. | Contract tests for all statuses and all active datasets. |
| FR-05 | MVP-required | Return NO_EVIDENCE only after successful query inside known coverage | #2, #3, #6, #11 | **PARTIAL** — PR #11 includes a captured empty MGB response, but maps it to `UNAVAILABLE` because valid-empty/coverage semantics are not established. | Independently repeat the query; verify source coverage and valid-empty semantics; test valid empty, outside coverage, timeout and malformed response. |
| FR-06 | MVP-required | Use geometry-appropriate spatial operations for point/area/fault data | #2, #6 | **NOT VERIFIED** | Per-source contract record and spatial-operation tests; area queries only where supported. |
| FR-07 | MVP-required | Show agency, dataset/class definition, source date, retrieval time, origin and attribution | #2, #8, #11 | **PARTIAL** — preview carries some provenance; production evidence UI is not implemented. | API schema plus UI acceptance test for all required provenance fields. |
| FR-08 | MVP-required | Preserve source class labels; never create universal hazard score | #8, #11 | **PARTIAL** — flood preview preserves published class labels; end-to-end UI behavior not verified. | Fixture contract tests and UI test that displays source wording without synthetic score. |
| FR-09 | MVP-required | Preserve multiple material matches and show source disagreements | #6, #11 | **PARTIAL** — preview preserves multiple matching features; multi-source comparison not implemented. | Fixtures with multiple features/classes and two sources with differing results. |
| FR-10 | MVP-required | Deterministic explanation based on stored class definitions | #4 | **NOT VERIFIED** | Unit tests proving explanation uses known definitions and explicitly states missing information. |
| FR-11 | Proposed post-MVP — team approval required; currently Core in SRS | Compare two or more past investigations without ranking | Issue #14; schema support in #1 | **NOT VERIFIED** | Tracked in #14; test same-session authorization and non-ranking comparison UI. |
| FR-12 | Proposed post-MVP — team approval required; currently Core in SRS | Printable report with provenance, limitations and optional AI summary | Issue #14 | **NOT VERIFIED** | Tracked in #14; verify print output, disclaimer, source attribution and no fabricated findings. |
| FR-13 | Proposed post-MVP — team approval required; currently Core in SRS | Current weather card separate from hazard evidence | Issue #15 | **NOT VERIFIED** | Tracked in #15; weather failure must not alter hazard result. |
| FR-14 | MVP-required | Evidence panel works without map tiles or geocoder | #3, #8 | **NOT VERIFIED** | Frontend/API integration test with map/geocoder disabled. |
| FR-15 | Proposed post-MVP | AI explanation consumes structured evidence and validates output schema | #4 | **DEFERRED** | Start only after core evidence slice is verified; malformed output tests and deterministic fallback. |
| FR-16 | Proposed post-MVP | AI chat grounded in current investigation; refuses unsupported facts | #4 | **DEFERRED** | Grounding tests including missing evidence and out-of-context questions. |
| FR-17 | Proposed post-MVP | Natural-language lookup uses bounded allow-listed tool calls | #4 | **DEFERRED** | Tool allow-list tests, maximum-five-call test and no arbitrary HTTP/SQL/shell capability. |
| FR-18 | Proposed post-MVP | Label AI output and store provider/model/prompt version/evidence hash/time | #4, #1 | **DEFERRED** | Provenance persistence and generated-content UI tests. |
| FR-19 | Proposed post-MVP | AI provider failure falls back; core evidence remains usable | #4 | **DEFERRED** | Simulate quota, timeout, transport and invalid-output failure. |
| FR-20 | Proposed post-MVP | Validate simple area polygons and configurable limits | Issue #16; schema support proposed in #1 | **NOT VERIFIED** | Tracked in #16; geometry validity, self-intersection, vertex and area-limit tests. |
| FR-21 | Proposed post-MVP | Weather failure returns UNAVAILABLE without changing hazard investigation | Issue #15 | **NOT VERIFIED** | Weather adapter failure integration test. |

## Non-functional requirements

| Requirement | Short intent | Issue / work item | Current evidence status | Verification needed |
|---|---|---|---|---|
| NFR-01 | MVP-required | Cached lookup under 1s; live lookup bounded by deadline | #3, #6 | **NOT VERIFIED** | Repeatable latency test with cache hit and bounded upstream timeout. |
| NFR-02 | MVP-required | Upstream timeout and one retry on timeout/5xx; no retry on 4xx | #2, #6, #11 | **PARTIAL** — preview implements retry behavior; all adapters are not implemented. | Adapter contract tests for timeout, 5xx retry and 4xx no-retry across each source. |
| NFR-03 | MVP-required | Upstream URLs from configuration/registry; no browser-supplied URLs/SQL/tools | #6 | **NOT VERIFIED** | API security tests and code review for SSRF/arbitrary query inputs. |
| NFR-04 | MVP-required | Restrictive CORS; AI keys server-side | Existing scaffold + #4 | **PARTIAL / NOT VERIFIED** — local-origin CORS exists; deployment origins and key handling are not end-to-end verified. | Environment-specific CORS test and secret-handling review. |
| NFR-05 | MVP-required | Random HttpOnly session cookie, no raw IP, 30-day expiry | #1 | **NOT VERIFIED** | Cookie flags, entropy, expiry cleanup, and absence of raw IP storage tests. |
| NFR-06 | MVP-required | Geocoding policy compliance, rate limit/cache, no autocomplete against public Nominatim | #7 | **INTERACTION SELECTED; PROVIDER PENDING** — use explicit user-submitted search plus coordinate/map fallback; team must confirm provider and UX. | Verify provider-specific terms; if public Nominatim is selected, verify max 1 request/second/app, identifying User-Agent/Referer, attribution, caching and no autocomplete. |
| NFR-07 | MVP-required | Recorded demo fixtures for several Iloilo points, labelled as recorded | #2, #11 | **PARTIAL** — PR #11 adds two captured MGB flood response fixtures (one Central Iloilo match and one offshore empty response) with provenance notes; this does not yet establish several Iloilo demo points or visible recorded-data labelling in the UI. | Review fixture provenance, add sufficient approved demo points if required, and verify the UI visibly distinguishes recorded fixtures from live results. |
| NFR-08 | MVP-required | Attribution and planning-data disclaimer on every page | #8, #10 | **PARTIAL** — scaffold disclaimer is proposed in PR #10; all pages not verified. | Page-by-page UI review and automated checks where practical. |
| NFR-09 | Unresolved — clarify before baseline | New dataset added via adapter and registry rows without schema change | #6 | **NOT VERIFIED** | Add a test/mock dataset through registry and adapter contract without migration. |
| NFR-10 | MVP-required | Dependencies pinned; API contract generated/shared with frontend | #1, #3 | **NOT VERIFIED** | Verify lockfile strategy and generated API type workflow against a clean install. |
| NFR-11 | MVP-required | Do not scrape, embed or frame HazardHunterPH | Issue #12 / code review gate | **NOT VERIFIED** | Code/config review confirms no scraping, embedding or framing. |
| NFR-12 | MVP-required | Session can access only its own investigations/comparisons | #1 | **NOT VERIFIED** | Cross-session authorization tests for every read/write path. |
| NFR-13 | MVP-required | Configurable rate limits on expensive public endpoints; HTTP 429 on limit | Issue #17 | **NOT VERIFIED** | Tracked in #17; concurrency/rate-limit tests and documented defaults. |
| NFR-14 | Proposed post-MVP | AI calls have timeouts and fallback on provider/format failure | #4 | **DEFERRED** | Provider tests after evidence slice; bounded timeout/fallback tests. |
| NFR-15 | Proposed post-MVP | External/user text cannot override AI rules or tools | #4 | **DEFERRED** | Prompt-injection tests using untrusted source attributes and user text. |
| NFR-16 | MVP-required | Keyboard access, focus, labels, status messaging; target WCAG 2.2 AA where practical | #18 | **NOT VERIFIED** | Keyboard-only review, automated accessibility scan and manual contrast/focus review. |
| NFR-17 | MVP-required | Support latest two major Chrome/Edge/Firefox and common mobile viewports | #18 | **NOT VERIFIED** | Browser/device matrix and responsive acceptance checks. |
| NFR-18 | MVP-required | Structured diagnostic logs without raw IPs | Issue #17 | **NOT VERIFIED** | Log-schema tests and review that identifiers/diagnostics omit raw IPs and secrets. |

## Traceability maintenance

1. Every requirement must map to a GitHub issue or a deliberately deferred item.
2. Each issue must have observable acceptance criteria and a separate reviewer.
3. Update the matrix when requirements, issue ownership or implementation status changes.
4. Mark a requirement complete only after acceptance evidence is linked (tests, CI run, source verification record or reproducible manual check).
5. Do not equate a green CI run with all requirements passing; CI currently runs lint/format/tests and frontend type/build checks, not live source verification or PostGIS migration tests.
