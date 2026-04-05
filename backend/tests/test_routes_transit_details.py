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
                                "departureTime": "2026-04-05T09:00:00Z",
                                "arrivalTime": "2026-04-05T09:26:00Z",
                            },
                            "localizedValues": {
                                "departureTime": {"time": {"text": "18:00"}},
                                "arrivalTime": {"time": {"text": "18:26"}},
                            },
                            "transitLine": {
                                "name": "Tokyo Metro Ginza Line",
                                "nameShort": "Ginza Line",
                                "uri": "https://example.com/ginza",
                                "color": "#F5A623",
                                "textColor": "#000000",
                                "agencies": [{"name": "Tokyo Metro"}],
                                "vehicle": {"type": "SUBWAY"},
                            },
                            "headsign": "Asakusa",
                            "stopCount": 12,
                            "headway": "600s",
                            "tripShortText": "G123",
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
    assert details["departure_time"] == "2026-04-05T09:00:00Z"
    assert details["arrival_time"] == "2026-04-05T09:26:00Z"
    assert details["localized_departure_time"] == "18:00"
    assert details["localized_arrival_time"] == "18:26"
    assert details["headway_minutes"] == 10
    assert details["trip_short_text"] == "G123"
    assert details["transit_agency_names"] == ["Tokyo Metro"]
    assert details["transit_line_uri"] == "https://example.com/ginza"
    assert details["transit_line_color"] == "#F5A623"
    assert details["transit_line_text_color"] == "#000000"


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


def test_extract_transit_fare_from_advisory() -> None:
    client = RoutesClient(http_client=httpx.AsyncClient(), settings=Settings())
    amount, currency = client._extract_transit_fare(
        {
            "transitFare": {
                "currencyCode": "JPY",
                "units": "320",
                "nanos": 0,
            }
        }
    )

    assert amount == 320.0
    assert currency == "JPY"


def test_extract_station_walk_minutes_ignores_missing_walk_duration() -> None:
    client = RoutesClient(http_client=httpx.AsyncClient(), settings=Settings())
    route = {
        "legs": [
            {
                "steps": [
                    {
                        "travelMode": "WALK",
                    },
                    {
                        "travelMode": "TRANSIT",
                        "transitDetails": {
                            "stopDetails": {
                                "departureStop": {"name": "Shinjuku Station"},
                                "arrivalStop": {"name": "Asakusa Station"},
                            },
                            "transitLine": {"nameShort": "Ginza Line"},
                            "headsign": "Asakusa",
                            "stopCount": 12,
                        },
                    },
                    {
                        "travelMode": "WALK",
                        "duration": "120s",
                    },
                ]
            }
        ]
    }

    walk_before, walk_after = client._extract_station_walk_minutes(route)

    assert walk_before is None
    assert walk_after == 2
