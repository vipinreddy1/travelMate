# TravelMate Backend Architecture

This document describes the current backend behavior in code today, including:

- where LLM calls are made
- where Maps/Routes calls are made
- where data is transformed
- where exceptions and fallbacks are handled

---

## 1. Runtime Topology

FastAPI app bootstraps in [`app/main.py`](./app/main.py).

Shared state initialized in `lifespan()`:

- `settings` from [`app/core/config.py`](./app/core/config.py)
- one shared `httpx.AsyncClient`
- in-memory session store [`app/services/memory.py`](./app/services/memory.py)

Registered routers:

- [`app/api/routes/health.py`](./app/api/routes/health.py)
- [`app/api/routes/planner.py`](./app/api/routes/planner.py)
- [`app/api/routes/routes_direct.py`](./app/api/routes/routes_direct.py)

---

## 2. API Surface

### `GET /api/v1/health`

File: [`app/api/routes/health.py`](./app/api/routes/health.py)

Returns readiness and config signals:

- `gemini_api_key_configured`
- `maps_api_key_configured`
- `google_calls_enabled`
- `gemini_model`

---

### `POST /api/v1/planner/test-simple-gemini`

File: [`app/api/routes/planner.py`](./app/api/routes/planner.py)

Purpose:

- parse prompt into `PlanningState` only
- no completeness/feasibility/tool execution

Legacy alias still exists (hidden): `POST /api/v1/planner/planning-state`

---

### `POST /api/v1/planner/plan`

File: [`app/api/routes/planner.py`](./app/api/routes/planner.py)

Purpose:

- full gated workflow:
  - planning-state extraction
  - completeness
  - feasibility
  - conditional Places/Routes/itinerary execution
  - final response synthesis

Response contract: `TripPlanResponse`

---

### `POST /api/v1/planner/test-transit-route`

File: [`app/api/routes/planner.py`](./app/api/routes/planner.py)

Purpose:

- debug-oriented transit route endpoint using service wrappers
- resolves `origin_query` and `destination_query` with Places
- computes one route with Routes client and parsed transit details

Validation:

- `departure_time` and `arrival_time` cannot both be set

---

### `POST /api/v1/routes-direct/compute`

File: [`app/api/routes/routes_direct.py`](./app/api/routes/routes_direct.py)

Purpose:

- direct passthrough to Google Routes `directions/v2:computeRoutes`
- bypasses planner, Gemini, optimizer, and memory
- returns raw Google response JSON

Input:

- request body is forwarded as-is to Google Routes
- optional query `fieldMask` maps to `X-Goog-FieldMask`

This endpoint is intended for low-level API debugging and validation.

---

## 3. `/plan` Happy Path Call Order

For a complete and feasible request:

1. Client calls `POST /api/v1/planner/plan`
2. Backend appends user turn to memory
3. Backend calls Gemini `generateContent` to extract planning state
4. Backend evaluates completeness (rule-based)
5. Backend evaluates feasibility (rule-based)
6. Backend calls Gemini `generateContent` to produce execution plan
7. Backend conditionally calls:
   - Places `places:searchText` (if `search_places` action)
   - Routes `directions/v2:computeRoutes` (if `compute_routes` action)
8. Backend builds shortlist, route map, itinerary, budget
9. Backend calls Gemini `generateContent` for final user-facing explanation (or direct answer fallback path)
10. Backend appends assistant turn to memory and returns `TripPlanResponse`

Early exits:

- incomplete request returns follow-up prompt (or approximate itinerary after threshold)
- not feasible request returns feasibility message without itinerary

---

## 4. Workflow Internals (`PlannerWorkflow`)

File: [`app/workflows/planner_graph.py`](./app/workflows/planner_graph.py)

Main stages:

- `_load_memory`
  - append latest user message
- `_extract_planning_state` (LLM call)
  - merge context + latest prompt
  - normalize transport preference/modes
- `_evaluate_completeness` (rule-based)
  - track incomplete attempts per session
- `_evaluate_feasibility` (rule-based)
- `_build_plan`
  - execution plan (LLM call)
  - action loop (`direct_answer`, `search_places`, `compute_routes`, `build_itinerary`)
  - candidate dedupe + shortlist
  - route computation for selected modes
  - route selection based on transport preference
  - itinerary + budget generation
  - explanation generation (LLM call) or direct-answer path
- `_finalize_response`
  - unify response shape for all branches
  - write assistant turn
  - include recent context and metadata

---

## 5. LLM Calls and Responsibilities

File: [`app/clients/gemini.py`](./app/clients/gemini.py)

### `extract_planning_state(...)`

- Gemini `generateContent` call
- outputs structured planning JSON
- local normalization before Pydantic validation:
  - constraint strength aliases
  - soft-preference weight aliases
  - transport preference aliases

Fallback if Gemini disabled/missing key:

- `_heuristic_planning_state`

### `plan_execution(...)`

- Gemini `generateContent` call
- outputs tool selection plan:
  - `direct_answer_only`
  - `use_places`
  - `use_routes`
  - `build_itinerary`
  - `action_order`
  - `search_focus`
  - `route_request` transit options

Normalization includes:

