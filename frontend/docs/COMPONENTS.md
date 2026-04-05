# TripMind Frontend — Components Guide

## Component Overview

All components are **functional React components** with TypeScript support. Most use the `'use client'` directive for client-side rendering.

---

## Core Components

### 1. LeftPanel

**Location**: `components/LeftPanel.tsx`

**Purpose**: Display user travel preferences that update in real-time as the user chats.

**Props**: None (uses Zustand store directly)

**Features**:
- Shows 6 default preferences (Budget, Vibe, Pace, Dietary, Stay, Group)
- Live updates with visual feedback
- Animated highlight when preference updates
- Pulse animation indicator for "Updating as you chat..."

**Key Markup**:
```tsx
<div className="fixed left-0 top-0 h-screen w-[220px] bg-off-white border-r border-gray-100">
  {preferences.map((pref) => (
    <div className={cn('px-3 py-2 rounded-full bg-white border', pref.updated && 'pref-update border-teal ring-2 ring-teal/10')}>
      {/* emoji icon, label, value */}
    </div>
  ))}
</div>
```

**Styling Notes**:
- Fixed width: 220px
- Vertical scroll: `overflow-y-auto`
- Border right: separates from center panel
- Preference cards: rounded-full pills with hover states

---

### 2. CenterPanel

**Location**: `components/CenterPanel.tsx`

**Purpose**: Main chat interface and AI conversation space.

**Props**: None (uses Zustand store)

**Features**:
- User/agent message display
- Auto-scroll to latest message
- Text input with send button
- Mic button for voice (ready state)
- Itinerary card generation below chat
- Mock AI responses with typing simulation

**Key State**:
```tsx
const [input, setInput] = useState('')
const [isLoading, setIsLoading] = useState(false)
const messagesEndRef = useRef<HTMLDivElement>(null)
```

**Message Rendering**:
- User messages: `text-right`, `bg-teal`, rounded-full pill
- Agent messages: `text-left`, `bg-white`, card style
- Typing indicator: animated dots below agent message

**Input Area**:
- Text input field with placeholder
- Mic button (triggers recording state)
- Send button (disabled if input empty)
- Auto-focus on mount

**Initial Message**: Mock greeting on first load

---

### 3. RightPanel

**Location**: `components/RightPanel.tsx`

**Purpose**: Display trip history and friends' shared trips.

**Props**: None (uses local state for tab switching)

**Features**:
- Two tabs: "My Trips" & "Friends"
- Trip cards with images and metadata
- Hover animation (subtle upward translate)
- Status badges (Completed, Ongoing)
- Optional friend avatar overlay

**Key State**:
```tsx
const [activeTab, setActiveTab] = useState<'my' | 'friends'>('my')
```

**Trip Card Structure**:
```
trip-card
├── Image (400x300)
├── Destination & Country
├── Date Range
├── Status Badge
└── Friend Avatar (optional)
```

**Styling Notes**:
- Fixed width: 280px
- Tab buttons: teal background when active
- Cards: hover effect with `translate-y[-2px]`
- Grid layout: responsive trip cards

---

### 4. ItineraryCard

**Location**: `components/ItineraryCard.tsx`

**Props**:
```tsx
interface ItineraryCardProps {
  itinerary: Itinerary
}
```

**Purpose**: Display generated travel itinerary with collapsible day-by-day activities.

**Features**:
- Hero image section with gradient overlay
- Flight and hotel details in 2-column grid
- Trip duration metadata
- Collapsible day sections with smooth animation
- Activity list per day with time, name, location
- Star rating for hotels

**Key State**:
```tsx
const [expandedDays, setExpandedDays] = useState<Set<number>>(new Set([1]))
```

**Day Expansion**:
- First day expanded by default
- Chevron icon rotates on expand/collapse
- Smooth `transition-transform duration-300`

**Flight & Hotel Cards**:
- Icon indicators (PlaneIcon, HotelIcon)
- Price prominently displayed in teal
- Route arrows for flights
- Star ratings for hotels

**Activities Section**:
- Time displayed on right in teal
- Activity name, location, description
- Icon indicators (MapPinIcon, CalendarIcon)
- Vertical timeline style (borders between items)

