# TripMind Frontend

TripMind is a Next.js frontend for a backend-driven travel planner. The app uses a 3-panel layout:

- Left: Travel DNA
- Center: chat plus itinerary
- Right: trip memory

## Current Product Behavior

### Main Planner Flow

- User sends a message in the center panel.
- The frontend sends the request to the local Next.js route at `/api/planner/plan`.
- That route proxies the request to the FastAPI backend.
- The backend response drives:
  - the chat reply
  - the inline itinerary card
  - Travel DNA updates from `planning_state`

### Travel DNA

- Travel DNA is meant to store reusable preference signals only.
- Preferences are updated from backend `planning_state`.
- Preference changes are persisted to Auth0 user metadata through the frontend metadata route.

### Follow-Up Questions

- The backend can return `follow_up_question`.
- The frontend shows that follow-up in chat.
- The choice panel above the input can show quick replies inferred from backend follow-up context.

## Intentional Fixture Data Still In Use

- Right-panel trip memories are seeded locally in the Zustand store.
- `/blog/[id]` uses local JSON blog fixtures.
- `/trip/[id]` still renders a mock editorial blog post component.
- Initial preferences are seeded locally until replaced by Auth0 metadata or backend planner output.

## Stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- Zustand
- Auth0

## Important Files

- `app/page.tsx`: main app shell
- `app/api/planner/plan/route.ts`: same-origin planner proxy
- `app/api/user-metadata/route.ts`: Auth0 metadata API route
- `components/CenterPanel.tsx`: planner chat flow
- `components/LeftPanel.tsx`: Travel DNA UI
- `components/RightPanel.tsx`: trip memory UI
- `components/ItineraryCard.tsx`: itinerary rendering
- `lib/plannerApi.ts`: planner request/response mapping
- `store/appStore.ts`: Zustand store

## Local Development

```bash
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`.

The planner flow expects the FastAPI backend to be reachable at the URL configured by `NEXT_PUBLIC_API_URL`, usually `http://localhost:8000`.

## Build

```bash
npm run build
```

## Backend Contract

The frontend currently depends on the FastAPI planner response shape, especially:

- itinerary-like content for rendering the trip card
- `planning_state` for Travel DNA
- `follow_up_question` and `missing_information` for clarification flows

See `frontend/docs/API_INTEGRATION.md` for the current frontend/backend contract.
