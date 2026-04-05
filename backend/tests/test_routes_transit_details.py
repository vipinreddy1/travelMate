import httpx

from app.clients.maps import RoutesClient
from app.core.config import Settings
from app.models.planning import TransportMode


def _sample_transit_route() -> dict:
    return {
        "legs": [
            {
                "steps": [
                    {
                        "travelMode": "WALK",
                        "staticDuration": "300s",
                        "navigationInstruction": {"instructions": "Walk to Shinjuku Station"},
                    },
                    {
                        "travelMode": "TRANSIT",
                        "staticDuration": "1500s",
                        "transitDetails": {
                            "stopDetails": {
                                "departureStop": {"name": "Shinjuku Station"},
                                "arrivalStop": {"name": "Asakusa Station"},
                            },
                            "transitLine": {
                                "name": "Tokyo Metro Ginza Line",
                                "nameShort": "Ginza Line",
                                "vehicle": {"type": "SUBWAY"},
                            },
                            "headsign": "Asakusa",
                            "stopCount": 12,
                        },
                    },
                    {
                        "travelMode": "WALK",
                        "staticDuration": "240s",
                        "navigationInstruction": {"instructions": "Walk to destination"},
                    },
                ]
            }
        ]
    }


def test_extract_transit_details_from_route() -> None:
    client = RoutesClient(http_client=httpx.AsyncClient(), settings=Settings())
    details = client._extract_transit_details(_sample_transit_route())

    assert details["departure_stop"] == "Shinjuku Station"
    assert details["arrival_stop"] == "Asakusa Station"
    assert details["transit_line"] == "Ginza Line"
    assert details["transit_headsign"] == "Asakusa"
    assert details["transit_stop_count"] == 12
    assert details["vehicle_type"] == "SUBWAY"


def test_extract_station_walk_minutes() -> None:
    client = RoutesClient(http_client=httpx.AsyncClient(), settings=Settings())
    walk_before, walk_after = client._extract_station_walk_minutes(_sample_transit_route())

    assert walk_before == 5
    assert walk_after == 4


def test_extract_step_instructions_for_transit() -> None:
    client = RoutesClient(http_client=httpx.AsyncClient(), settings=Settings())
    instructions = client._extract_step_instructions(
        _sample_transit_route(),
        TransportMode.TRANSIT,
    )

    assert any("Take Ginza Line from Shinjuku Station to Asakusa Station" in item for item in instructions)
    assert any("Walk to Shinjuku Station." == item for item in instructions)
