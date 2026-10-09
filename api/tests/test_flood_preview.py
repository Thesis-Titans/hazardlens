from unittest.mock import AsyncMock

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routers.flood_preview import get_http_client


class FakeResponse:
    status_code = 200

    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

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
async def test_found_result_preserves_source_classification_and_rounds_coordinates() -> None:
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
    result = body["results"][0]
    assert result["status"] == "FOUND"
    assert result["matches"] == [
        {"class_code": "HF", "class_label": "High Susceptibility to Flooding"},
        {"class_code": "VHF", "class_label": "Very High Susceptibility to Flooding"},
    ]
    assert "not a complete multi-hazard investigation" in body["limitation"]
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
async def test_upstream_timeout_is_unavailable_not_no_evidence() -> None:
    fake_client = AsyncMock()
    fake_client.get.side_effect = httpx.ReadTimeout("upstream timeout")

    response = await request_with_fake_client(
        fake_client,
        {"latitude": 10.72, "longitude": 122.56},
    )

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["status"] == "UNAVAILABLE"
    assert result["matches"] == []


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
