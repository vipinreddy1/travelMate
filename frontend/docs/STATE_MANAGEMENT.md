# TripMind Frontend — State Management with Zustand

## Overview

TripMind uses **Zustand** for state management — a lightweight, TypeScript-friendly state management library. The entire app state is centralized in a single store located at `store/appStore.ts`.

**Why Zustand?**
- Minimal boilerplate compared to Redux
- Built-in TypeScript support
- Excellent performance (selector-based subscriptions)
- No provider wrapper required
- Simple API: create → subscribe → use

---

## Store Structure

### AppStore Interface

```typescript
interface AppStore {
  // ========== PREFERENCES ==========
  preferences: Preference[]
  updatePreference: (key: string, value: string) => void
  
  // ========== MESSAGES ==========
  messages: Message[]
  addMessage: (message: Omit<Message, 'id'>) => void
  setTypingStatus: (isTyping: boolean) => void
  clearMessages: () => void
  
  // ========== ITINERARY ==========
  itinerary: Itinerary | null
  setItinerary: (itinerary: Itinerary) => void
  
  // ========== UI STATE ==========
  isRecording: boolean
  setRecording: (recording: boolean) => void
}
```

---

## State Sections

### 1. Preferences State

**Purpose**: Store user travel preferences that update in real-time as they chat with the AI.

**Type**:
```typescript
interface Preference {
  key: string              // Unique identifier: 'budget', 'vibe', 'pace', etc.
  icon: string            // Emoji icon: '💰', '🎯', '🚶', etc.
  label: string           // Display label: 'Budget', 'Vibe', 'Pace', etc.
  value: string           // Current value: '$$ (Mid-range)', 'Relaxed', 'Slow explorer', etc.
  updated?: boolean       // Animation flag for UI feedback
}
```

**Initial Preferences**:
```typescript
const initialPreferences: Preference[] = [
  { key: 'budget', icon: '💰', label: 'Budget', value: '$$ (Mid-range)' },
  { key: 'vibe', icon: '🎯', label: 'Vibe', value: 'Relaxed' },
  { key: 'pace', icon: '🚶', label: 'Pace', value: 'Slow explorer' },
  { key: 'dietary', icon: '🥗', label: 'Dietary', value: 'Vegetarian' },
  { key: 'stay', icon: '🏨', label: 'Stay', value: 'Boutique hotels' },
  { key: 'group', icon: '👤', label: 'Group', value: 'Solo' },
]
```

**Action: updatePreference()**

```typescript
updatePreference: (key: string, value: string) =>
  set((state: AppStore) => ({
    preferences: state.preferences.map((pref: Preference) =>
      pref.key === key ? { ...pref, value, updated: true } : pref
    ),
  }))
```

**Usage**:
```tsx
const updatePreference = useAppStore((state) => state.updatePreference)

// Update budget to luxury
updatePreference('budget', '$$$ (Luxury)')
```

**UI Feedback**:
- When `updated` is true, LeftPanel applies `pref-update` class
- CSS class triggers `highlight` keyframe animation (teal flash)
- Pulse animation shows "Updating as you chat..."

---

### 2. Messages State

**Purpose**: Store chat history between user and AI agent.

**Type**:
```typescript
interface Message {
  id: string              // Unique ID: 'msg-1729788456123'
  role: 'user' | 'agent'  // Sender: user or AI
  content: string         // Message text
  timestamp: Date         // When message was created
  isTyping?: boolean      // Typing indicator flag
}
```

**Action: addMessage()**

Adds a new message to the messages array with auto-generated ID.

```typescript
addMessage: (message: Omit<Message, 'id'>) =>
  set((state: AppStore) => ({
    messages: [
      ...state.messages,
      {
        ...message,
        id: `msg-${Date.now()}`,  // Timestamp-based ID
      },
    ],
  }))
```

**Usage**:
```tsx
const addMessage = useAppStore((state) => state.addMessage)

// Add user message
addMessage({
  role: 'user',
  content: 'Plan a trip to Tokyo',
  timestamp: new Date(),
})

// Add agent response (after API call)
addMessage({
  role: 'agent',
  content: 'I\'ve created a 3-day itinerary...',
  timestamp: new Date(),
})
```

**Action: setTypingStatus()**

Sets typing indicator for agent messages.

```typescript
setTypingStatus: (isTyping: boolean) =>
  set((state: AppStore) => ({
    messages: state.messages.map((msg) =>
      msg.role === 'agent'
        ? { ...msg, isTyping }
        : msg
    ),
  }))
```

