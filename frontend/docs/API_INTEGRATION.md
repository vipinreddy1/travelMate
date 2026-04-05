# TripMind Frontend - API Integration

## Overview

The frontend is already integrated with the FastAPI backend for the main planner flow. This file documents the current contract and the remaining fixture-backed areas.

## Live Planner Request Path

The browser does not call the FastAPI backend directly.

Request path:

1. UI calls `planTrip(...)` in `lib/plannerApi.ts`
2. Frontend sends a request to `/api/planner/plan`
3. `app/api/planner/plan/route.ts` proxies the request to the FastAPI backend
4. Backend responds with `TripPlanResponse`
5. Frontend maps the response into:
   - chat output
   - itinerary card data
   - Travel DNA preferences
   - follow-up choices

This same-origin proxy avoids browser CORS issues in the main planner flow.

## Planner Endpoint

### Frontend Route

- `POST /api/planner/plan`

### Backend Route

- `POST /api/v1/planner/plan`

## Request Shape

The frontend sends the backend:

- `prompt`
- `language_code`
- `region_code`
- `currency_code`
- `transport_preference`
- `session_id`

The visible Travel DNA preferences are also summarized into the prompt before the request is sent, so the backend receives both:

- the user’s raw message
- a structured preference summary embedded in the prompt text

## Response Shape Used By Frontend

The frontend currently depends on these backend fields:

- `trip_plan` or equivalent itinerary content used for card rendering
- `planning_state`
- `follow_up_question`
- `missing_information`
- `metadata`
- `recent_context`

### `planning_state`

`planning_state` is the backend’s structured understanding of the request. The frontend uses it to build Travel DNA items such as:

- budget
- group
- transport
- pace
- vibe
- dietary
- stay

Trip-specific items like destination and one-off constraints are intentionally not persisted in Travel DNA.

### `follow_up_question`

If the backend needs clarification, the frontend:

- shows the follow-up in chat
- derives quick-reply options for the choice panel when possible

The backend does not currently send a dedicated `choices` array.

## Auth0 Metadata Sync

The frontend persists preferences through:

- `app/api/user-metadata/route.ts`
- `components/Auth0MetadataSync.tsx`
- `lib/auth0Management.ts`

Flow:

1. On load, frontend reads Auth0 user metadata.
2. Store preferences are hydrated from metadata.
3. When preferences change, the frontend debounces and writes them back to Auth0.

## Remaining Fixture-Backed Areas

These are still local and not backend-backed:

- right-panel trip memories in `store/appStore.ts`
- `/blog/[id]` local blog fixtures in `data/blogs`
- `/trip/[id]` mock blog page in `components/BlogPostPage.tsx`

## Not Currently Implemented

These are not part of the live integration today:

- direct browser calls to FastAPI from the chat UI
- SSE preference streaming
- React Query server-state layer
- ElevenLabs voice production flow
- real trip-memory backend fetches
- real blog/trip CMS APIs

## Environment

Frontend environment:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

The FastAPI backend must be running at that URL for planner requests to succeed.
