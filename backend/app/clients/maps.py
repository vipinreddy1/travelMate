from __future__ import annotations

import asyncio
import math
import re
from datetime import UTC, datetime
from typing import Iterable

from app.clients.base import BaseGoogleClient, GoogleAPIError
from app.models.planning import CandidatePlace, PlaceLocation, TransportMode, TravelStep


PRICE_LEVEL_MAP = {
    "PRICE_LEVEL_FREE": 0,
    "PRICE_LEVEL_INEXPENSIVE": 1,
    "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3,
    "PRICE_LEVEL_VERY_EXPENSIVE": 4,
}


class PlacesClient(BaseGoogleClient):
    async def search_text(
        self,
        *,
        text_query: str,
        language_code: str,
        region_code: str,
        max_results: int,
    ) -> list[CandidatePlace]:
        if not self.settings.planner_enable_google_calls:
            raise GoogleAPIError("Google calls are disabled by configuration.")

        headers = {
            "X-Goog-Api-Key": self.require_maps_api_key(),
            "X-Goog-FieldMask": ",".join(
                [
                    "places.id",
                    "places.displayName",
                    "places.formattedAddress",
                    "places.location",
                    "places.primaryType",
                    "places.rating",
                    "places.userRatingCount",
                    "places.priceLevel",
                    "places.googleMapsUri",
                    "places.editorialSummary",
                ]
            ),
        }
        payload = {
            "textQuery": text_query,
            "languageCode": language_code,
            "regionCode": region_code,
            "maxResultCount": max_results,
        }
        data = await self.post_json(
            f"{self.settings.places_base_url}/places:searchText",
            json_payload=payload,
            headers=headers,
        )

        places: list[CandidatePlace] = []
        for raw_place in data.get("places", []):
            location = raw_place.get("location") or {}
            if "latitude" not in location or "longitude" not in location:
                continue
            places.append(
                CandidatePlace(
                    place_id=raw_place["id"],
                    name=(raw_place.get("displayName") or {}).get("text", "Unknown place"),
                    address=raw_place.get("formattedAddress"),
                    location=PlaceLocation(
                        lat=location["latitude"],
                        lng=location["longitude"],
                    ),
                    primary_type=raw_place.get("primaryType"),
                    rating=raw_place.get("rating"),
                    user_rating_count=raw_place.get("userRatingCount"),
                    price_level=PRICE_LEVEL_MAP.get(raw_place.get("priceLevel")),
                    google_maps_uri=raw_place.get("googleMapsUri"),
                    editorial_summary=(raw_place.get("editorialSummary") or {}).get("text"),
                    source_query=text_query,
                )
            )

        return places


