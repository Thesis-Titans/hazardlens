# HazardLens Decision Log

**Status:** Proposed decisions for team review  
**Baseline:** SRS v3.1 in draft PR #9; the team must approve the baseline before it becomes canonical.  
**Rule:** A decision is not final merely because it appears in this file. Record the decision owner, date, rationale, and affected requirements when the team agrees.

## Decision register

| ID | Topic | Current proposal / known fact | Status | Decision owner / next action |
|---|---|---|---|---|
| DEC-01 | SRS version | The SRS revision history already contains a v3.1 entry dated 9 Oct 2026, while front matter and architecture/verification headers on `main` still identify v3.0. PR #9 aligns the headers. | **Pending team review** | Project lead + reviewer: approve or correct PR #9. |
| DEC-02 | Database schema | SRS §4.6 names 14 tables, including `dataset`, `location`, and `comparison_investigation`. Issue #1 previously used `hazard_dataset` and omitted two tables. | **Proposed; migration blocked** | Database owner + project lead: review `docs/schema-reconciliation.md`; document types, nullability, constraints, indexes and deletion semantics before migration PR. |
| DEC-03 | Evidence status semantics | Use `FOUND`, `NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, `UNSUPPORTED`. A source error or timeout is not `NO_EVIDENCE`. `OUTSIDE_COVERAGE` requires a defensible coverage rule. | **Product rule in SRS; source-specific verification pending** | Project lead + source owner + QA: confirm semantics against each layer. |
| DEC-04 | Geocoding provider and interaction | Issue #7 proposes autocomplete. The public Nominatim service explicitly prohibits autocomplete and requires a valid identifying User-Agent/Referer, attribution and a maximum of one request per second. | **Blocked pending provider/UX choice** | Backend + frontend owners: choose a compliant one-shot search or another provider; document caching, rate limits, attribution and fallback. See https://operations.osmfoundation.org/policies/nominatim/. |
| DEC-05 | First sprint goal | Build a verified source → normalized API result → evidence UI vertical slice before multi-provider AI and other advanced features. | **Recommended; team confirmation required** | Whole team: confirm at sprint planning; adjust only with an explicit scope decision. |
| DEC-06 | MGB flood preview | PR #11 implements a limited preview adapter using published layer metadata. The layer metadata does not state a publication date; the adapter does not invent one. Live point-query behavior and coverage-based empty-result semantics were not independently confirmed. | **Partial technical evidence** | Source owner + QA: independently verify a live query, capture sanitized fixture, document coverage and source date behavior. |
| DEC-07 | Health semantics | Current `/v1/health` returns static application status and does not check dependencies. | **Open** | Backend owner + project lead: decide liveness/readiness contract and tests before expanding health reporting. |
| DEC-08 | AI provider evaluation | AI is an enhancement layer; core evidence must work without AI. Defer provider/tool-calling work until the evidence vertical slice and source status semantics are verified. | **Recommended; reflected in issue #4 note** | Project lead: re-prioritize only after Sprint 1 exit criteria are met. |
| DEC-09 | Team roles and capacity | README and issues suggest five work tracks, but role assignments are starting proposals and availability is not verified. | **Open** | Whole team: confirm ownership and nominate a separate reviewer for each issue. |
| DEC-10 | Sprint dates | SRS says about eight weeks; no exact project start/deadline was established in the available evidence. | **Open** | Team: confirm dates and real capacity before creating or changing due dates. |

## How to close a decision

For each open item, record:
- agreed outcome and alternatives rejected;
- decision owner and date;
- evidence/source consulted;
- affected SRS requirements, issues and code;
- follow-up work and how the result will be verified.

For decisions that alter requirements, update the SRS and traceability matrix in the same review cycle. Do not treat comments in a PR as the only permanent record of a product decision.
