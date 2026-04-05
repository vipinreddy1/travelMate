# TripMind Frontend - Architecture

## High-Level View

TripMind is a Next.js App Router frontend with a fixed 3-panel layout:

- left: Travel DNA
- center: planner chat and itinerary
- right: trip memory

The current architecture is backend-driven for the planning experience. The old guided mock chat flow is no longer part of the main product path.

## Main Routes

### `/`

Primary planner experience.

Key panels:

- `LeftPanel.tsx`: reusable Travel DNA preferences
- `CenterPanel.tsx`: planner chat, quick replies, itinerary rendering
- `RightPanel.tsx`: trip memory browser

### `/blog/[id]`

Renders local editorial blog fixtures using `BlogPostContent.tsx` and `lib/blogData.ts`.

### `/trip/[id]`

Authenticated route that still renders the older mock `BlogPostPage.tsx`.

## Request And Render Flow

1. User types a prompt in `CenterPanel.tsx`.
2. The frontend enriches the prompt with the current Travel DNA summary.
3. `lib/plannerApi.ts` sends the request to `/api/planner/plan`.
4. `app/api/planner/plan/route.ts` forwards the request to FastAPI.
5. The frontend receives a planner response.
6. The response is mapped into:
   - chat content
   - inline itinerary card
   - Travel DNA updates from `planning_state`
   - quick replies for clarification when needed

## State Model

The frontend uses a multi-workspace Zustand store keyed by user ID.

Each workspace holds:

- `preferences`
- `messages`
- `itinerary`
- `isRecording`
- `flowStep`
- `itineraryInlineAfterMessageId`
- `tripMemories`

The store is documented in more detail in `STATE_MANAGEMENT.md`.

## Travel DNA

Travel DNA now reflects reusable user preferences rather than trip-local facts.

It is built from backend `planning_state` and persisted through Auth0 metadata sync.

Examples of values that belong in Travel DNA:

- budget style
- transport preference
- travel group
- pace
- vibe
- dietary preference
- stay style

Examples that do not belong there:

- a specific destination
- exact trip dates
- stop count for one itinerary
- one-off missing fields

## Itinerary Rendering

The itinerary card is driven by the backend planner response.

When an itinerary card is shown:

- the chat message above it is intentionally brief
- the frontend avoids repeating the full itinerary in text form

The UI also tolerates backend responses that do not yet contain full hotel or flight booking data.

## Follow-Up Questions

When the backend cannot fully plan the trip:

- `follow_up_question` is shown in chat
- the choice panel above the input can render quick replies inferred from backend context

This keeps the clarification flow structured without requiring the backend to send explicit choice arrays.

## Remaining Fixture Areas

The planner is real, but some support surfaces still use fixtures:

- right-panel trip memories
- local blog content
- `/trip/[id]` mock editorial page

## Auth0 Integration

Auth0 is used for:

- app authentication
- user metadata persistence for preferences

The frontend sync layer loads metadata on startup and writes changes back after preference updates.
