import httpx
from fastapi import APIRouter, Depends

from app.adapters.mgb_flood import query_flood_evidence
from app.schemas.flood_preview import FloodPreviewRequest, FloodPreviewResponse


router = APIRouter(tags=["investigations"])


async def get_http_client():
    async with httpx.AsyncClient(timeout=10.0) as client:
        yield client


@router.post("/v1/preview/flood", response_model=FloodPreviewResponse)
async def preview_flood_investigation(
    request: FloodPreviewRequest,
    client: httpx.AsyncClient = Depends(get_http_client),
) -> FloodPreviewResponse:
    result = await query_flood_evidence(request.latitude, request.longitude, client)
    return FloodPreviewResponse(
        latitude=request.latitude,
        longitude=request.longitude,
        results=[result],
    )
