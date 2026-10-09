# HazardLens Database Schema Reconciliation

**Baseline:** SRS v3.1, §4.6 and §4.7  
**Status:** Proposed logical design for team review; the full inventory must be reconciled before implementation, but physical tables and migrations are to be implemented incrementally as MVP workflows require.  
**Purpose:** Resolve the mismatch between the SRS data model and GitHub issue #1 before writing SQLAlchemy models or Alembic migrations. The inventory is not a requirement to create all 14 tables in the first migration.

## 1. Naming decision

Use the exact table names in SRS §4.6. In particular, the canonical dataset table is `dataset`, not `hazard_dataset`. Do not silently rename tables or omit entities from the approved SRS.

## 2. Required table inventory

| Table | Required fields stated by SRS §4.6 | Relationship / lifecycle contract |
|---|---|---|
| `dataset` | `key`, `name`, `description` | Parent of `dataset_source`; registry data, not per-investigation data. |
| `data_source` | `agency`, `attribution`, `terms_url` | Parent of `dataset_source`; source identity and attribution. |
| `dataset_source` | `dataset_id` FK, `data_source_id` FK, `access_path`, `base_url`, `layer`, `extent`, `priority`, `active`, `last_checked` | Joins dataset to a configured source; parent of `hazard_class` and `evidence_result`. Do not delete source-registry rows as a side effect of expiring a session. |
| `hazard_class` | `dataset_source_id` FK, `code`, `label`, `definition_text` | Source-scoped official classification; referenced by `evidence_match`. Preserve published source labels and definitions. |
| `location` | `geography` point, snapped latitude and longitude | Optional normalized selected-point record referenced by `investigation`; coordinate values use WGS84/EPSG:4326 and five-decimal snapping per FR-01. |
| `session` | `id`, `created_at`, `expires_at` | Anonymous session owner for investigations and saved comparisons; expires after 30 days under NFR-05. |
| `investigation` | nullable `location_id`, `session_id` FK, `selection_type` (`POINT`/`AREA`), `geometry`, `created_at`, `duration_ms` | Session-owned investigation; its geometry is the canonical point/polygon selection. Deleting a session cascades to its investigations. |
| `evidence_result` | `investigation_id` FK, `dataset_source_id` FK, `status`, `source_date_text`, `retrieved_at`, `origin`, `latency_ms`, `raw` JSONB | Investigation-scoped source evaluation. Deleting an investigation cascades to its evidence results. Status values follow SRS §4.5 and FR-04/FR-05. |
| `evidence_match` | `evidence_result_id` FK, `hazard_class_id` FK, `distance_band_m` | Child rows preserve all material matching features/classes. Deleting an evidence result cascades to its matches. |
| `weather_snapshot` | `investigation_id` FK, temperature, humidity, precipitation, wind, `valid_time` | Investigation-scoped weather data; deleting an investigation cascades to snapshots. Weather failure must not suppress hazard evidence. |
| `ai_generation` | `investigation_id` FK, `kind`, `provider`, `model`, `prompt_version`, `evidence_hash`, `output`, `created_at` | Investigation-scoped AI output with provenance; deleting an investigation cascades to generations. |
| `geocode_cache` | `normalized_query`, `response`, `expires_at` | Cache entries expire after 30 days; no raw IP storage. |
| `saved_comparison` | `session_id` FK, `name`, `created_at` | Session-owned comparison; deleting a session cascades to comparisons. |
| `comparison_investigation` | `comparison_id` FK, `investigation_id` FK, `position` | Join table for ordered investigations in a comparison. Deleting the comparison cascades to join rows; investigation deletion must not leave dangling join rows. |

**Count: 14 tables.** This inventory follows SRS §4.6 and includes both `location` and `comparison_investigation`, which were absent from the original issue checklist.

## 3. Required constraints and spatial rules

- Enable PostGIS and use SRID 4326 for user-selected point and polygon geometry unless the reviewed implementation documents a different storage contract.
- Use a geography point or equivalent WGS84 point storage for `location`; keep snapped latitude/longitude consistent with the canonical geometry.
- `investigation.selection_type` is constrained to `POINT` or `AREA`. Geometry validity, polygon simplicity, configured vertex limit and configured area limit are enforced before upstream calls.
- Evidence status is constrained to `FOUND`, `NO_EVIDENCE`, `OUTSIDE_COVERAGE`, `UNAVAILABLE`, or `UNSUPPORTED`.
- `FOUND` requires at least one `evidence_match`; all other statuses require zero matches. Enforce this in service logic and tests; if a database constraint cannot safely express the cross-table rule, do not pretend a simple row check enforces it.
- Use uniqueness where justified by stable keys: `dataset.key`; source-scoped `hazard_class(dataset_source_id, code)`; comparison membership `(comparison_id, investigation_id)` and/or ordered position `(comparison_id, position)`. Confirm source-specific edge cases before locking constraints.
- Index foreign keys and spatial geometry used in selection queries. Use GiST indexes for PostGIS geometry/geography as applicable.
- Keep source-registry records independent of anonymous-session cleanup.

## 4. Deletion and retention

1. Session cleanup deletes expired `session` rows where `expires_at < NOW()`.
2. `session` deletion cascades to `investigation` and `saved_comparison`.
3. `investigation` deletion cascades to `evidence_result`, `weather_snapshot`, and `ai_generation`.
4. `evidence_result` deletion cascades to `evidence_match`.
5. `saved_comparison` deletion cascades to `comparison_investigation`; investigation deletion must also clean up comparison join rows without deleting unrelated investigations or their parent comparisons.
6. `geocode_cache` cleanup deletes rows where `expires_at < NOW()`.
7. Dataset/source/class registry rows must not be cascaded away when a session expires. Choose restrictive or explicit archival/deactivation behavior for referenced registry rows.

## 5. Implementation gates

Before each migration merge, tests must prove the acceptance criteria for the tables and relationships introduced by that migration:

- clean PostGIS database can run alembic upgrade head from the documented baseline;
- the migration downgrade/recovery strategy is documented and tested;
- introduced geometry columns have the intended types and SRID;
- foreign keys, nullability, uniqueness, indexes and deletion behavior match the reviewed physical schema decision;
- where session-owned tables are introduced, expiry/cascade tests remove only that session's records;
- where evidence results/matches are introduced, status/match invariants are enforced at the service boundary and covered by tests;
- where comparison tables are introduced, membership cannot point to nonexistent investigations and deletion leaves no dangling join rows;
- where session access is introduced, one session cannot read another session's investigation by guessing an identifier.

The **logical design review** must account for all 14 SRS entities and their relationships before schema work is treated as planned. That does not mean all 14 physical tables must exist in the first migration. The first migration should contain only the minimal reviewed tables required by the agreed vertical slice; later tables should arrive with the feature/workflow that needs them and with corresponding tests.

## 6. Incremental implementation rule

Review the entire logical model once for consistency, privacy, retention and cross-entity relationships. Then stage implementation by actual MVP dependency. Do not add unused tables just to satisfy an inventory count, and do not omit a logical entity silently: record its planned phase and the issue that will introduce it. The first vertical slice may use a small subset of the logical model.

## 7. Deliberately not decided here

The SRS table list does not fully specify every SQL type, index, default, uniqueness rule, nullable column, source-registry update policy, or whether historical evidence should be restricted from deletion when registry rows are retired. The implementation PR must document these details as a schema decision and receive review. Do not infer a canonical design solely from the short column lists in §4.6.