class RoutesClient(BaseGoogleClient):
    async def compute_route_maps_for_modes(
        self,
        *,
        places: Iterable[CandidatePlace],
        modes: Iterable[TransportMode],
        language_code: str,
    ) -> dict[TransportMode, dict[tuple[str, str], TravelStep]]:
        mode_list = list(dict.fromkeys(modes))
        tasks = [
            self.compute_route_map(
                places=places,
                mode=mode,
                language_code=language_code,
            )
            for mode in mode_list
        ]
        results = await asyncio.gather(*tasks)
        return {
            mode: route_map
            for mode, route_map in zip(mode_list, results, strict=True)
        }

    async def compute_route_map(
        self,
        *,
        places: Iterable[CandidatePlace],
        mode: TransportMode,
        language_code: str,
    ) -> dict[tuple[str, str], TravelStep]:
        place_list = list(places)
        if len(place_list) < 2:
            return {}

        route_map: dict[tuple[str, str], TravelStep] = {}
        tasks = [
            self.compute_route(
                origin=origin,
                destination=destination,
                mode=mode,
                language_code=language_code,
            )
            for origin in place_list
            for destination in place_list
            if origin.place_id != destination.place_id
        ]
        results = await asyncio.gather(*tasks)

        index = 0
        for origin in place_list:
            for destination in place_list:
                if origin.place_id == destination.place_id:
                    continue
                route_map[(origin.place_id, destination.place_id)] = results[index]
                index += 1

        return route_map

    async def compute_route(
        self,
        *,
        origin: CandidatePlace,
        destination: CandidatePlace,
        mode: TransportMode,
        language_code: str,
        departure_time: datetime | None = None,
        arrival_time: datetime | None = None,
        compute_alternative_routes: bool = False,
        transit_allowed_travel_modes: list[str] | None = None,
        transit_routing_preference: str | None = None,
    ) -> TravelStep:
        if not self.settings.planner_enable_google_calls or not self.settings.maps_api_key_value:
            return self._heuristic_route(origin, destination, mode)

        payload = {
            "origin": self._waypoint(origin),
            "destination": self._waypoint(destination),
            "travelMode": self._route_mode(mode),
            "languageCode": language_code,
        }
        if departure_time is not None:
            payload["departureTime"] = self._to_rfc3339(departure_time)
        if arrival_time is not None:
            payload["arrivalTime"] = self._to_rfc3339(arrival_time)
        if compute_alternative_routes:
            payload["computeAlternativeRoutes"] = True
        if mode == TransportMode.TRANSIT:
            transit_preferences: dict[str, object] = {}
            if transit_allowed_travel_modes:
                transit_preferences["allowedTravelModes"] = transit_allowed_travel_modes
            if transit_routing_preference:
                transit_preferences["routingPreference"] = transit_routing_preference
            if transit_preferences:
                payload["transitPreferences"] = transit_preferences
        headers = {
            "X-Goog-Api-Key": self.require_maps_api_key(),
            "X-Goog-FieldMask": ",".join(
                [
                    "routes.duration",
                    "routes.distanceMeters",
                    "routes.travelAdvisory",
                    "routes.legs.duration",
                    "routes.legs.distanceMeters",
                    "routes.legs.steps.distanceMeters",
                    "routes.legs.steps.staticDuration",
                    "routes.legs.steps.travelMode",
                    "routes.legs.steps.navigationInstruction.instructions",
                    "routes.legs.steps.transitDetails",
                ]
            ),
        }
        data = await self.post_json(
            f"{self.settings.routes_base_url}/directions/v2:computeRoutes",
            json_payload=payload,
            headers=headers,
        )
        routes = data.get("routes") or []
        if not routes:
            return self._heuristic_route(origin, destination, mode)

        route = routes[0]
        duration_seconds = self._duration_to_seconds(route.get("duration", "0s"))
        advisory = route.get("travelAdvisory") or {}
        note = None
        if advisory.get("tollInfo"):
            note = "Route may include tolls."
        transit_details = self._extract_transit_details(route)
        fare_amount, fare_currency = self._extract_transit_fare(advisory)
        walk_to_station_minutes, walk_from_station_minutes = self._extract_station_walk_minutes(route)
        step_instructions = self._extract_step_instructions(route, mode)
        cost_estimate = self._estimate_cost(
            mode=mode,
            distance_meters=route.get("distanceMeters"),
        )

        return TravelStep(
            mode=mode,
            duration_minutes=max(1, round(duration_seconds / 60)),
            distance_meters=route.get("distanceMeters"),
            cost_estimate=cost_estimate,
            note=note,
            departure_stop=transit_details.get("departure_stop"),
            arrival_stop=transit_details.get("arrival_stop"),
            transit_line=transit_details.get("transit_line"),
            transit_headsign=transit_details.get("transit_headsign"),
            transit_stop_count=transit_details.get("transit_stop_count"),
            vehicle_type=transit_details.get("vehicle_type"),
            departure_time=transit_details.get("departure_time"),
            arrival_time=transit_details.get("arrival_time"),
            localized_departure_time=transit_details.get("localized_departure_time"),
            localized_arrival_time=transit_details.get("localized_arrival_time"),
            headway_minutes=transit_details.get("headway_minutes"),
            trip_short_text=transit_details.get("trip_short_text"),
            transit_agency_names=transit_details.get("transit_agency_names", []),
            transit_line_uri=transit_details.get("transit_line_uri"),
            transit_line_color=transit_details.get("transit_line_color"),
            transit_line_text_color=transit_details.get("transit_line_text_color"),
            transit_fare=fare_amount,
            transit_fare_currency=fare_currency,
            walk_to_station_minutes=walk_to_station_minutes,
            walk_from_station_minutes=walk_from_station_minutes,
            step_instructions=step_instructions,
        )

    def _waypoint(self, place: CandidatePlace) -> dict[str, object]:
        return {
            "location": {
                "latLng": {
                    "latitude": place.location.lat,
                    "longitude": place.location.lng,
                }
            }
        }

    def _route_mode(self, mode: TransportMode) -> str:
        mapping = {
            TransportMode.WALK: "WALK",
            TransportMode.TRANSIT: "TRANSIT",
            TransportMode.DRIVE: "DRIVE",
            TransportMode.BICYCLE: "BICYCLE",
        }
        return mapping[mode]

    def _duration_to_seconds(self, raw_duration: str) -> int:
        cleaned = raw_duration.removesuffix("s")
        try:
            return int(float(cleaned))
        except ValueError:
            return 0

    def _to_rfc3339(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.isoformat().replace("+00:00", "Z")

    def _heuristic_route(
        self,
        origin: CandidatePlace,
        destination: CandidatePlace,
        mode: TransportMode,
    ) -> TravelStep:
        distance_meters = self._haversine_distance(origin.location, destination.location)
        speeds_kmh = {
            TransportMode.WALK: 4.5,
            TransportMode.TRANSIT: 20.0,
            TransportMode.DRIVE: 28.0,
            TransportMode.BICYCLE: 14.0,
        }
        speed = speeds_kmh[mode]
        duration_minutes = max(1, round((distance_meters / 1000) / speed * 60))
        instructions: list[str] = []
        if mode == TransportMode.TRANSIT:
            instructions.append(
                "Transit details unavailable; use a local transit app for exact line/station guidance."
            )
        return TravelStep(
            mode=mode,
            duration_minutes=duration_minutes,
            distance_meters=round(distance_meters),
            cost_estimate=self._estimate_cost(mode=mode, distance_meters=round(distance_meters)),
            note="Estimated locally because Google routing was unavailable.",
            step_instructions=instructions,
        )

    def _estimate_cost(
        self,
        *,
        mode: TransportMode,
        distance_meters: int | float | None,
    ) -> float | None:
        if distance_meters is None:
            return None

        distance_km = distance_meters / 1000
        if mode == TransportMode.DRIVE:
            return round(max(2.5, distance_km * 0.22), 2)
        if mode == TransportMode.TRANSIT:
            return round(max(2.0, 1.5 + distance_km * 0.08), 2)
        if mode in {TransportMode.WALK, TransportMode.BICYCLE}:
            return 0.0
        return None

    def _haversine_distance(self, a: PlaceLocation, b: PlaceLocation) -> float:
        radius = 6_371_000
        lat1 = math.radians(a.lat)
        lat2 = math.radians(b.lat)
        delta_lat = math.radians(b.lat - a.lat)
        delta_lng = math.radians(b.lng - a.lng)

        haversine = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2) ** 2
        )
        return 2 * radius * math.asin(math.sqrt(haversine))

    def _extract_transit_details(self, route: dict[str, object]) -> dict[str, object]:
        legs = route.get("legs") or []
        for leg in legs:
            steps = leg.get("steps") or []
            for step in steps:
                transit_details = step.get("transitDetails") or step.get("transit_details") or {}
                if not transit_details:
                    continue

                stop_details = transit_details.get("stopDetails") or {}
                localized_values = transit_details.get("localizedValues") or {}
                departure_stop = (
                    (stop_details.get("departureStop") or {}).get("name")
                    or (transit_details.get("departureStop") or {}).get("name")
                )
                arrival_stop = (
                    (stop_details.get("arrivalStop") or {}).get("name")
                    or (transit_details.get("arrivalStop") or {}).get("name")
                )
                transit_line = self._extract_transit_line_name(transit_details)
                line = transit_details.get("transitLine") or transit_details.get("transit_line") or {}
                agencies = line.get("agencies") or []
                return {
                    "departure_stop": departure_stop,
                    "arrival_stop": arrival_stop,
                    "transit_line": transit_line,
                    "transit_headsign": transit_details.get("headsign"),
                    "transit_stop_count": transit_details.get("stopCount"),
                    "vehicle_type": self._extract_vehicle_type(transit_details),
                    "departure_time": stop_details.get("departureTime")
                    or transit_details.get("departureTime"),
                    "arrival_time": stop_details.get("arrivalTime")
                    or transit_details.get("arrivalTime"),
                    "localized_departure_time": (
                        ((localized_values.get("departureTime") or {}).get("time") or {}).get("text")
                    ),
                    "localized_arrival_time": (
                        ((localized_values.get("arrivalTime") or {}).get("time") or {}).get("text")
                    ),
                    "headway_minutes": self._duration_to_minutes(transit_details.get("headway")),
                    "trip_short_text": transit_details.get("tripShortText")
                    or transit_details.get("trip_short_text"),
                    "transit_agency_names": [
                        agency.get("name")
                        for agency in agencies
                        if isinstance(agency, dict) and agency.get("name")
                    ],
                    "transit_line_uri": line.get("uri"),
                    "transit_line_color": line.get("color"),
                    "transit_line_text_color": line.get("textColor") or line.get("text_color"),
                }

        return {
            "departure_stop": None,
            "arrival_stop": None,
            "transit_line": None,
            "transit_headsign": None,
            "transit_stop_count": None,
            "vehicle_type": None,
            "departure_time": None,
            "arrival_time": None,
            "localized_departure_time": None,
            "localized_arrival_time": None,
            "headway_minutes": None,
            "trip_short_text": None,
            "transit_agency_names": [],
            "transit_line_uri": None,
            "transit_line_color": None,
            "transit_line_text_color": None,
        }

    def _extract_transit_fare(
        self,
        advisory: dict[str, object],
    ) -> tuple[float | None, str | None]:
        transit_fare = advisory.get("transitFare") or {}
        if not isinstance(transit_fare, dict):
            return (None, None)
        currency = transit_fare.get("currencyCode")
        amount = self._money_to_float(transit_fare)
        return (amount, currency if isinstance(currency, str) else None)

    def _money_to_float(self, money: dict[str, object]) -> float | None:
        units_raw = money.get("units")
        nanos_raw = money.get("nanos", 0)
        try:
            units = int(units_raw) if units_raw is not None else 0
            nanos = int(nanos_raw)
        except (TypeError, ValueError):
            return None
        return round(units + nanos / 1_000_000_000, 2)

    def _extract_transit_line_name(self, transit_details: dict[str, object]) -> str | None:
        line = transit_details.get("transitLine") or transit_details.get("transit_line") or {}
        name_short = line.get("nameShort") or line.get("name_short")
        name = line.get("name")
        return name_short or name

    def _extract_vehicle_type(self, transit_details: dict[str, object]) -> str | None:
        line = transit_details.get("transitLine") or transit_details.get("transit_line") or {}
        vehicle = line.get("vehicle") or {}
        vehicle_type = vehicle.get("type")
        if not vehicle_type:
            return None
        return str(vehicle_type)

    def _extract_station_walk_minutes(self, route: dict[str, object]) -> tuple[int | None, int | None]:
        legs = route.get("legs") or []
        if not legs:
            return (None, None)
        steps = legs[0].get("steps") or []
        if not steps:
            return (None, None)

        first_transit_index = None
        last_transit_index = None
        for index, step in enumerate(steps):
            mode = str(step.get("travelMode") or "").upper()
            has_transit = bool(step.get("transitDetails") or step.get("transit_details"))
            if mode == "TRANSIT" or has_transit:
                if first_transit_index is None:
                    first_transit_index = index
                last_transit_index = index

        if first_transit_index is None:
            return (None, None)

        walk_before = 0
        for step in steps[:first_transit_index]:
            if str(step.get("travelMode") or "").upper() == "WALK":
                walk_minutes = self._duration_to_minutes(
                    step.get("staticDuration") or step.get("duration")
                )
                if walk_minutes is not None:
                    walk_before += walk_minutes

        walk_after = 0
        if last_transit_index is not None:
            for step in steps[last_transit_index + 1 :]:
                if str(step.get("travelMode") or "").upper() == "WALK":
                    walk_minutes = self._duration_to_minutes(
                        step.get("staticDuration") or step.get("duration")
                    )
                    if walk_minutes is not None:
                        walk_after += walk_minutes

        return (
            walk_before if walk_before > 0 else None,
            walk_after if walk_after > 0 else None,
        )

    def _extract_step_instructions(
        self,
        route: dict[str, object],
        mode: TransportMode,
    ) -> list[str]:
        legs = route.get("legs") or []
        instructions: list[str] = []
        for leg in legs:
            steps = leg.get("steps") or []
            for step in steps:
                instruction = (step.get("navigationInstruction") or {}).get("instructions")
                transit_details = step.get("transitDetails") or step.get("transit_details") or {}
                travel_mode = str(step.get("travelMode") or "").upper()
                if transit_details:
                    formatted = self._format_transit_instruction(transit_details)
                    if formatted:
                        instructions.append(formatted)
                        continue
                if instruction:
                    normalized = self._normalize_instruction(instruction)
                    if normalized:
                        instructions.append(normalized)
                        continue
                if travel_mode == "WALK":
                    minutes = self._duration_to_minutes(step.get("staticDuration") or step.get("duration"))
                    if minutes is not None:
                        instructions.append(f"Walk for about {minutes} minute(s).")
                elif travel_mode == "DRIVE" and mode == TransportMode.DRIVE:
                    minutes = self._duration_to_minutes(step.get("staticDuration") or step.get("duration"))
                    if minutes is not None:
                        instructions.append(f"Drive for about {minutes} minute(s).")
        deduped: list[str] = []
        for instruction in instructions:
            if instruction not in deduped:
                deduped.append(instruction)
        return deduped

    def _format_transit_instruction(self, transit_details: dict[str, object]) -> str | None:
        stop_details = transit_details.get("stopDetails") or {}
        departure_stop = (
            (stop_details.get("departureStop") or {}).get("name")
            or (transit_details.get("departureStop") or {}).get("name")
        )
        arrival_stop = (
            (stop_details.get("arrivalStop") or {}).get("name")
            or (transit_details.get("arrivalStop") or {}).get("name")
        )
        line = self._extract_transit_line_name(transit_details)
        headsign = transit_details.get("headsign")
        stop_count = transit_details.get("stopCount")

        line_part = line or "the transit line"
        departure_part = departure_stop or "the departure stop"
        arrival_part = arrival_stop or "the arrival stop"

        text = f"Take {line_part} from {departure_part} to {arrival_part}"
        if headsign:
            text += f" toward {headsign}"
        if stop_count is not None:
            text += f" ({stop_count} stops)"
        return text + "."

    def _normalize_instruction(self, instruction: str) -> str | None:
        cleaned = re.sub(r"\s+", " ", instruction).strip()
        if not cleaned:
            return None
        if not cleaned.endswith("."):
            cleaned += "."
        return cleaned

    def _duration_to_minutes(self, raw_duration: object) -> int | None:
        if raw_duration is None:
            return None
        seconds = self._duration_to_seconds(str(raw_duration))
        if seconds <= 0:
            return None
        return max(1, round(seconds / 60))
