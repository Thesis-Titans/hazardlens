# HazardLens Official Source Verification Notes

**Status:** Metadata research only; not a source-integration approval or live-query verification.  
**Prepared:** 9 October 2026  
**Purpose:** Capture the currently identified official ArcGIS layer candidates, what their published metadata supports, and the unresolved checks that must be completed before integration.

## Important evidence distinction

This note records metadata visible from official service pages. Reading a layer's metadata is not the same as executing and validating a live feature query. No source below should be marked production-verified until the source owner records a live request, sanitized response, query parameters, observed latency, coverage interpretation, and failure behavior. An advertised service extent is a bounding extent, not proof that every point within it has mapped features.

## Candidate layer inventory

| Hazard | Candidate official layer | Published metadata observed | Unresolved before integration |
|---|---|---|---|
| MGB flood susceptibility | [Detailed Flood Susceptibility — FeatureServer/0](https://controlmap.mgb.gov.ph/arcgis/rest/services/GeospatialDataInventory/GDI_Detailed_Flood_Susceptibility/FeatureServer/0) | Polygon geometry; spatial reference EPSG:3857; query operation advertised; classification field FloodSusc with VHF, HF, MF and LF labels; maximum record count 2,000. The layer fields shown in metadata do not include a publication-date field. | Independently execute a point query; verify the ArcGIS spatial query parameter/axis-order handling; test known in-coverage points; determine whether an empty response can mean no intersecting feature or can also reflect gaps/coverage limits. Do not invent a publication date. |
| MGB rain-induced landslide susceptibility | [Detailed Rain-induced Landslide Susceptibility — FeatureServer/0](https://controlmap.mgb.gov.ph/arcgis/rest/services/GeospatialDataInventory/GDI_Detailed_Rain_induced_Landslide_Susceptibility/FeatureServer/0) | Polygon geometry; spatial reference EPSG:3857; query operation advertised; class field LndslideSusc with VHL (Very High), HL (High), ML (Moderate), LL (Low), and DF (Debris flow path/Possible accumulation zone). The listed layer fields do not expose a publication-date field. | Independently execute a live point query and verify coordinate transformation/parameter behavior; document whether DF is a distinct class or special mapping category; establish coverage and valid-empty semantics from evidence, not extent alone. |
| PHIVOLCS active faults | Candidate: [ActiveFaultGeneric — MapServer/0](https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCS/ActiveFaultGeneric/MapServer/0) | Search-indexed official metadata identifies polyline geometry in EPSG:4326, query support, a layer named AF_2025_asofJanuary, and fields including fccode, ttcode, datemapped, and publishdate. Active vs potentially active and trace type have source-coded values. | Direct page access returned an ArcGIS application error during this review, so current availability is **not verified**. Recheck service access, exact current layer ID, source attribution/date and codes. Define a defensible proximity query rule and communicate that distance is not a universal hazard score. An older PHIVOLCS HAS_AF layer is also discoverable but describes the source as of July 2018; do not silently substitute it for the newer candidate. |
| PHIVOLCS liquefaction | [Liquefaction — FeatureServer/0](https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCS/Liquefaction_ohas/FeatureServer/0) | Polygon geometry; spatial reference EPSG:4326; query operation advertised; field lccode plus liqcode, liqcodepk, datemapped, and publishdate. Metadata renderer lists codes 01–07 with labels including Generally Susceptible, Low/Moderate/High Potential, Least Susceptible, Moderately Susceptible and Highly Susceptible. The service description says the map was processed using geology, active-fault presence, historical liquefaction, geomorphology, hydrology and preliminary microtremor survey data. | Independently query and inspect actual returned features. Verify the code/label mapping and whether the mixed wording is intentional source taxonomy; preserve source labels rather than normalize them into a new severity scale. Confirm record-level publication/update dates and coverage/valid-empty semantics. |

## Cross-source rules

1. Record official URL, layer ID, query endpoint, geometry type, spatial reference, input geometry/coordinate order, query parameters, relevant fields, source date basis, attribution, timestamp, latency and sanitized response for each live check.
2. Use point/polygon intersection for polygon susceptibility layers only after the query has been validated. Faults are polylines: use a source-supported distance/proximity operation only after a team-reviewed distance interpretation is defined. Do not invent one common radius for all hazards.
3. Return FOUND only when at least one material matching feature is present. Return NO_EVIDENCE only when the query succeeded and source-specific coverage evidence justifies interpreting the empty response as no matching feature. Return OUTSIDE_COVERAGE only when a defensible source-specific coverage rule supports it. Otherwise use UNAVAILABLE or UNSUPPORTED as appropriate.
4. Treat malformed data, timeout, server errors and service outages as unavailable evidence, never as an absence of hazard.
5. Keep source-reported class text unchanged. Do not turn class labels into a universal score, probability or safety determination.
6. Keep source publication/update date separate from request/retrieval time. If metadata does not state a date, say so rather than inferring one from the current date or a service name.
7. Store sanitized responses as clearly labelled recorded fixtures for deterministic offline tests. Fixtures are not evidence that the live service is currently available or that recorded conditions are current.
8. Re-check source terms and metadata at implementation time. Do not bulk-copy or host official geometries unless the applicable terms explicitly permit it.

## References

- MGB Detailed Flood Susceptibility layer metadata: https://controlmap.mgb.gov.ph/arcgis/rest/services/GeospatialDataInventory/GDI_Detailed_Flood_Susceptibility/FeatureServer/0
- MGB Detailed Rain-induced Landslide Susceptibility layer metadata: https://controlmap.mgb.gov.ph/arcgis/rest/services/GeospatialDataInventory/GDI_Detailed_Rain_induced_Landslide_Susceptibility/FeatureServer/0
- PHIVOLCS ActiveFaultGeneric candidate: https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCS/ActiveFaultGeneric/MapServer/0
- PHIVOLCS older HAS_AF candidate: https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCS/HAS_AF/MapServer/0
- PHIVOLCS Liquefaction layer metadata: https://gisweb.phivolcs.dost.gov.ph/arcgis/rest/services/PHIVOLCS/Liquefaction_ohas/FeatureServer/0
- Public Nominatim usage policy (separate geocoding dependency): https://operations.osmfoundation.org/policies/nominatim/
