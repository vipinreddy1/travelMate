import httpx

from app.clients.gemini import GeminiClient
from app.core.config import Settings


def test_normalize_planning_payload_coerces_constraint_strength() -> None:
    client = GeminiClient(http_client=httpx.AsyncClient(), settings=Settings())
    payload = {
        "raw_request": "test",
        "destination": {"value": "Kyoto"},
        "hard_constraints": [
            {"key": "budget_cap", "description": "cap spend", "strength": "must"},
            {"key": "pace", "description": "relaxed", "strength": "should"},
            {"key": "misc", "description": "misc", "strength": "weird-value"},
        ],
        "transport_preference": "fastest",
    }

    normalized = client._normalize_planning_payload(payload)

    assert normalized["hard_constraints"][0]["strength"] == "hard"
    assert normalized["hard_constraints"][1]["strength"] == "soft"
    assert normalized["hard_constraints"][2]["strength"] == "soft"
    assert normalized["transport_preference"] == "optimize_for_time"


def test_normalize_planning_payload_coerces_soft_preference_weights() -> None:
    client = GeminiClient(http_client=httpx.AsyncClient(), settings=Settings())
    payload = {
        "raw_request": "test",
        "destination": {"value": "Kyoto"},
        "soft_preferences": [
            {"key": "food", "weight": "high"},
            {"key": "nature", "weight": "medium"},
            {"key": "museums", "weight": "low"},
            {"key": "shopping", "weight": "0.72"},
            {"key": "pace", "weight": "unknown"},
        ],
    }

    normalized = client._normalize_planning_payload(payload)

    assert normalized["soft_preferences"][0]["weight"] == 0.9
    assert normalized["soft_preferences"][1]["weight"] == 0.6
    assert normalized["soft_preferences"][2]["weight"] == 0.3
    assert normalized["soft_preferences"][3]["weight"] == 0.72
    assert normalized["soft_preferences"][4]["weight"] == 0.5


def test_normalize_execution_plan_normalizes_route_request_and_time_conflict() -> None:
    client = GeminiClient(http_client=httpx.AsyncClient(), settings=Settings())
    payload = {
        "direct_answer_only": False,
        "use_places": True,
        "use_routes": True,
        "build_itinerary": True,
        "search_focus": ["ramen"],
        "action_order": ["search_places", "compute_routes", "build_itinerary"],
        "route_request": {
            "compute_alternative_routes": True,
            "departure_time": "2026-04-06T09:00:00+09:00",
            "arrival_time": "2026-04-06T10:00:00+09:00",
            "transit_allowed_travel_modes": ["metro", "BUS", "tram", "unknown"],
            "transit_routing_preference": "less walking",
        },
    }

    normalized = client._normalize_execution_plan(payload, raw_request="route options")

    assert normalized["route_request"]["compute_alternative_routes"] is True
    assert normalized["route_request"]["departure_time"] == "2026-04-06T09:00:00+09:00"
    assert normalized["route_request"]["arrival_time"] is None
    assert normalized["route_request"]["transit_allowed_travel_modes"] == [
        "SUBWAY",
        "BUS",
        "LIGHT_RAIL",
    ]
    assert normalized["route_request"]["transit_routing_preference"] == "LESS_WALKING"


def test_normalize_execution_plan_direct_answer_clears_route_request() -> None:
    client = GeminiClient(http_client=httpx.AsyncClient(), settings=Settings())
    payload = {
        "direct_answer_only": True,
        "use_places": True,
        "use_routes": True,
        "build_itinerary": True,
        "action_order": ["search_places"],
        "route_request": {
            "compute_alternative_routes": True,
            "departure_time": "2026-04-06T09:00:00+09:00",
            "arrival_time": None,
            "transit_allowed_travel_modes": ["BUS"],
            "transit_routing_preference": "FEWER_TRANSFERS",
        },
    }

    normalized = client._normalize_execution_plan(payload, raw_request="what is jet lag")

    assert normalized["action_order"] == ["direct_answer"]
    assert normalized["route_request"]["compute_alternative_routes"] is False
    assert normalized["route_request"]["departure_time"] is None
    assert normalized["route_request"]["arrival_time"] is None
    assert normalized["route_request"]["transit_allowed_travel_modes"] == []
    assert normalized["route_request"]["transit_routing_preference"] is None
