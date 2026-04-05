from __future__ import annotations

from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Query, Request, status

from app.clients.base import BaseGoogleClient, GoogleAPIError
from app.core.config import get_settings


DEFAULT_FIELD_MASK = ",".join(
    [
        "routes.duration",
        "routes.distanceMeters",
        "routes.travelAdvisory.transitFare",
        "routes.legs.duration",
        "routes.legs.distanceMeters",
        "routes.legs.steps.travelMode",
        "routes.legs.steps.staticDuration",
        "routes.legs.steps.navigationInstruction.instructions",
        "routes.legs.steps.transitDetails",
    ]
)


router = APIRouter(prefix="/api/v1/routes-direct", tags=["routes-direct"])


@router.post("/compute")
async def compute_routes_direct(
    payload: dict[str, Any],
    request: Request,
    field_mask: str = Query(
        default=DEFAULT_FIELD_MASK,
        alias="fieldMask",
        description=(
            "Google Routes field mask sent as X-Goog-FieldMask. "
            "Use '*' only for debugging; prefer explicit fields in production."
        ),
    ),
) -> dict[str, Any]:
    settings = getattr(request.app.state, "settings", get_settings())
    http_client = getattr(request.app.state, "http_client", None)
    if http_client is None:
        http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.planner_request_timeout_seconds)
        )
        request.app.state.http_client = http_client

    client = BaseGoogleClient(http_client=http_client, settings=settings)
    try:
        return await client.post_json(
            f"{settings.routes_base_url}/directions/v2:computeRoutes",
            json_payload=payload,
            headers={
                "X-Goog-Api-Key": client.require_maps_api_key(),
                "X-Goog-FieldMask": field_mask,
            },
        )
    except GoogleAPIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
# Example request payload:{
#   "origin": { "address": "phoenix" },
#   "destination": { "address": "tempe" },
#   "travelMode": "TRANSIT",
#   "departureTime": "2026-04-06T09:00:00+09:00",
#   "computeAlternativeRoutes": true,
#   "transitPreferences": { "routingPreference": "LESS_WALKING","allowedTravelModes": ["TRAIN"] },
#   "languageCode": "jp"
# }
