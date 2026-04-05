# TripMind Frontend — Development Guide

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to see the app.

---

## Architecture Overview

### 3-Panel Layout System

The frontend uses a fixed 3-panel layout that spans the full viewport:

```
┌─────────────────┬──────────────────────────┬───────────────────┐
│  LEFT PANEL     │     CENTER PANEL         │  RIGHT PANEL      │
│   (220px)       │   (flex, remaining)      │  (280px)          │
│                 │                          │                   │
│ Preferences     │   Chat + Itinerary       │  Trip Memory      │
│ (Updates live)  │   (Main interaction)     │  (Browse past)    │
└─────────────────┴──────────────────────────┴───────────────────┘
```

All panels use `position: fixed` and `overflow-y: auto`, so the outer shell never scrolls — only inner content scrolls within each panel.

### Component Tree

```
layout.tsx (Root)
  ↓
page.tsx (Page 1)
  ├── LeftPanel (Fixed width 220px)
  │   └── Preferences list with animations
  │
  ├── CenterPanel (Flexes to fill)
  │   ├── Header with logo & user menu
  │   ├── Message list (scrollable)
  │   │   ├── User messages (right-aligned, teal pill)
  │   │   └── Agent messages (left-aligned, white card)
  │   ├── ItineraryCard (slides in after generation)
  │   └── Input area with mic + text
  │
  └── RightPanel (Fixed width 280px)
      ├── Tabs (My Trips / Friends)
      └── Trip cards (scrollable list)

trip/[id]/page.tsx (Page 2)
  └── BlogPostPage
      ├── Hero section
      ├── Sticky author + TOC
      ├── Day-by-day content with images
      └── CTA section
```

---

## Zustand Store Architecture

The `appStore` manages three main concerns:

### 1. Preferences State
```typescript
preferences: Preference[]
updatePreference(key: string, value: string): void
```

- Stores 6 preference chips (Budget, Vibe, Pace, Dietary, Stay, Group)
- Each preference has `updated` flag that triggers highlight animation
- Updates as user chats with agent

### 2. Chat Messages State
```typescript
messages: Message[]
addMessage(message: Omit<Message, 'id'>): void
setTypingStatus(isTyping: boolean): void
clearMessages(): void
```

- Tracks message history with role (user/agent)
- Typing status automatically adds/removes typing indicator message
- Messages render with auto-scroll to bottom

### 3. Itinerary State
```typescript
itinerary: Itinerary | null
setItinerary(itinerary: Itinerary): void
```

- Stores complete trip plan after agent generation
- Includes flights, hotel, and day-by-day activities
- ItineraryCard reads from store and renders

---

## Component Details

### LeftPanel
- **Purpose**: Display and reflect live preference updates
- **Key Features**: 
  - 6 preference chips with icons and values
  - Highlight animation when preference updates (`pref-update` class)
  - Footer with pulsing dot showing "Updating as you chat..."
- **Styling**: Warm off-white background, subtle shadows

### CenterPanel
- **Purpose**: Main chat and itinerary interface
- **Key Features**:
  - Message history with auto-scroll
  - User messages: right-aligned, teal pill shape
  - Agent messages: left-aligned, white card with subtle shadow
  - Typing indicators: three animated dots
  - Itinerary appears inline after agent message
  - Voice mic button glows when active
  - Input area with send button
  