**Animation**: Slide-up and fade-in on generation

---

### 5. BlogPostPage

**Location**: `components/BlogPostPage.tsx`

**Props**:
```tsx
interface BlogPostPageProps {
  params: { id: string }
}
```

**Purpose**: Editorial-style blog post page for sharing travel experiences.

**Features**:
- Full-width hero image with text overlay
- Sticky header with author info and table of contents
- Day-by-day narrative sections
- Photo grids (3 columns per day)
- CTA buttons for planning similar trips
- Social sharing options (future)

**Header Section**:
- Hero image: 400px height with gradient overlay
- Title and destination overlaid at bottom
- Author avatar (48x48 circular)
- Author name and trip dates
- "Written with TripMind" badge

**Sticky TOC**:
- Horizontal scroll of day buttons
- Active day highlighted in teal
- Smooth scroll behavior
- Responsive design

**Content Sections**:
- Opening paragraph (serif font, large size)
- Day dividers with horizontal rules
- Day title and content (sans-serif for metadata, serif for copy)
- Photo grid: 3 images per row
- Gap between photos: responsive

**CTA Section**:
- Button to plan similar trip
- Links back to main app

---

### 6. Icons

**Location**: `components/Icons.tsx`

**Purpose**: SVG icon components used throughout the app.

**Icon Functions** (all accept `IconProps`):

| Icon | Usage | Size | Fill |
|------|-------|------|------|
| `CompassIcon` | Logo placeholder, branding | 24 | stroke |
| `SparkleIcon` | Travel DNA section | 20 | fill (yellow) |
| `MapPinIcon` | Location indicators | 20 | stroke |
| `MicIcon` | Voice input, recording | 24 | conditional |
| `SendIcon` | Message send action | 20 | stroke |
| `BrainIcon` | Trip Memory header | 20 | stroke |
| `StarIcon` | Hotel ratings | 18 | conditional |
| `ChevronDownIcon` | Expand/collapse indicator | 18 | stroke |
| `ArrowRightIcon` | Navigation, direction | 14 | stroke |
| `PlaneIcon` | Flight details | 18 | stroke |
| `HotelIcon` | Hotel details | 18 | stroke |
| `CalendarIcon` | Date indicators | 14 | stroke |
| `UserIcon` | User profile/avatar | 20 | stroke |

**Icon Props Interface**:
```tsx
interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
  className?: string
}

interface MicIconProps extends IconProps {
  isActive?: boolean
}

interface StarIconProps extends IconProps {
  filled?: boolean
}
```

**Usage Example**:
```tsx
<CompassIcon size={24} className="text-teal" />
<StarIcon filled={true} className="text-yellow-400" />
```

**Styling Notes**:
- Default colors: inherited from parent
- Stroke width: 2px for outline icons
- Icons are inline SVG (not external files)
- Support for TailwindCSS color classes

---

## Layout Components (Page-Level)

### Layout Component (`app/layout.tsx`)

**Purpose**: Root layout wrapper for entire application.

**Features**:
- Sets metadata (title, description)
- Configures viewport settings
- Applies global CSS
- Wraps children

**Key Configuration**:
```tsx
metadata: {
  title: 'TripMind - Your Intelligent Travel Companion',
  description: 'Plan smarter trips by learning from your memories and your friends\' experiences.',
}

viewport: {
  width: 'device-width',
  initialScale: 1,
}
```

---

### Page Component (`app/page.tsx`)

**Purpose**: Main app page rendering 3-panel layout.

**Render**:
```tsx
<main className="w-full h-screen overflow-hidden bg-warm-white">
  <LeftPanel />
  <CenterPanel />
  <RightPanel />
</main>
```

**Key Styles**:
- Full width and height
- `overflow-hidden` prevents body scroll
- Warm white background

---

### Trip Page (`app/trip/[id]/page.tsx`)

**Purpose**: Dynamic route for individual trip blog posts.

**Route Parameter**: `[id]` - Trip ID

**Component**:
```tsx
<BlogPostPage params={params} />
```

---

## Utility Functions

### `cn()` - Class Name Merge

**Location**: `lib/utils.ts`