**Usage**:
```tsx
const setTypingStatus = useAppStore((state) => state.setTypingStatus)

// Show typing indicator
setTypingStatus(true)

// Simulate AI thinking...
setTimeout(() => {
  addMessage({ role: 'agent', content: 'Response...', timestamp: new Date() })
  setTypingStatus(false)
}, 2000)
```

**Action: clearMessages()**

Resets message history (for future "new chat" button).

```typescript
clearMessages: () =>
  set({
    messages: [],
  })
```

**UI Rendering**:
- Messages render in order (oldest at top, newest at bottom)
- Auto-scroll to bottom when new message added
- User messages: right-aligned, teal background pill
- Agent messages: left-aligned, white card background
- Typing indicator: animated dots below agent message

---

### 3. Itinerary State

**Purpose**: Store the generated trip itinerary.

**Type**:
```typescript
interface Itinerary {
  destination: string     // City name: 'Tokyo'
  country: string         // Country name: 'Japan'
  startDate: string       // ISO date: '2024-10-12'
  endDate: string         // ISO date: '2024-10-22'
  flights: {
    airline: string       // 'ANA Airways'
    departure: string     // 'SFO'
    arrival: string       // 'NRT'
    price: number         // 680 (in USD)
    date: string          // '2024-10-12'
  }
  hotel: {
    name: string          // 'The Hoshinoya Tokyo'
    rating: number        // 5
    price: number         // 450 (per night, USD)
    image: string         // URL
  }
  days: Array<{           // Day-by-day breakdown
    dayNumber: number     // 1, 2, 3...
    date: string          // '2024-10-12'
    activities: Array<{
      time: string        // '14:00'
      name: string        // 'Arrival at Narita'
      location: string    // 'Tokyo Airport'
      description?: string
    }>
  }>
  heroImage: string       // Hero image URL
}
```

**Action: setItinerary()**

```typescript
setItinerary: (itinerary: Itinerary) =>
  set({
    itinerary,
  })
```

**Usage**:
```tsx
const setItinerary = useAppStore((state) => state.setItinerary)

const mockItinerary: Itinerary = {
  destination: 'Tokyo',
  country: 'Japan',
  startDate: '2024-10-12',
  endDate: '2024-10-22',
  // ... rest of structure
}

setItinerary(mockItinerary)
```

**UI Rendering**:
- ItineraryCard component renders when itinerary is not null
- Displays hero image, flight/hotel details, day-by-day activities
- Scrolls into view with `useRef` and `scrollIntoView()`
- Disappears when cleared or new itinerary generated

**Initial Value**: `null`

---

### 4. UI State

**Purpose**: Track temporary UI states like recording status.

**State**: `isRecording: boolean`

**Action: setRecording()**

```typescript
setRecording: (recording: boolean) =>
  set({
    isRecording: recording,
  })
```

**Usage**:
```tsx
const isRecording = useAppStore((state) => state.isRecording)
const setRecording = useAppStore((state) => state.setRecording)

// Start recording
setRecording(true)

// Stop recording
setRecording(false)
```

**Future Integration**:
- ElevenLabs voice input recording
- Visual feedback (mic button color change)
- Record audio and send as message

---

## Store Creation & Initialization

### Creating the Store

```typescript
export const useAppStore = create<AppStore>((set) => ({
  // ========== PREFERENCES ==========
  preferences: initialPreferences,
  
  updatePreference: (key: string, value: string) =>
    set((state: AppStore) => ({
      preferences: state.preferences.map((pref: Preference) =>
        pref.key === key ? { ...pref, value, updated: true } : pref
      ),
    })),
  
  // ========== MESSAGES ==========
  messages: [],
  
  addMessage: (message: Omit<Message, 'id'>) =>
    set((state: AppStore) => ({
      messages: [
        ...state.messages,
        {
          ...message,
          id: `msg-${Date.now()}`,
        },
      ],
    })),
  
  // ... rest of actions
}))
```

### Key Points

1. **Set Function**: Each action returns new state object
2. **Immutability**: Always create new arrays/objects, never mutate
3. **Type Safety**: Full TypeScript support for all actions
4. **No Reducers**: Simple key-value action structure

---

## Using the Store in Components

### Basic Pattern

```tsx
import { useAppStore } from '@/store/appStore'

export const MyComponent = () => {
  // Subscribe to specific slice of state
  const preferences = useAppStore((state) => state.preferences)
  
  return (
    <div>
      {preferences.map((pref) => (
        <div key={pref.key}>{pref.value}</div>
      ))}
    </div>
  )
}
```

### Advanced Pattern: Selecting Multiple Values

