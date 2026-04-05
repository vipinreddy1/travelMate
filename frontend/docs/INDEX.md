# TripMind Frontend Documentation Index

These docs describe the current frontend as it exists today. A few UI areas still use fixture data on purpose, but the planner flow itself is backend-driven.

## Read First

### [ARCHITECTURE.md](ARCHITECTURE.md)

Use this for the current app structure, routes, and data flow.

### [API_INTEGRATION.md](API_INTEGRATION.md)

Use this for the live frontend/backend contract, proxy route, Auth0 metadata sync, and remaining fixture-backed areas.

### [STATE_MANAGEMENT.md](STATE_MANAGEMENT.md)

Use this for the current multi-workspace Zustand store, Travel DNA state, messages, itinerary placement, and trip memories.

### [COMPONENTS.md](COMPONENTS.md)

Use this for the components that power the current UI.

## Additional References

### [STYLING_GUIDE.md](STYLING_GUIDE.md)

Design tokens, Tailwind usage, and styling conventions.

### [FILE_STRUCTURE.md](FILE_STRUCTURE.md)

Directory layout and codebase navigation.

### [SETUP_AND_BUILD.md](SETUP_AND_BUILD.md)

Environment setup and production build notes.

### [DEVELOPMENT.md](DEVELOPMENT.md)

General engineering notes. Parts of this file may still describe older planned work, so prefer `ARCHITECTURE.md` and `API_INTEGRATION.md` first.

### [ERROR_RESOLUTION.md](ERROR_RESOLUTION.md)

Known troubleshooting notes.

## Current Reality In One Page

- Planner requests go through `app/api/planner/plan/route.ts`.
- The FastAPI backend is the source of truth for itineraries and Travel DNA updates.
- Travel DNA is derived from backend `planning_state`.
- Auth0 metadata sync persists frontend preferences.
- The right panel and some blog/trip pages still use local fixture content.
