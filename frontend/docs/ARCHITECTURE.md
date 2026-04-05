# TripMind Frontend — Architecture & System Design

## High-Level Overview

TripMind frontend is a modern Next.js 14 application built with React 18 and TypeScript. It features a sophisticated 3-panel layout system for real-time trip planning with AI assistance, complemented by an editorial blog interface for sharing travel experiences.

**Core Philosophy**: Trustworthy, calm, and sophisticated travel companion UI.

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│ (Components: LeftPanel, CenterPanel, RightPanel, BlogPost)   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     STATE MANAGEMENT                          │
│        (Zustand store for preferences, messages, UI state)    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    UTILITY LAYER                              │
│      (Helpers, formatters, styling utilities, custom hooks)   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER (Future)                        │
│     (API calls to backend, ElevenLabs integration, Auth0)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 3-Panel Layout System

The frontend uses a fixed **3-panel layout** that never scrolls externally. Each panel scrolls independently within its bounds.

### Layout Structure

```
┌─────────────────┬──────────────────────────┬───────────────────┐
│  LEFT PANEL     │     CENTER PANEL         │  RIGHT PANEL      │
│  (Fixed 220px)  │  (Flexible remaining)    │ (Fixed 280px)     │
│                 │                          │                   │
│  • Preferences  │  • Chat interface        │  • Trip memory    │
│  • Travel DNA   │  • Message list          │  • My trips       │
│  • Live updates │  • Itinerary cards       │  • Friends trips  │
│                 │  • Input with mic/send   │  • Browse history │
│                 │  • Voice integration     │                   │
└─────────────────┴──────────────────────────┴───────────────────┘
```

### Panel Behavior

- **Position**: `position: fixed` across entire viewport height
- **Scrolling**: Each panel scrolls independently with `overflow-y: auto`
- **No body scroll**: Outer shell never scrolls, maintaining stable layout
- **Responsive**: Collapses gracefully on tablets/mobile (implemented via media queries)

---

## Component Hierarchy

```
RootLayout (app/layout.tsx)
  └── Body (.antialiased, warmWhite background)
      
      Page (app/page.tsx)
        ├── LeftPanel
        │   └── Preferences List
        │       └── Individual Preference Items (with animations)
        │
        ├── CenterPanel
        │   ├── Chat Interface Header
        │   ├── Message List Container
        │   │   ├── Agent Messages (left-aligned, white card)
        │   │   ├── User Messages (right-aligned, teal pill)
        │   │   └── Typing Indicator (dots animation)
        │   ├── ItineraryCard (conditional render)
        │   │   ├── Hero Image with Gradient
        │   │   ├── Flight Details Section
        │   │   ├── Hotel Details Section
        │   │   └── Day-by-Day Activities (collapsible)
        │   └── Input Area
        │       ├── Text Input
        │       ├── Mic Button (voice ready)
        │       └── Send Button
        │
        └── RightPanel
            ├── Tab Navigation (My Trips | Friends)
            ├── Trip List
            │   └── Individual Trip Cards
            │       ├── Trip Image
            │       ├── Destination & Date
            │       ├── Status Badge
            │       └── Friend Avatar (if applicable)
            └── ScrollableContent

      TripPage (app/trip/[id]/page.tsx)
        └── BlogPostPage
            ├── Hero Section
            │   ├── Cover Image with Gradient
            │   └── Title Overlay
            ├── Sticky Header
            │   ├── Author Info
            │   ├── Trip Duration Meta
            │   ├── "Written with TripMind" Badge
            │   └── Table of Contents (Day Selector)
            ├── Article Content
            │   ├── Opening Paragraph
            │   └── Day Sections
            │       ├── Day Divider
            │       ├── Day Content (serif font)
            │       ├── Photo Grid (3 columns)
            │       └── CTA to Plan Similar Trip
            └── Footer
                ├── Social Share Options
                └── Back to Home Link
```

---

## Data Flow & State Management

### Zustand Store Structure

```typescript
AppStore {
  // Preferences State
  preferences: Preference[] ✨ LIVE UPDATES
  updatePreference(key, value)
  
  // Messages State
  messages: Message[] 💬
  addMessage(message)
  setTypingStatus(isTyping)
  clearMessages()
  
  // Itinerary State
  itinerary: Itinerary | null 🗺️
  setItinerary(itinerary)
  
  // UI State
  isRecording: boolean 🎤
  setRecording(recording)
}
```

### Data Flow Example

**User sends message** → CenterPanel input handler calls `addMessage()` → Zustand updates `messages` array → Component re-renders with new message → Mock AI response simulated → `setItinerary()` stores generated itinerary → ItineraryCard renders

---

## Page Routes

### Route 1: Main App (`/`)
- **Component**: `page.tsx`
- **Layout**: 3-panel fixed layout
- **Features**:
  - Real-time chat interface
  - Live preference updates
  - Itinerary generation & display
  - Trip memory browser
  - Voice input ready (ElevenLabs)

### Route 2: Trip Details (`/trip/[id]`)
- **Component**: `BlogPostPage` via `app/trip/[id]/page.tsx`
- **Layout**: Full-width editorial layout
- **Features**:
  - Hero image with gradient
  - Day-by-day narrative
  - Photo galleries per day
  - Sticky table of contents
  - Author information
  - Call-to-action for trip planning

---

## Key Features & Implementation

### 1. **Live Preference Updates**
- Preferences update in real-time with visual feedback
- Animation: `pref-update` class triggers `highlight` keyframe
- Preferences tracked with `updated` flag
- Updated indicator: pulse animation: `pulse-soft`

