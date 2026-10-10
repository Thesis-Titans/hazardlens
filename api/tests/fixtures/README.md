# Test Fixtures

These fixtures capture real HTTP responses from official Philippine government geospatial services, captured via live endpoint query.

## MGB Detailed Flood Susceptibility

- **Layer:** `GeospatialDataInventory/GDI_Detailed_Flood_Susceptibility/FeatureServer/0`
- **Host:** `controlmap.mgb.gov.ph`
- **Published Spatial Reference:** EPSG:3857 (Web Mercator)
- **Query Input Coordinate Reference:** EPSG:4326 (WGS 84 Point)

### Fixtures

1. `mgb_flood_iloilo_mf.json`: Query for Central Iloilo City (`10.7202 N, 122.5621 E`). Returned 1 feature: `{"OBJECTID": 41, "FloodSusc": "MF"}` (Moderate Susceptibility).
2. `mgb_flood_sea_empty.json`: Query for Panay Gulf offshore coordinate (`10.5000 N, 122.8000 E`). Returned `{"features": []}`.
