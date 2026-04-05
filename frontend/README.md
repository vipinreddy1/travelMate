# TripMind Frontend

A premium, modern travel AI assistant web app built with Next.js, React, and Tailwind CSS.

## Overview

TripMind is an intelligent travel companion that helps users plan trips using memories from past trips and friends' experiences. The frontend provides a beautiful 3-panel interface for real-time trip planning with voice interaction and an editorial-style blog post page for sharing travel experiences.

## Features

### Page 1 — Main App (`/`)
- **3-Panel Layout**
  - **Left Panel**: Live preferences that update in real-time as you chat
  - **Center Panel**: AI chat interface with itinerary generation
  - **Right Panel**: Past trips memory and friends' experiences

- **Real-time Features**
  - Live preference updates with smooth animations
  - Chat interface with typing indicators
  - Voice input/output ready (ElevenLabs integration)
  - Beautiful itinerary cards with expandable day-by-day plans

### Page 2 — Blog Post (`/trip/:id`)
- Editorial-style layout inspired by Medium
- Full-width hero image with gradient overlay
- Author information and trip metadata
- Day-by-day content with photo grids
- Call-to-action for planning similar trips
- Sticky table of contents for navigation

## Design System

### Colors
- **Base**: Warm whites and off-whites (`#fafaf8`, `#f5f3f0`)
- **Text**: Deep charcoal (`#1a1a2e`, `#6b6b7f`)
- **Accent**: Rich teal (`#0d7377`) and ocean blue (`#084c61`)
- **Functional**: Success (`#10b981`), Warning (`#f59e0b`), Error (`#ef4444`)

### Typography
- **UI Font**: Inter (sans-serif)
- **Blog Font**: Lora (serif for editorial warmth)
- **Font Sizes**: Carefully tuned for readability and hierarchy

### Components
- Soft shadows and generous spacing
- Medium border radius (10-12px)
- Smooth animations and transitions
- Responsive design (1280px+ primary, tablet graceful collapse)

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Server State**: TanStack Query (React Query)
- **Icons**: Custom SVGs + Lucide React
- **Images**: Next/Image for optimization
- **UI Patterns**: Micro-interactions and smooth animations

## Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open browser to http://localhost:3000
```

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                      # Next.js app directory
│   ├── page.tsx             # Home page (Page 1)
│   ├── trip/[id]/          # Blog post page (Page 2)
│   ├── layout.tsx           # Root layout
│   └── globals.css          # Global styles
├── components/              # Reusable React components
│   ├── LeftPanel.tsx        # Preferences panel
│   ├── CenterPanel.tsx      # Chat & itinerary panel
│   ├── RightPanel.tsx       # Trip memory panel
│   ├── ItineraryCard.tsx    # Itinerary display card
│   ├── BlogPostPage.tsx     # Blog post layout
│   └── Icons.tsx            # SVG icon components
├── store/                   # Zustand state management
│   └── appStore.ts          # App-wide state
├── lib/                     # Utility functions
│   └── utils.ts             # Helper functions
├── hooks/                   # Custom React hooks
├── tailwind.config.ts       # Tailwind CSS config
├── tsconfig.json            # TypeScript config
└── package.json             # Dependencies
```

## Key Components

### LeftPanel
Displays user preferences that update in real-time during chat. Features smooth animations when preferences change.

### CenterPanel
Contains:
- Chat interface with message history
- AI agent messages with typing indicators
- Itinerary card with flight, hotel, and day-by-day activities
- Voice and text input area
- Preference update feedback

### RightPanel
Tabs for "My Trips" and "Friends' Trips",showing:
- Destination thumbnail images
- Trip metadata (dates, status)
- Friend avatars for shared trips
- Hover effects and animations

### ItineraryCard
Displays the generated trip plan with:
- Hero image of destination
- Flight information and pricing
- Hotel details and ratings
- Expandable day-by-day activities with times, locations, and descriptions

### BlogPostPage
Editorial-style trip blog with:
- Full-width hero image
- Author information
- Day-by-day content sections
- Photo grids after each day
- Sticky table of contents
- CTA to plan similar trips

## State Management (Zustand)

The `appStore` manages:
- **preferences**: Array of user preferences with update tracking
- **messages**: Chat message history with roles (user/agent)
- **itinerary**: Generated trip itinerary data
- **isRecording**: Voice recording state
- **updatePreference**: Update a specific preference
- **addMessage**: Add message to chat
- **setItinerary**: Store generated itinerary

## Styling Approach

Uses Tailwind CSS with:
- Custom color palette defined in `tailwind.config.ts`
- Custom animations (`pulse-soft`, `fade-in`, `slide-up`, `highlight`)
- Component-level utilities in `globals.css`
- Responsive design with mobile-first approach

## Micro-interactions

- **Preference updates**: Yellow-green highlight flash animation
- **Message entry**: Slide-up fade-in animation
- **Trip card hover**: Gentle lift and border color change
- **Mic button**: Glow effect when recording
- **Typing indicator**: Three animated dots
- **Itinerary expansion**: Smooth chevron rotation

## API Integration Points

When connecting to backend:
- `POST /chat`: Send user messages to agent
- `GET /trips`: Fetch user and friends' trips
- `GET /trip/:id`: Get blog post content
- `SSE /preferences`: Real-time preference updates
- `ElevenLabs STT/TTS`: Voice input and output

## Future Enhancements

- [ ] Implement ElevenLabs voice integration
- [ ] Connect to Auth0 for authentication
- [ ] Real backend API integration
- [ ] PWA support
- [ ] Dark mode
- [ ] Mobile app (React Native)
- [ ] Photo upload for trips
- [ ] Trip collaboration features

## Development Notes

- Preferences animate when updated via `pref-update` class
- Messages use intersection observer for lazy loading in production
- Itinerary card is positioned relative to chat for scrolling context
- Blog post uses sticky positioning for table of contents
- All images are optimized with Next/Image
- SVG icons are bundled for tree-shaking

## License

MIT

## Support

For questions or issues, please open a GitHub issue or contact the team.
