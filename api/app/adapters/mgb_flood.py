from datetime import UTC, datetime
from time import perf_counter
from typing import Any

import httpx

from app.config import settings
from app.schemas.flood_preview import EvidenceStatus, FloodEvidenceResult, FloodMatch

CLASS_LABELS = {
    "VHF": "Very High Susceptibility to Flooding",
    "HF": "High Susceptibility to Flooding",
    "MF": "Moderate Susceptibility to Flooding",
    "LF": "Low Susceptibility to Flooding",
}
MAX_MATCHES = 20


async def query_flood_evidence(
    latitude: float,
    longitude: float,
    client: httpx.AsyncClient,
) -> FloodEvidenceResult:
    started_at = perf_counter()
    retrieved_at = datetime.now(UTC)
    params = {
        "f": "json",
        "where": "1=1",
        "geometry": (f'{{"x":{longitude},"y":{latitude},"spatialReference":{{"wkid":4326}}}}'),
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "OBJECTID,FloodSusc",
        "returnGeometry": "false",
        "resultRecordCount": MAX_MATCHES,
    }
    try:
        payload: Any = None
        for attempt in range(2):
            try:
                response = await client.get(settings.mgb_flood_query_url, params=params)
            except (TimeoutError, httpx.TimeoutException):
                if attempt == 0:
                    continue
                raise
            if response.status_code >= 500 and attempt == 0:
                continue
            response.raise_for_status()
            payload = response.json()
            break

        if not isinstance(payload, dict) or "error" in payload:
            raise ValueError("The MGB service returned an invalid or error payload.")

        features = payload.get("features")
        if not isinstance(features, list):
            raise TypeError("The MGB response did not include a features array.")

        latency_ms = round((perf_counter() - started_at) * 1000)
        if not features:
            return FloodEvidenceResult(
                source_url=settings.mgb_flood_query_url,
                status=EvidenceStatus.UNAVAILABLE,
                matches=[],
                retrieved_at=retrieved_at,
                latency_ms=latency_ms,
                raw={"feature_count": 0},
                message=(
                    "The source query returned no features, but coverage at this point has "
                    "not been established. No hazard conclusion can be drawn."
                ),
            )

        matches: list[FloodMatch] = []
        raw_features: list[dict[str, Any]] = []
        for feature in features[:MAX_MATCHES]:
            if not isinstance(feature, dict):
                raise TypeError("The MGB response contained a malformed feature.")
            attributes = feature.get("attributes")
            if not isinstance(attributes, dict):
                raise TypeError("The MGB response contained malformed feature attributes.")
            raw_code = attributes.get("FloodSusc")
            if not isinstance(raw_code, str) or not raw_code.strip():
                raise ValueError("A matching feature did not include its FloodSusc classification.")
            code = raw_code.strip()
            matches.append(
                FloodMatch(
                    class_code=code,
                    class_label=CLASS_LABELS.get(code, code),
                )
            )
            raw_features.append(
                {
                    "OBJECTID": attributes.get("OBJECTID"),
                    "FloodSusc": code,
                }
            )

        matches.sort(key=lambda match: (match.class_code, match.distance_band_m or 0))
        return FloodEvidenceResult(
            source_url=settings.mgb_flood_query_url,
            status=EvidenceStatus.FOUND,
            matches=matches,
            retrieved_at=retrieved_at,
            latency_ms=latency_ms,
            raw={"features": raw_features, "returned_feature_count": len(features)},
        )
    except (TimeoutError, httpx.TimeoutException):
        return FloodEvidenceResult(
            source_url=settings.mgb_flood_query_url,
            status=EvidenceStatus.UNAVAILABLE,
            matches=[],
            retrieved_at=retrieved_at,
            latency_ms=round((perf_counter() - started_at) * 1000),
            raw={},
            message="The MGB flood source timed out. No hazard conclusion can be drawn.",
        )
    except (httpx.HTTPError, ValueError, TypeError, KeyError):
        return FloodEvidenceResult(
            source_url=settings.mgb_flood_query_url,
            status=EvidenceStatus.UNAVAILABLE,
            matches=[],
            retrieved_at=retrieved_at,
            latency_ms=round((perf_counter() - started_at) * 1000),
            raw={},
            message="The MGB flood source could not provide a valid response.",
        )
