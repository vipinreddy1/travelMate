# travelMate

travelMate is a full-stack travel planning app with a chat-first frontend and an AI-assisted planning backend.

The frontend is a Next.js app that authenticates users with Auth0, collects travel requests in a conversational UI, supports microphone input, and renders itinerary cards, preference signals, and trip memory content. The backend is a FastAPI service that turns free-form prompts into structured travel plans using Gemini for planning-state extraction and explanation generation, Google Places for destination discovery, Google Routes for travel-time estimation, and ElevenLabs for realtime speech-to-text relaying.

## What The Code Does

### Frontend

The frontend lives in [`frontend`](./frontend) and is built with Next.js App Router, TypeScript, Tailwind CSS, and Zustand.

- `app/page.tsx` renders a 3-panel authenticated workspace:
  - left panel: "Travel DNA" preferences inferred from planner output
  - center panel: chat interface, starter prompts, microphone input, and inline itinerary cards
  - right panel: seeded trip memories and links to local blog-style trip content
- `app/api/planner/plan/route.ts` acts as a same-origin proxy from Next.js to the FastAPI backend.
- `components/CenterPanel.tsx` drives the planner conversation:
  - sends free-form prompts to the backend
  - infers a transport preference from the user message
  - displays follow-up questions and quick replies
  - maps backend responses into a visual itinerary card
  - opens Google Calendar links for itinerary events
  - streams microphone audio to the backend STT websocket
- `components/LeftPanel.tsx` shows reusable preference signals such as budget, pace, group type, dietary hints, and travel style.
- `components/RightPanel.tsx` shows mock "trip memory" cards for the user and friends.
- `app/api/user-metadata/route.ts` reads and updates Auth0 user metadata so preferences can be synced per user.
- `lib/plannerApi.ts` converts backend responses into frontend-friendly chat text, itinerary data, preference chips, and a fallback presentation mode if the planner is unavailable.

Not everything is live-backed yet. The trip memory feed, blog pages, and some presentation fallback data are still local fixtures.

### Backend

The backend lives in [`backend`](./backend) and is built with FastAPI and Pydantic.

- `app/main.py` boots the API, configures CORS, and registers the route modules.
- `app/api/routes/planner.py` exposes:
  - `POST /api/v1/planner/plan`
  - `POST /api/v1/planner/test-simple-gemini`
- `app/api/routes/stt.py` exposes `WS /api/v1/stt/stream`, which relays browser audio chunks to ElevenLabs realtime speech-to-text and streams transcript events back.
- `app/workflows/planner_graph.py` contains the main planning workflow.
- `app/services/planner.py` wires together the Gemini, Places, Routes, optimizer, completeness, feasibility, and memory layers.
- `app/services/memory.py` stores recent conversation turns and cached planner responses in process memory.
- `app/services/optimizer.py` shortlists places, builds day plans, and estimates budget.
- `app/models/planning.py` defines the backend request/response contract shared with the frontend.

### Planner Flow

For `POST /api/v1/planner/plan`, the code currently does this:

1. Accepts a natural-language travel prompt plus optional locale, currency, transport preference, and session ID.
2. Adds the user turn to in-memory session history.
3. Uses Gemini to extract a structured planning state from the prompt and recent context.
4. Runs a completeness check.
5. If details are missing, returns a follow-up question instead of calling Places/Routes.
6. After repeated incomplete attempts, falls back to an approximate itinerary response.
7. If the request is complete, runs a feasibility check.
8. If feasible, generates search queries, fetches candidate places, computes route options, builds an itinerary, estimates budget, and asks Gemini for a final explanation.
9. Stores assistant output back into session memory and returns the structured trip plan.

The workflow is sequential and the memory/cache layer is ephemeral, so session history resets when the backend restarts.

## Repo Layout

```text
travelMate/
|- frontend/   Next.js app
|- backend/    FastAPI planner API
|- docs/       Product and planning notes
|- vercel.json Vercel multi-service config
```

## Local Development

### Prerequisites

- Node.js 18+
- npm
- Python 3.11+

### 1. Start the backend

Create `backend/.env` from `backend/.env.example` and fill in the required keys.

Minimum useful backend variables:

- `GEMINI_API_KEY`
- `MAPS_API_KEY`
- `ELEVENLABS_API_KEY` if you want microphone transcription
- `CORS_ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000`

Then run:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Backend default URL: `http://localhost:8000`

### 2. Start the frontend

Create `frontend/.env.local`.

Variables used by the frontend code:

- `NEXT_PUBLIC_API_URL=http://localhost:8000`
- `PLANNER_API_URL=http://localhost:8000` optional server-side override for the proxy route
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=...` for the map script loaded in `app/layout.tsx`
- Auth0 variables required by `@auth0/nextjs-auth0`
- `AUTH0_DOMAIN`
- `AUTH0_CLIENT_ID`
- `AUTH0_CLIENT_SECRET`
- `APP_BASE_URL=http://localhost:3000`
- `AUTH0_SECRET`
- `AUTH0_MANAGEMENT_CLIENT_ID` and `AUTH0_MANAGEMENT_CLIENT_SECRET` if you want metadata sync through the management API

Then run:

```powershell
cd frontend
npm install
npm run dev
```

Frontend default URL: `http://localhost:3000`

## Frontend To Backend Contract

The frontend posts planner requests to `/api/planner/plan`, and the Next.js route forwards them to the backend `POST /api/v1/planner/plan` endpoint.

The frontend especially depends on these backend response fields:

- `planning_state` to update Travel DNA
- `follow_up_question` and `missing_information` to continue the chat
- `itinerary` to render the itinerary card
- `budget` and `warnings` to enrich the planner response
- `metadata.itinerary_generated_at` to build dated itinerary events

If the backend request fails, the frontend falls back to a built-in presentation-safe mock planner for a few destinations like Las Vegas and Tokyo.

## Deployment Notes

`vercel.json` is configured with experimental multi-service routing:

- `frontend` is mounted at `/`
- `backend` is mounted at `/_/backend`

The frontend proxy route can be pointed at any reachable planner backend through `PLANNER_API_URL` or `NEXT_PUBLIC_API_URL`.

## Useful Entry Points

- [`frontend/app/page.tsx`](./frontend/app/page.tsx)
- [`frontend/components/CenterPanel.tsx`](./frontend/components/CenterPanel.tsx)
- [`frontend/lib/plannerApi.ts`](./frontend/lib/plannerApi.ts)
- [`backend/app/main.py`](./backend/app/main.py)
- [`backend/app/api/routes/planner.py`](./backend/app/api/routes/planner.py)
- [`backend/app/api/routes/stt.py`](./backend/app/api/routes/stt.py)
- [`backend/app/workflows/planner_graph.py`](./backend/app/workflows/planner_graph.py)

## Testing

Backend tests live in `backend/tests` and cover pieces of normalization, feasibility, memory, and optimization logic.

```powershell
cd backend
pytest
```

The frontend repository includes documentation and implementation files, but no dedicated frontend test suite is wired up in the current root flow.
