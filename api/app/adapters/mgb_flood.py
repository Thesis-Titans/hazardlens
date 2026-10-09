from datetime import UTC, datetime
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


async def query_flood_evidence(
    latitude: float,
    longitude: float,
    client: httpx.AsyncClient,
) -> FloodEvidenceResult:
    retrieved_at = datetime.now(UTC)
    try:
        response = await client.get(
            settings.mgb_flood_query_url,
            params={
                "f": "json",
                "where": "1=1",
                "geometry": (
                    '{"x":'
                    f"{longitude}"
                    ',"y":'
                    f"{latitude}"
                    ',"spatialReference":{"wkid":4326}}'
                ),
                "geometryType": "esriGeometryPoint",
                "inSR": "4326",
                "spatialRel": "esriSpatialRelIntersects",
                "outFields": "OBJECTID,FloodSusc",
                "returnGeometry": "false",
            },
        )
        response.raise_for_status()
        payload: Any = response.json()
        if not isinstance(payload, dict) or "error" in payload:
            raise ValueError("The MGB service returned an invalid or error payload.")

        features = payload.get("features")
        if not isinstance(features, list):
            raise TypeError("The MGB response did not include a features array.")

        if not features:
            return FloodEvidenceResult(
                source_url=settings.mgb_flood_query_url,
                status=EvidenceStatus.NO_EVIDENCE,
                matches=[],
                retrieved_at=retrieved_at,
                message="The source query succeeded but returned no matching flood features.",
            )

        matches: list[FloodMatch] = []
        for feature in features:
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

        unique_matches = {
            (match.class_code, match.class_label): match for match in matches
        }
        ordered_matches = [
            unique_matches[key] for key in sorted(unique_matches, key=lambda item: item[0])
        ]
        return FloodEvidenceResult(
            source_url=settings.mgb_flood_query_url,
            status=EvidenceStatus.FOUND,
            matches=ordered_matches,
            retrieved_at=retrieved_at,
        )
    except (TimeoutError, httpx.TimeoutException):
        return FloodEvidenceResult(
            source_url=settings.mgb_flood_query_url,
            status=EvidenceStatus.UNAVAILABLE,
            matches=[],
            retrieved_at=retrieved_at,
            message="The MGB flood source timed out. No hazard conclusion can be drawn.",
        )
    except (httpx.HTTPError, ValueError, TypeError, KeyError):
        return FloodEvidenceResult(
            source_url=settings.mgb_flood_query_url,
            status=EvidenceStatus.UNAVAILABLE,
            matches=[],
            retrieved_at=retrieved_at,
            message="The MGB flood source could not provide a valid response.",
        )