- action filtering
- `route_request` sanitization:
  - RFC3339 timestamp checks
  - transit mode enum normalization (`BUS`, `SUBWAY`, `TRAIN`, `LIGHT_RAIL`, `RAIL`)
  - transit routing preference normalization (`LESS_WALKING`, `FEWER_TRANSFERS`)
  - conflict resolution when both departure/arrival times are set

Fallback if Gemini disabled/missing key:

- `_heuristic_execution_plan`

### `explain_itinerary(...)`

- Gemini `generateContent` call
- final natural-language rendering from structured data
- prompt instructs model to prioritize route/step details and avoid hallucination

### `answer_without_tools(...)`

- Gemini `generateContent` call for direct answer path

### `approximate_itinerary_from_incomplete(...)`

- Gemini `generateContent` call used only after repeated incomplete attempts

---

## 6. Maps and Routes Processing

File: [`app/clients/maps.py`](./app/clients/maps.py)

### Places client

- `PlacesClient.search_text(...)`
- calls `POST {places_base_url}/places:searchText`
- maps response into `CandidatePlace` models

### Routes client

- `RoutesClient.compute_route(...)`
- calls `POST {routes_base_url}/directions/v2:computeRoutes`
- supports `WALK`, `TRANSIT`, `DRIVE`, `BICYCLE`
- supports transit request controls:
  - `departureTime`
  - `arrivalTime`
  - `computeAlternativeRoutes`
  - `transitPreferences.allowedTravelModes`
  - `transitPreferences.routingPreference`

Extracted transit details include:

- station names, line, headsign, stop count
- step instructions
- walk-to/from-station minutes
- departure/arrival times and localized display times
- headway and trip short text
- line metadata (agency names, URI, line colors)
- transit fare and currency when available

Fallback behavior:

- if Google calls disabled/missing API key, or no routes returned, use heuristic route estimate
- heuristic route includes explicit note:
  - `"Estimated locally because Google routing was unavailable."`

---

## 7. Data Processing Ownership

- API schemas: [`app/models/planning.py`](./app/models/planning.py)
- Orchestration: [`app/workflows/planner_graph.py`](./app/workflows/planner_graph.py)
- Planner façade: [`app/services/planner.py`](./app/services/planner.py)
- Completeness rules: [`app/services/completeness.py`](./app/services/completeness.py)
- Feasibility rules: [`app/services/feasibility.py`](./app/services/feasibility.py)
- Query generation: [`app/services/query_builder.py`](./app/services/query_builder.py)
- Ranking/itinerary/budget: [`app/services/optimizer.py`](./app/services/optimizer.py)
- Session memory: [`app/services/memory.py`](./app/services/memory.py)
- Google API transport/errors: [`app/clients/base.py`](./app/clients/base.py)

---

## 8. Exception and Fallback Handling

### Client/base layer

File: [`app/clients/base.py`](./app/clients/base.py)

- network errors -> `GoogleAPIError`
- non-2xx Google responses -> `GoogleAPIError`
- missing keys via `require_gemini_api_key()` / `require_maps_api_key()` -> `GoogleAPIError`

### Planner routes

File: [`app/api/routes/planner.py`](./app/api/routes/planner.py)

- `GoogleAPIError` -> HTTP 502
- `ValueError` -> HTTP 400 (for `/plan` and `/test-transit-route`)

### Direct routes endpoint

File: [`app/api/routes/routes_direct.py`](./app/api/routes/routes_direct.py)

- `GoogleAPIError` -> HTTP 502
- raw payload is passed through (schema-free for flexibility)

### Non-exception fallbacks

- Gemini disabled or key missing:
  - heuristic planning/execution/explanation paths
- Maps disabled or key missing:
  - heuristic route estimates

---

## 9. Session Memory Model

File: [`app/services/memory.py`](./app/services/memory.py)

Current implementation:

- in-process dictionary storage only
- keyed by `session_id`
- stores user/assistant turns and last planning state
- resets on process restart

Used for:

- context injection into planning-state extraction
- turn-count and recent context in responses
- incomplete-attempt tracking

---

## 10. Transport Strategy

Transport preference from request maps to evaluated modes:

- `own_transport` -> `drive`
- `public_transport` -> `transit`
- `hybrid` -> `drive + transit` (hybrid score)
- `optimize_for_time` -> `drive + transit` (min duration)
- `optimize_for_money` -> `transit + drive` (min cost)

Leg-level route selection is performed in workflow route-map selection.

---

## 11. Current Limitation to Be Aware Of

`GeminiClient.plan_execution(...)` now returns a normalized `route_request` object with transit-specific options, but the current `PlannerWorkflow._build_plan(...)` does not yet pass that `route_request` into its internal `compute_route(...)` calls.

Impact:

- planner endpoint uses default internal route-compute settings
- transit preference tuning from execution-plan output is fully available today in:
  - `POST /api/v1/planner/test-transit-route`
  - `POST /api/v1/routes-direct/compute`

---

## 12. Practical Summary

There are now two clear operating modes:

- planner mode (`/api/v1/planner/plan`): conversational, gated, optimized, memory-aware
- direct mode (`/api/v1/routes-direct/compute`): raw Google Routes debugging, no orchestration

All Google transport failures are normalized through `GoogleAPIError`, and route fallback behavior is explicit in the returned route notes.