**Purpose**: Merge Tailwind classes with conditional logic using `clsx` and `tailwind-merge`.

**Signature**:
```tsx
function cn(...inputs: ClassValue[]): string
```

**Usage**:
```tsx
<div className={cn('base-styles', condition && 'conditional-styles')}>
```

**Benefit**: Prevents Tailwind specifying conflicts in complex classNames.

---

### Format Functions

**Location**: `lib/utils.ts`

#### formatDate()
```tsx
export const formatDate = (date: string | Date): string
// Input: "2024-10-12" or new Date()
// Output: "October 12, 2024"
```

#### formatTime()
```tsx
export const formatTime = (time: string): string
// Input: "14:00"
// Output: "2:00 PM"
```

#### truncateText()
```tsx
export const truncateText = (text: string, limit: number): string
// Input: "Hello World", 5
// Output: "Hello..."
```

---

## Component Composition Patterns

### Pattern 1: Store Hook Usage

```tsx
'use client'

import { useAppStore } from '@/store/appStore'

export const MyComponent = () => {
  const preferences = useAppStore((state) => state.preferences)
  const updatePreference = useAppStore((state) => state.updatePreference)
  
  return (
    // Component JSX
  )
}
```

### Pattern 2: Conditional Rendering

```tsx
{condition && <ConditionalComponent />}

{items.map((item) => (
  <ItemComponent key={item.id} item={item} />
))}
```

### Pattern 3: Animation Classes

```tsx
<div className="slide-up animate-fade-in">
  {/* Animated content */}
</div>
```

### Pattern 4: Responsive Classes

```tsx
<div className="w-full md:w-1/2 lg:w-1/3">
  {/* Responsive layout */}
</div>
```

---

## Component Communication

### State Flow

1. **User Action**: Click button, type message, etc.
2. **Component Handler**: onClick, onChange, etc.
3. **Store Update**: Call Zustand setter (e.g., `addMessage()`)
4. **Store Broadcast**: Zustand notifies all subscribed components
5. **Component Re-render**: Component receives new state
6. **UI Update**: DOM reflects new state

### Example: Sending a Message

```typescript
// 1. User types and clicks send
handleSendMessage()
  ↓
// 2. Add user message to store
addMessage({ role: 'user', content: input, timestamp: new Date() })
  ↓
// 3. Zustand updates messages array
  ↓
// 4. CenterPanel subscribed to messages, re-renders
  ↓
// 5. New message appears in chat
// 6. Simulate AI response with setTimeout
  ↓
// 7. Add agent message via addMessage()
  ↓
// 8. Send itinerary if generated
setItinerary(mockItinerary)
  ↓
// 9. ItineraryCard renders below chat
```

---

## Props & TypeScript

### Props Documentation Standards

All components should document props:

```tsx
interface ComponentProps {
  /** Description of prop */
  propName: string
  
  /** Whether component is loading */
  isLoading?: boolean
}

export const Component: React.FC<ComponentProps> = ({ propName, isLoading = false }) => {
  // Component implementation
}
```

---

## Best Practices

1. **Use `cn()` for class merging** to avoid Tailwind conflicts
2. **Store subscriptions**: Use selector functions to prevent unnecessary re-renders
3. **Use `'use client'` directive** for interactive components
4. **Memoize expensive renders**: Consider React.memo for non-updating components
5. **Type all props**: Leverage TypeScript for type safety
6. **Use semantic HTML**: Good accessibility practices
7. **Consistent naming**: camelCase for functions, PascalCase for components
8. **Icon sizing**: Use `size` prop consistently across components
9. **Color themes**: Always use custom color tokens, not hardcoded colors
10. **Animations**: Use predefined animation classes for consistency

---

## Future Component Ideas

- `PreferenceModal` - Edit preferences in detail
- `MessageInput` - Separated input component
- `ChatHeader` - Extracted header logic
- `ErrorBoundary` - Graceful error handling
- `LoadingSpinner` - Loading state indicator
- `Toast` - Notification system
- `Modal` - Generic modal dialog
- `Dropdown` - Reusable dropdown menu
- `SearchBox` - Search functionality
- `Pagination` - For large lists

