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


class FloodMatch(BaseModel):
    class_code: str
    class_label: str


class FloodEvidenceResult(BaseModel):
    dataset_key: str = "mgb_detailed_flood"
    dataset_name: str = "Detailed Flood Susceptibility"
    agency: str = "Mines and Geosciences Bureau (MGB)"
    source_url: str
    status: EvidenceStatus
    matches: list[FloodMatch] = Field(default_factory=list)
    retrieved_at: datetime
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
