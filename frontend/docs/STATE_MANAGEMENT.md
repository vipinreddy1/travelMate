# TripMind Frontend - State Management

## Overview

The frontend uses Zustand for client state. The store lives in `store/appStore.ts`.

The current store is workspace-based rather than a single global flat app state.

## Core Types

### Preference

```ts
interface Preference {
  key: string
  icon: string
  label: string
  value: string
  updated?: boolean
}
```

These power the Travel DNA panel.

### Message

```ts
interface Message {
  id: string
  role: 'user' | 'agent'
  content: string
  timestamp: Date
  isTyping?: boolean
  options?: string[]
  showOtherOption?: boolean
}
```

Messages can also carry quick-reply options for backend clarification flows.

### Itinerary

The itinerary type is the frontend render model used by `ItineraryCard.tsx`. It is created by mapping the backend planner response into UI-friendly fields.

### TripMemoryItem

Trip memories power the right panel. These are still fixture-backed by default.

## Workspace Shape

Each user workspace stores:

- `preferences`
- `messages`
- `itinerary`
- `isRecording`
- `flowStep`
- `itineraryInlineAfterMessageId`
- `tripMemories`

The store keeps `workspaces: Record<string, WorkspaceState>`, keyed by user ID.

## Important Actions

### `ensureWorkspace(userId)`

Creates a workspace on first access.

### `setPreferences(userId, preferences)`

Replaces the full Travel DNA list. This is used when backend `planning_state` is mapped into reusable preferences.

### `replacePreferences(userId, values)`

Hydrates existing preferences from Auth0 metadata.

### `updatePreference(userId, key, value)`

Updates an individual preference item. This is still useful for direct UI changes, but the main planner flow now prefers replacing Travel DNA from backend output.

### `addMessage(userId, message)`

Appends a chat message. Agent messages may include quick replies.

### `setTypingStatus(userId, isTyping)`

Adds or removes the typing indicator message.

### `setItinerary(userId, itinerary)`

Stores the current itinerary card render model.

### `setItineraryInlineAfterMessageId(userId, messageId)`

Controls where the itinerary card appears within the chat stream.

### `upsertTripMemory(userId, memory)`

Adds or updates a trip memory item in the right panel data set.

## Data Sources

### Backend-Driven

- itinerary
- Travel DNA from `planning_state`
- follow-up message content

### Auth0-Driven

- persisted preference values through user metadata

### Fixture-Backed

- initial Travel DNA defaults
- right-panel trip memories

## Current Store Role In The Planner Flow

1. User sends a message.
2. UI adds the user message to Zustand.
3. Frontend calls the planner API.
4. Backend response is mapped into:
   - agent message
   - itinerary
   - Travel DNA preferences
5. Zustand updates the corresponding workspace.
6. Auth0 metadata sync persists the updated preferences.

## Notes

- The store is client-side state, not the source of truth for trip planning logic.
- The backend is the source of truth for interpreting planner inputs.
- Travel DNA should remain reusable across trips, so trip-local backend fields are filtered before entering the store.
