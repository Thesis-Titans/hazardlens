from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class EvidenceStatus(StrEnum):
    FOUND = "FOUND"
    NO_EVIDENCE = "NO_EVIDENCE"
    OUTSIDE_COVERAGE = "OUTSIDE_COVERAGE"
    UNAVAILABLE = "UNAVAILABLE"
    UNSUPPORTED = "UNSUPPORTED"


class FloodPreviewRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    @field_validator("latitude", "longitude")
    @classmethod
    def round_coordinates(cls, value: float) -> float:
        return round(value, 5)


class SourceDate(BaseModel):
    text: str
    basis: str


class FloodMatch(BaseModel):
    class_code: str
    class_label: str
    distance_band_m: float | None = None


class FloodEvidenceResult(BaseModel):
    dataset_key: str = "flood"
    source_key: str = "mgb_detailed_flood"
    status: EvidenceStatus
    result_type: str = "containment"
    matches: list[FloodMatch] = Field(default_factory=list)
    source_date: SourceDate = Field(
        default_factory=lambda: SourceDate(
            text="Not stated in the published layer metadata",
            basis="metadata_not_provided",
        )
    )
    retrieved_at: datetime
    origin: str = "live"
    latency_ms: int = Field(ge=0)
    raw: dict = Field(default_factory=dict)
    source_url: str
    agency: str = "Mines and Geosciences Bureau (MGB)"
    attribution: str = "Source: Mines and Geosciences Bureau (MGB), Detailed Flood Susceptibility."
    message: str | None = None


class FloodPreviewResponse(BaseModel):
    latitude: float
    longitude: float
    results: list[FloodEvidenceResult]
    limitation: str = (
        "Preview endpoint for the flood source only. This is not a complete multi-hazard "
        "investigation and does not create a persisted investigation."
    )
