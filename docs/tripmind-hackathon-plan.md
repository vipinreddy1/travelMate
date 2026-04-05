# TripMind Roadmap And Current Status

## What This Document Is

This file is a roadmap and product vision document, not a statement of everything already implemented.

The current shipped app is smaller in scope than the original hackathon plan:

- The frontend is a Next.js 3-panel app.
- The backend is a FastAPI planner service.
- The core flow is backend-driven itinerary planning through `/api/v1/planner/plan`.
- Travel DNA on the left updates from backend `planning_state`.
- The itinerary card in the center renders from the real backend response.
- Auth0 user metadata is used to persist frontend preference state.

## What Is Implemented Today

### Main App (`/`)

- Left panel shows reusable Travel DNA preferences.
- Center panel sends user messages to the FastAPI planner.
- Backend follow-up questions appear in chat and can surface quick replies above the input.
- Successful planner responses render an itinerary card inline.
- The browser talks to a same-origin Next.js route, which proxies planner calls to the backend.

### Supporting Pages

- `/blog/[id]` renders local editorial blog fixtures from `frontend/data/blogs`.
- `/trip/[id]` still uses a mock editorial trip page.

### Backend

- FastAPI route: `/api/v1/planner/plan`
- Sequential planning workflow with completeness and feasibility checks
- Google/Gemini-backed planner services where configured
- In-memory planner response cache with a delayed replay for cached hits

## What Is Still Fixture Or Mock Backed

- Right-panel trip memories are seeded in the frontend store.
- `/trip/[id]` uses a hardcoded mock blog post.
- `/blog/[id]` uses local JSON fixture content rather than backend persistence.
- Initial Travel DNA defaults are still seeded locally until real metadata or planner output replaces them.

## Not Implemented From The Original Vision

These ideas remain roadmap items unless called out elsewhere as shipped:

- Multi-node LangGraph orchestration
- Voice input/output production flow
- Real trip history backend persistence
- Automatic blog generation from completed trips
- Proactive in-trip replanning
- Flight shopping integration
- Maps visualization in the itinerary UI
- SSE preference streaming

## Recommended Reading

For the current implementation, prefer:

- `backend/architecture.md`
- `frontend/README.md`
- `frontend/docs/ARCHITECTURE.md`
- `frontend/docs/API_INTEGRATION.md`

## Roadmap Direction

The product direction is still consistent with the original vision:

1. Make the current planner loop robust.
2. Persist real trip memories and generated trips.
3. Replace static blog and trip fixtures with backend data.
4. Add richer follow-up interactions and voice only after the core planning flow is stable.