### RightPanel
- **Purpose**: Browse past trips (yours and friends')
- **Key Features**:
  - Tabs to switch between "My Trips" and "Friends"
  - Trip cards with destination images
  - Friend avatars overlay on images
  - Status badge (Completed/Ongoing)
  - Hover lift animation
  - Empty state placeholder if no trips

### ItineraryCard
- **Purpose**: Display generated trip plan
- **Key Features**:
  - Hero image with destination title overlay
  - Flight info row with price and dates
  - Hotel info with star rating
  - Day-by-day accordion (expandable sections)
  - Each day shows: time, activity name, location, description
  - Save button at bottom

### BlogPostPage
- **Purpose**: Beautiful editorial-style trip blog
- **Key Features**:
  - Full-width hero with gradient overlay
  - Sticky author info and table of contents
  - Day-by-day content sections with dividers
  - 3-column photo grid after each day
  - Serif font for editorial warmth
  - CTA section to plan similar trips
  - Responsive layout (680px max-width for content)

---

## Tailwind CSS Customization

### Color System
```typescript
colors: {
  'warm-white': '#fafaf8',      // Base background
  'off-white': '#f5f3f0',       // Card backgrounds
  'text-primary': '#1a1a2e',    // Main text
  'text-secondary': '#6b6b7f',  // Secondary text
  'teal': '#0d7377',            // Primary accent
  'ocean': '#084c61',           // Secondary accent
}
```

### Custom Animations
```css
@keyframes fade-in { /* Messages appear */
@keyframes slide-up { /* Cards slide up */
@keyframes highlight { /* Preference flashes */
@keyframes typing { /* Typing dots animation */
@keyframes pulse-soft { /* Live status dot */
```

### Utility Classes
```css
.flex-center           /* Flex + center */
.transition-smooth    /* Standard animation */
.message-enter        /* Message animation */
.pref-update         /* Preference flash */
.typing-dots         /* Typing indicator */
```

---

## State Flow Examples

### Example 1: User sends message

```
User types "I want to go to Tokyo"
    ↓
handleSendMessage() called
    ↓
addMessage({ role: 'user', content: '...' })
    ↓
Store updates → messages array changes
    ↓
Component re-renders → new message appears
    ↓
scrollToBottom() → auto-scroll to new message
    ↓
setTypingStatus(true) → typing indicator appears
    ↓
[Wait 2 seconds for agent response]
    ↓
setTypingStatus(false) → remove typing indicator
    ↓
addMessage({ role: 'agent', content: '...' })
    ↓
setItinerary({...}) → itinerary appears in chat
    ↓
updatePreference('budget', '$$') → preference updates with animation
```

### Example 2: Preference updates

```
Agent extracts preference from user message
    ↓
updatePreference('vibe', 'Relaxed')
    ↓
Store updates preferences array
    ↓
Preference item gets updated: true flag
    ↓
Component adds 'pref-update' class
    ↓
Animation triggers (1 second highlight flash)
    ↓
After animation ends, class removed
```

### Example 3: Day accordion expansion

```
User clicks "Day 2" header in itinerary
    ↓
toggleDayExpanded(2) called
    ↓
expandedDays Set updates: new Set([1, 2])
    ↓
Component re-renders
    ↓
ChevronIcon gets 'rotate-180' class
    ↓
Day 2 activities section slides down (ChevronDownIcon rotation)
```

---

## Integration Points (When Backend Ready)

### Chat API
```typescript
POST /api/chat
{
  userId: string
  message: string
  conversationId?: string
}

Response:
{
  agentMessage: string
  preferences?: Record<string, string>
  itinerary?: Itinerary
}
```

**Integration**: In `CenterPanel.handleSendMessage()`, replace setTimeout with actual API call.

### SSE for Preferences
```typescript
EventSource("/api/preferences-stream?userId=123")

Events:
{
  type: "preference-update"
  key: "budget"
  value: "Mid-range"
}
```

**Integration**: Create a custom hook `usePreferenceStream()` that listens to EventSource and calls `updatePreference()`.

### Trips API
```typescript
GET /api/trips?userId=123&tab=my|friends

Response: Trip[]
```

**Integration**: In `RightPanel`, replace mockTrips with React Query useQuery.

### Blog Post API
```typescript
GET /api/trips/:id

Response: BlogPost
```

**Integration**: In `BlogPostPage`, fetch post data based on `params.id`.

---

## Micro-interactions Breakdown

### 1. Preference Update Animation
```css
.pref-update {
  animation: highlight 1s ease-in-out;
}

@keyframes highlight {
  0% { background-color: rgba(13, 115, 119, 0) }
  50% { background-color: rgba(13, 115, 119, 0.1) }
  100% { background-color: rgba(13, 115, 119, 0) }
}
```

**Trigger**: `updatePreference()` sets `updated: true` on preference

**Duration**: 1 second

**Effect**: Yellow-green glow flash on the preference chip

### 2. Message Entry Animation
```css
.message-enter {
  animation: slide-up 0.3s ease-out;
}

@keyframes slide-up {
  0% { transform: translateY(10px); opacity: 0 }
  100% { transform: translateY(0); opacity: 1 }
}
```

**Trigger**: Message added to store

**Duration**: 0.3 seconds

**Effect**: New message slides up and fades in

### 3. Itinerary Card Animation
```css
.slide-up.animate-fade-in {
  animation: slide-up 0.3s ease-out, fade-in 0.3s ease-in-out;
}
```

**Effect**: Card slides up when itinerary is generated

### 4. Typing Indicator
```css
.typing-dot {
  animation: typing 0.6s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.1s }
.typing-dot:nth-child(3) { animation-delay: 0.2s }

@keyframes typing {
  0%, 60%, 100% { opacity: 0.3 }
  30% { opacity: 1 }
}
```

**Effect**: Three dots pulsing at offset times

### 5. Trip Card Hover
```css
.group:hover {
  transform: translateY(-2px);
  border-color: #0d7377;
  box-shadow: md;
}

.group-hover\:scale-105 {
  transform: scale(1.05);
}
```

**Effect**: Card tilts up, image zooms slightly, border turns teal

### 6. Mic Button Active State
```css
.isRecording ? 'bg-teal/20 text-teal' : 'text-text-muted'
```

**Effect**: Button lights up teal when recording

---

## Performance Considerations

### Optimization Done
- ✅ Next/Image for image optimization
- ✅ Zustand for minimal re-renders
- ✅ Component memoization opportunities (React.memo on card components)
- ✅ CSS animations instead of JS animations where possible
- ✅ Lazy loading ready (can add SuspenseList later)

### Optimization TODO
- [ ] Intersection Observer for message virtualization (if chat gets long)
- [ ] React.memo on LeftPanel, RightPanel for isolated updates
- [ ] Image lazy loading on blog page
- [ ] Code splitting on route (automatic with Next.js)

---

## Responsive Design

### Breakpoints (via Tailwind)
- **Desktop**: 1280px+ (primary, all 3 panels visible)
- **Tablet**: 768px - 1279px (might need collapse logic)
- **Mobile**: < 768px (not supported yet)

### Current Implementation
- All panels use fixed positioning
- No responsive adjustments yet (can add later)

### Future Tablet Support
- Collapsible left/right panels
- Full-width center on mobile
- Hamburger menu for preferences
- Drawer for trip memory

---

## Testing Strategy

### Component Tests (Jest + React Testing Library)
- Test message adding and display
- Test preference updates and animations
- Test expandable itinerary days
- Test form submissions

### Integration Tests
- Test entire chat flow
- Test message → preference → UI update flow
- Test itinerary generation and display

### E2E Tests (Playwright/Cypress)
- User types message → agent responds → itinerary shows
- User clicks trip card → navigates to blog page
- User expands day in itinerary → activities display

---

## Deployment

### Vercel (Recommended for Next.js)
```bash
vercel --prod
```

### Environment Variables
Copy `.env.local.example` to `.env.local` and fill in:
```
NEXT_PUBLIC_API_URL=https://api.tripmind.app
NEXT_PUBLIC_AUTH0_DOMAIN=tripmind.auth0.com
NEXT_PUBLIC_AUTH0_CLIENT_ID=xxx
NEXT_PUBLIC_ELEVENLABS_API_KEY=xxx
```

### Build Output
```bash
npm run build
# .next folder created, ready for deployment
```

---

## Debugging Tips

### 1. Check Store State
```typescript
import { useAppStore } from '@/store/appStore'

// In component
const { preferences, messages } = useAppStore()
console.log(preferences, messages)
```

### 2. Watch Animations
Add `animation-delay: 0s !important` to CSS to remove delays and speed up testing.

### 3. Mock Data
All data is hardcoded as `mock*` objects. Search for "mock" to find data sources.

### 4. Network Requests
When backend is ready, use browser DevTools → Network to inspect API calls.

---

## File Locations Quick Reference

| Purpose | File |
|---------|------|
| Global styles | `app/globals.css` |
| Tailwind config | `tailwind.config.ts` |
| App state | `store/appStore.ts` |
| Utilities | `lib/utils.ts` |
| Icons | `components/Icons.tsx` |
| Home page | `app/page.tsx` |
| Blog post page | `app/trip/[id]/page.tsx` |
| Preferences panel | `components/LeftPanel.tsx` |
| Chat panel | `components/CenterPanel.tsx` |
| Trips panel | `components/RightPanel.tsx` |
| Itinerary card | `components/ItineraryCard.tsx` |
| Blog component | `components/BlogPostPage.tsx` |

---

## Next Steps

1. **Backend Integration**: Replace mock data with API calls
2. **Auth0 Setup**: Integrate login/logout flow
3. **ElevenLabs**: Wire up voice input/output
4. **React Query**: Replace Zustand for server state
5. **Testing**: Add Jest + Playwright tests
6. **Analytics**: Add event tracking
7. **Mobile**: Add responsive tablet/mobile support
8. **PWA**: Add service worker for offline support

---

## Resources

- [Next.js 14 Docs](https://nextjs.org/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Zustand Docs](https://github.com/pmndrs/zustand)
- [React Testing Library](https://testing-library.com/react)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