### 2. **Chat Interface**
- Messages stored in order (oldest → newest)
- Auto-scroll to latest message
- User messages: right-aligned, teal background
- Agent messages: left-aligned, white card
- Typing indicator: animated dots with staggered delays
- Input validation: trimmed text check

### 3. **Itinerary Generation**
- Generated on agent response
- Displays as expandable card
- Days are collapsible with smooth chevron rotation
- Flight & hotel details in 2-column grid
- Activities with time, location, description

### 4. **Trip Memory Browser**
- Two tabs: "My Trips" & "Friends"
- Mock trip data with images, dates, status
- Hover effect: subtle upward translate
- Clickable for future navigation

### 5. **Editorial Blog Layout**
- Full-width hero with gradient overlay
- Sticky header stays on scroll
- Serif font for body text (Lora)
- Day-by-day content sections
- 3-column photo grid per day
- Responsive image container with object-fit

---

## Animation & Visual Effects

### Keyframe Animations

```css
pulse-soft          // Soft pulsing (0.5 → 1 opacity)
fade-in             // Element fades in (0 → 1 opacity)
slide-up            // Element slides up 10px and fades in
highlight           // Teal background flash animation
typing              // Typing dots staggered animation
```

### Animation Usage

- **Message enter**: `message-enter` class (slide-up)
- **Preference update**: `pref-update` class (highlight + border flash)
- **Typing indicator**: `.typing-dot` with staggered delays
- **Itinerary card**: `slide-up animate-fade-in` classes

### Transitions

- Default: `transition-all duration-300 ease-out`
- Hover effects: smooth color/transform transitions
- Chevron rotation: `transition-transform duration-300`

---

## State Persistence Strategy

**Current**: All state is ephemeral (resets on page refresh)

**Future Enhancement**:
- Implement LocalStorage wrapper for preferences
- Session-based storage for current chat
- Backend API integration for trip history
- Auth0 integration for user authentication

---

## Performance Considerations

### Optimization Implemented

1. **Image Loading**:
   - Next.js `Image` component with lazy loading
   - Unsplash URLs with width/height parameters for CDN optimization
   - Hero images: `priority` attribute for initial page

2. **Code Splitting**:
   - Dynamic component imports via Next.js
   - Route-based code splitting (Page 1 vs Page 2)

3. **State Updates**:
   - Zustand uses shallow updates only when state slice changes
   - Component subscriptions via `useAppStore((state) => state.slice)`

4. **CSS**:
   - Tailwind CSS with PurgeCSS (removes unused styles)
   - Custom utility classes for common patterns

### Areas for Enhancement

- Add React.memo for non-updating components
- Implement message virtualization for long chat histories
- Lazy load trip cards in RightPanel
- Debounce input validation

---

## Styling Architecture

### Tailwind CSS Extension

The Tailwind config extends defaults with:

**Colors**: 15+ custom colors (warm-white, teal variants, text colors)
**Typography**: Custom font stack (Inter + Lora)
**Spacing**: Consistent 4px-based scale
**Border Radius**: Soft 8-12px defaults
**Shadows**: 5 custom shadow levels from xs to xl
**Animations**: 5 custom animations with keyframes

### CSS Layers

```
Global Styles (globals.css)
  ├── @tailwind directives
  ├── Custom utility classes (.flex-center, .transition-smooth)
  ├── Scrollbar styling
  ├── Animation definitions
  └── Component-specific animations

Tailwind Components (via @apply)
  └── Utility-first approach (no component layer)

Component-Level Styles (via className)
  └── cn() utility for conditional classes
```

---

## TypeScript Interfaces

### Core Models

```typescript
interface Preference {
  key: string                    // Unique ID
  icon: string                   // Emoji icon
  label: string                  // Display label
  value: string                  // Current value
  updated?: boolean              // Animation flag
}

interface Message {
  id: string                     // Unique ID (timestamp-based)
  role: 'user' | 'agent'         // Message sender
  content: string                // Message text
  timestamp: Date                // Creation time
  isTyping?: boolean             // Typing indicator
}

interface Itinerary {
  destination: string            // City name
  country: string                // Country name
  startDate: string              // ISO date
  endDate: string                // ISO date
  flights: FlightInfo            // Flight details
  hotel: HotelInfo               // Hotel details
  days: DayItinerary[]           // Activities per day
  heroImage: string              // Hero image URL
}

interface DayItinerary {
  dayNumber: number
  date: string
  activities: Activity[]
}

interface Activity {
  time: string                   // "HH:MM" format
  name: string                   // Activity name
  location: string               // Location
  description?: string           // Optional description
}
```

---

## Error Handling Strategy

### Current Implementation

- TypeScript strict mode catches most compile-time errors
- Runtime errors logged to console (future: error boundary)

### Future Enhancements

- Implement Error Boundary component for graceful fallbacks
- API error handling and user-friendly messages
- Form validation with error display
- Toast notifications for user feedback
- Sentry integration for error tracking

---

## Integration Points

### Planned Integrations

1. **Backend API**
   - Trip planning algorithm
   - Preference optimization
   - Itinerary generation

2. **ElevenLabs API**
   - Voice input/output for chat
   - Natural language processing

3. **Google Maps API**
   - Location search
   - Route optimization
   - Place details

4. **Auth0**
   - User authentication
   - Session management
   - Profile management

5. **Future: Social Features**
   - Trip sharing
   - Friend recommendations
   - Collaborative planning

---

## Conclusion

The TripMind frontend architecture balances **aesthetics with functionality**. The 3-panel layout provides an intuitive interface for trip planning while maintaining a premium, editorial feel. The modular component structure and centralized state management make it easy to extend with new features and integrate with backend services.
