# TripMind Frontend - Components Guide

## Core Components

### `LeftPanel.tsx`

Purpose:

- renders Travel DNA
- shows preference update feedback
- keeps the left rail focused on reusable user preferences

Notes:

- Travel DNA items are no longer limited to the original hardcoded six keys
- the panel includes icon fallbacks for preference types such as stay or accommodation

### `CenterPanel.tsx`

Purpose:

- drives the main planner conversation
- sends requests to the backend through the frontend proxy route
- renders chat messages, follow-up options, and the inline itinerary card

Current behavior:

- no old guided mock flow
- no duplicate wall-of-text itinerary summary when the itinerary card is visible
- respects manual user scroll while messages are generating
- shows backend follow-up questions in chat
- uses the choice panel above the input for quick replies inferred from backend follow-up context

### `RightPanel.tsx`

Purpose:

- renders trip memories under `My Trips` and `Friends`

Current data source:

- local fixture-backed memories from the Zustand store

### `ItineraryCard.tsx`

Purpose:

- renders the frontend itinerary model derived from the backend planner response

Current behavior:

- supports incomplete hotel and flight details gracefully
- renders a visual trip plan without requiring the same information to also appear as a large chat message

### `Auth0MetadataSync.tsx`

Purpose:

- keeps frontend preferences in sync with Auth0 user metadata

Behavior:

- reads metadata on load
- hydrates store preferences
- debounces writes back to Auth0 after updates

### `BlogPostContent.tsx`

Purpose:

- renders `/blog/[id]` from local blog fixture content

### `BlogPostPage.tsx`

Purpose:

- powers `/trip/[id]`

Current status:

- still mock-backed and not part of the live planner integration

## Utility Modules

### `lib/plannerApi.ts`

This file is central to the planner UI. It handles:

- planner request construction
- backend response typing
- itinerary mapping
- Travel DNA mapping from `planning_state`
- chat formatting
- quick-reply derivation for follow-up questions

### `store/appStore.ts`

Zustand store for:

- workspaces
- messages
- itinerary
- preferences
- trip memories

## Component Map By Surface

### Main App

- `LeftPanel.tsx`
- `CenterPanel.tsx`
- `RightPanel.tsx`
- `ItineraryCard.tsx`

### Blog And Trip Reading

- `BlogPostContent.tsx`
- `BlogPostPage.tsx`

### Auth And Sync

- `AuthScreen.tsx`
- `Auth0MetadataSync.tsx`

## Fixture Areas To Keep In Mind

The following components still surface fixture-backed content:

- `RightPanel.tsx`
- `BlogPostContent.tsx`
- `BlogPostPage.tsx`