```tsx
const MyComponent = () => {
  // Get multiple values in one hook
  const { messages, addMessage, itinerary } = useAppStore((state) => ({
    messages: state.messages,
    addMessage: state.addMessage,
    itinerary: state.itinerary,
  }))
  
  return (
    // Use messages, addMessage, itinerary
  )
}
```

### Anti-Pattern: Avoid This

```tsx
// ❌ WRONG: Subscribes to entire store, causes unnecessary re-renders
const state = useAppStore()
const messages = state.messages  // Any change to any state part causes re-render
```

### Best Practice: Selector Functions

```tsx
// ✅ RIGHT: Only subscribes to messages, ignores other state changes
const messages = useAppStore((state) => state.messages)
```

---

## Notable Zustand Features Used

### 1. State Selection (Optimization)

The selector function ensures components only re-render when their specific state slice changes.

```typescript
// Component only re-renders when messages change
useAppStore((state) => state.messages)

// Doesn't re-render when preferences change
```

### 2. Direct State Modification

Actions receive `set` function to update state:

```typescript
updatePreference: (key: string, value: string) =>
  set((state: AppStore) => ({
    // Return new state object
    preferences: state.preferences.map(...)
  }))
```

### 3. Direct Store Access (rarely needed)

```typescript
// Get current state without subscribing
const currentMessages = useAppStore.getState().messages

// Direct update without component
useAppStore.setState({
  itinerary: mockItinerary
})
```

This should be used sparingly in event handlers or async operations.

---

## Data Flow Example: Sending a Message

```
User types "Plan Tokyo trip"
  ↓
User clicks Send button
  ↓
CenterPanel.handleSendMessage()
  ↓
addMessage({ role: 'user', content: 'Plan Tokyo trip', timestamp: new Date() })
  ↓
Zustand.set({ messages: [...messages, newMessage] })
  ↓
CenterPanel re-renders (subscribed to messages)
  ↓
New user message appears in chat
  ↓
setIsLoading(true), setTypingStatus(true)
  ↓
setTimeout(() => {
  setTypingStatus(false)
  addMessage({ role: 'agent', content: 'I\'ve created...', timestamp: new Date() })
  setItinerary(mockItinerary)
}, 2000)
  ↓
CenterPanel re-renders with agent message and itinerary
  ↓
ItineraryCard slides in with animation
```

---

## Persistence & Future Enhancements

### Current State

**Ephemeral**: All state resets on page refresh.

### Future: LocalStorage Persistence

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAppStore = create<AppStore>(
  persist(
    (set) => ({
      // Store definition
    }),
    {
      name: 'tripMind-store', // localStorage key
      partialize: (state) => ({
        preferences: state.preferences,
        // Don't persist: messages, itinerary (session-based)
      }),
    }
  )
)
```

### Future: Session API

Store chat sessions on backend:
- Save messages and itineraries to database
- Retrieve session history
- Create new sessions

### Future: Analytics Middleware

Track user interactions:

```typescript
const useAppStore = create<AppStore>(
  (set) => ({
    // Store definition
  }),
  {
    name: 'tripMind-store',
    onStateChange: (state) => {
      analytics.track('app-state-change', state)
    },
  }
)
```

---

## Debugging

### React DevTools

1. Install Redux DevTools Extension
2. Connect Zustand (requires middleware setup)

### Manual Debugging

```typescript
// Log current state
console.log(useAppStore.getState())

// Watch state changes
useAppStore.subscribe(
  (state) => state.messages,
  (messages) => console.log('Messages changed:', messages)
)
```

### In Browser Console

```javascript
// Access store directly
window.__store__.getState()

// Update state
window.__store__.setState({ ... })
```

---

## Performance Tips

1. **Use Selectors**: Always use selector functions to avoid unnecessary re-renders
2. **Memoize Selectors**: For complex selections, memoize the selector
3. **Batch Updates**: Combine multiple state updates into one `set` call when possible
4. **Lazy Load**: Don't load full itineraries initially

---

## Best Practices

1. ✅ Use specific selectors: `useAppStore((state) => state.preferences)`
2. ✅ Keep actions pure: No side effects in actions
3. ✅ Type all state: Full TypeScript coverage
4. ✅ Organize by domain: Preferences, Messages, Itinerary, UI
5. ✅ Document state fields and actions
6. ❌ Don't mutate state directly
7. ❌ Don't store functions in state (except actions)
8. ❌ Don't make store too large (consider splitting for very large apps)

---

## Summary

Zustand provides a simple, performant state management solution for TripMind. The store is organized into four main domains:

- **Preferences**: User travel preferences
- **Messages**: Chat history
- **Itinerary**: Generated trip plan
- **UI**: Temporary UI states

Selector-based subscriptions ensure optimal performance, while TypeScript provides type safety throughout the application.

