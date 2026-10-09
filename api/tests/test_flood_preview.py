from unittest.mock import AsyncMock

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routers.flood_preview import get_http_client


class FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200) -> None:
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            request = httpx.Request("GET", "https://example.test/source")
            response = httpx.Response(self.status_code, request=request)
            response.raise_for_status()

    def json(self) -> dict:
        return self.payload


async def request_with_fake_client(fake_client: object, payload: dict) -> httpx.Response:
    async def override_client():
        yield fake_client

    app.dependency_overrides[get_http_client] = override_client
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            return await client.post("/v1/preview/flood", json=payload)
    finally:
        app.dependency_overrides.pop(get_http_client, None)


@pytest.mark.asyncio
async def test_found_result_matches_srs_contract_and_preserves_features() -> None:
    fake_client = AsyncMock()
    fake_client.get.return_value = FakeResponse(
        {
            "features": [
                {"attributes": {"OBJECTID": 2, "FloodSusc": "HF"}},
                {"attributes": {"OBJECTID": 1, "FloodSusc": "VHF"}},
                {"attributes": {"OBJECTID": 3, "FloodSusc": "HF"}},
            ]
        }
    )

    response = await request_with_fake_client(
        fake_client,
        {"latitude": 10.720234, "longitude": 122.562149},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["latitude"] == 10.72023
    assert body["longitude"] == 122.56215
    assert "not a complete multi-hazard investigation" in body["limitation"]
    result = body["results"][0]
    assert result["dataset_key"] == "flood"
    assert result["source_key"] == "mgb_detailed_flood"
    assert result["status"] == "FOUND"
    assert result["result_type"] == "containment"
    assert result["origin"] == "live"
    assert result["latency_ms"] >= 0
    assert result["source_date"]["basis"] == "metadata_not_provided"
    assert result["matches"] == [
        {"class_code": "HF", "class_label": "High Susceptibility to Flooding", "distance_band_m": None},
        {"class_code": "HF", "class_label": "High Susceptibility to Flooding", "distance_band_m": None},
        {"class_code": "VHF", "class_label": "Very High Susceptibility to Flooding", "distance_band_m": None},
    ]
    assert len(result["raw"]["features"]) == 3
    fake_client.get.assert_awaited_once()


@pytest.mark.asyncio
async def test_empty_response_with_unverified_coverage_is_unavailable() -> None:
    fake_client = AsyncMock()
    fake_client.get.return_value = FakeResponse({"features": []})

    response = await request_with_fake_client(
        fake_client,
        {"latitude": 10.72, "longitude": 122.56},
    )

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["status"] == "UNAVAILABLE"
    assert result["matches"] == []
    assert "coverage" in result["message"]


@pytest.mark.asyncio
async def test_upstream_timeout_is_unavailable_and_retried_once() -> None:
    fake_client = AsyncMock()
    fake_client.get.side_effect = [
        httpx.ReadTimeout("upstream timeout"),
        httpx.ReadTimeout("upstream timeout"),
    ]

    response = await request_with_fake_client(
        fake_client,
        {"latitude": 10.72, "longitude": 122.56},
    )

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["status"] == "UNAVAILABLE"
    assert result["matches"] == []
    assert fake_client.get.await_count == 2


@pytest.mark.asyncio
async def test_upstream_server_error_is_retried_once() -> None:
    fake_client = AsyncMock()
    fake_client.get.side_effect = [
        FakeResponse({"error": "temporarily unavailable"}, status_code=503),
        FakeResponse({"features": [{"attributes": {"FloodSusc": "HF", "OBJECTID": 1}}]}),
    ]

    response = await request_with_fake_client(
        fake_client,
        {"latitude": 10.72, "longitude": 122.56},
    )

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["status"] == "FOUND"
    assert fake_client.get.await_count == 2


@pytest.mark.asyncio
async def test_malformed_upstream_payload_is_unavailable() -> None:
    fake_client = AsyncMock()
    fake_client.get.return_value = FakeResponse({"unexpected": []})

    response = await request_with_fake_client(
        fake_client,
        {"latitude": 10.72, "longitude": 122.56},
    )

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["status"] == "UNAVAILABLE"
    assert result["matches"] == []


@pytest.mark.asyncio
async def test_invalid_coordinates_are_rejected_before_upstream_call() -> None:
    fake_client = AsyncMock()
    fake_client.get.return_value = FakeResponse({"features": []})

    response = await request_with_fake_client(
        fake_client,
        {"latitude": 95, "longitude": 122.56},
    )

    assert response.status_code == 422
    fake_client.get.assert_not_awaited()
