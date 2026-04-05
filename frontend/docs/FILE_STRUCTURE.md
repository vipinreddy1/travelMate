# TripMind Frontend — File Structure & Organization

## Project Directory Tree

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout (metadata, fonts, global styles)
│   ├── page.tsx                 # Main app page (/ route)
│   ├── globals.css              # Global CSS with custom utilities
│   ├── trip/
│   │   └── [id]/
│   │       └── page.tsx         # Trip detail page (/trip/:id)
│   └── head.tsx                 # (optional) Custom head
│
├── components/                   # React components
│   ├── LeftPanel.tsx            # Left sidebar with preferences
│   ├── CenterPanel.tsx          # Center chat interface
│   ├── RightPanel.tsx           # Right sidebar with trip memory
│   ├── ItineraryCard.tsx        # Itinerary display card
│   ├── BlogPostPage.tsx         # Editorial blog layout
│   └── Icons.tsx                # SVG icon components
│
├── store/                        # State management
│   └── appStore.ts              # Zustand store (preferences, messages, itinerary, UI state)
│
├── lib/                          # Utilities and helpers
│   └── utils.ts                 # Formatting functions, cn() class merger
│
├── data/                         # Static data and content
│   └── blogs/                   # Blog post content files
│       ├── japan.txt            # Japan blog content
│       ├── vegas.txt            # Vegas blog content
│       └── vermount.txt         # Vermont blog content
│
├── images/                       # Image assets
│   ├── posters/                 # Hero image posters
│   └── themes/                  # Theme-specific images
│
├── docs/                         # Documentation
│   ├── DESIGN_SYSTEM.md         # Design tokens and visual language
│   ├── DEVELOPMENT.md           # Architecture and dev guide
│   ├── GETTING_STARTED.md       # Setup and installation
│   ├── ERROR_RESOLUTION.md      # Known issues and fixes
│   ├── ARCHITECTURE.md          # System architecture (NEW)
│   ├── COMPONENTS.md            # Component documentation (NEW)
│   ├── STATE_MANAGEMENT.md      # Zustand store guide (NEW)
│   ├── STYLING_GUIDE.md         # Tailwind and CSS guide (NEW)
│   └── FILE_STRUCTURE.md        # This file
│
├── public/                       # Static public assets
│   └── (files served at root)
│
├── node_modules/                # Dependencies (generated)
│
├── .eslintrc.json               # ESLint configuration
├── .gitignore                   # Git ignore rules
├── .next/                       # Next.js build output (generated)
├── next.config.js               # Next.js configuration
├── package.json                 # Project dependencies
├── package-lock.json            # Locked versions
├── postcss.config.js            # PostCSS configuration (for Tailwind)
├── README.md                    # Project overview
├── tailwind.config.ts           # Tailwind CSS configuration
├── tsconfig.json                # TypeScript configuration
└── next-env.d.ts               # Next.js TypeScript definitions
```

---

## Detailed Directory Descriptions

### `/app` - Next.js App Router

The app router controls all routing in the application.

```
app/
├── layout.tsx
│   ├── Purpose: Root layout wrapper for entire app
│   ├── Exports: RootLayout component
│   ├── Sets: Metadata, viewport, fonts
│   ├── Wraps: All page content
│   └── Contains: <html>, <head>, <body> tags
│
├── page.tsx
│   ├── Purpose: Main application page at / route
│   ├── Layout: 3-panel fixed layout (LeftPanel, CenterPanel, RightPanel)
│   ├── Features: Chat interface, preferences, trip memory
│   └── Uses: Zustand store
│
├── globals.css
│   ├── Purpose: Global styles for entire application
│   ├── Contains: Tailwind directives, custom utilities, animations
│   ├── Imports: Google Fonts (Inter, Lora)
│   └── Defines: Scrollbar styling, custom classes
│
└── trip/[id]/
    └── page.tsx
        ├── Purpose: Dynamic route for trip detail pages
        ├── Parameter: id (trip ID)
        ├── Layout: Full-width editorial blog layout
        └── Component: BlogPostPage
```

---

### `/components` - React Components

All reusable React components.

```
components/
├── LeftPanel.tsx
│   ├── Type: Functional component
│   ├── Directive: 'use client'
│   ├── Props: None (uses Zustand)
│   ├── Purpose: Display user travel preferences
│   ├── Features:
│   │   ├── Preference list with icons
│   │   ├── Live update animations
│   │   ├── Pulse indicator
│   │   └── Fixed 220px width sidebar
│   ├── Exports: Named export LeftPanel
│   └── Dependencies: useAppStore, cn(), Icons
│
├── CenterPanel.tsx
│   ├── Type: Functional component
│   ├── Directive: 'use client'
│   ├── Props: None (uses Zustand)
│   ├── Purpose: Main chat interface
│   ├── Features:
│   │   ├── Message list with auto-scroll
│   │   ├── User/agent message rendering
│   │   ├── Text input with send button
│   │   ├── Mic button for voice (ready)
│   │   ├── Itinerary card rendering
│   │   └── Typing indicator animation
│   ├── Exports: Named export CenterPanel
│   └── Dependencies: Icons, ItineraryCard, useAppStore
│
├── RightPanel.tsx
│   ├── Type: Functional component
│   ├── Directive: 'use client'
│   ├── Props: None (uses local state)
│   ├── Purpose: Trip memory and history
│   ├── Features:
│   │   ├── Tab navigation (My Trips / Friends)
│   │   ├── Trip card list with images
│   │   ├── Status badges
│   │   ├── Hover animations
│   │   └── Friend avatars
│   ├── Exports: Named export RightPanel
│   └── Dependencies: Image, Icons, cn()
│
├── ItineraryCard.tsx
│   ├── Type: Functional component
│   ├── Directive: 'use client'
│   ├── Props: { itinerary: Itinerary }
│   ├── Purpose: Display generated travel itinerary
│   ├── Features:
│   │   ├── Hero image with gradient
│   │   ├── Flight/hotel details grid
│   │   ├── Collapsible day sections
│   │   ├── Activity timeline per day
│   │   ├── Star ratings
│   │   └── Animations on generation
│   ├── Exports: Named export ItineraryCard
│   └── Dependencies: Image, Icons, formatDate, cn()
│
├── BlogPostPage.tsx
│   ├── Type: Functional component
│   ├── Directive: 'use client'
│   ├── Props: { params: { id: string } }
│   ├── Purpose: Editorial blog post layout
│   ├── Features:
│   │   ├── Full-width hero section
│   │   ├── Sticky metadata header
│   │   ├── Day-by-day content sections
│   │   ├── Photo galleries (3 columns)
│   │   ├── Table of contents
│   │   ├── Author information
│   │   └── CTA buttons
│   ├── Exports: Named export BlogPostPage
│   └── Dependencies: Image, Link, Icons, formatDate, cn()
│
└── Icons.tsx
    ├── Type: Collection of icon components
    ├── Directive: 'use client'
    ├── Props: IconProps interface (size, className)
    ├── Purpose: SVG icons used throughout app
    ├── Icons Exported:
    │   ├── CompassIcon - Logo, branding
    │   ├── SparkleIcon - Travel DNA
    │   ├── MapPinIcon - Location indicators
    │   ├── MicIcon - Voice input
    │   ├── SendIcon - Message send
    │   ├── BrainIcon - Trip memory
    │   ├── StarIcon - Ratings
    │   ├── ChevronDownIcon - Expand/collapse
    │   ├── ArrowRightIcon - Navigation
    │   ├── PlaneIcon - Flights
    │   ├── HotelIcon - Accommodation
    │   ├── CalendarIcon - Dates
    │   └── UserIcon - Profile
    ├── Export: All as named exports
    └── Dependencies: React.SVGProps, cn()
```

---

### `/store` - State Management

Zustand store definitions.

```
store/
└── appStore.ts
    ├── Purpose: Centralized application state
    ├── Store: useAppStore (Zustand hook)
    ├── Sections:
    │   ├── Preferences state and actions
    │   ├── Messages state and actions
    │   ├── Itinerary state and actions
    │   └── UI state and actions
    ├── Exports: Named export useAppStore
    ├── Interfaces:
    │   ├── Preference
    │   ├── Message
    │   ├── Itinerary
    │   └── AppStore
    └── Dependencies: zustand
```

---

### `/lib` - Utility Functions

Shared utility functions and helpers.

```
lib/
└── utils.ts
    ├── Purpose: Shared utility functions
    ├── Functions:
    │   ├── cn() - Class name merging with Tailwind
    │   ├── formatDate() - Convert date to readable format
    │   ├── formatTime() - Convert time to 12-hour format
    │   └── truncateText() - Truncate text with ellipsis
    ├── Exports: All as named exports
    └── Dependencies: clsx, tailwind-merge
```

---

### `/data` - Static Data

Static content and blog data.

```
data/
└── blogs/
    ├── japan.txt
    │   └── Japan trip blog content
    ├── vegas.txt
    │   └── Las Vegas trip blog content
    └── vermount.txt
        └── Vermont trip blog content

Note: In production, this data would load from database
rather than static text files.
```

---

### `/images` - Image Assets

Organized image assets.

```
images/
├── posters/
│   └── (Hero image posters for blog posts)
└── themes/
    └── (Theme-specific images and backgrounds)

Note: Current implementation uses Unsplash URLs instead
of local image files. Consider storing hero images locally
for better performance and control.
```

---

### `/docs` - Documentation

Comprehensive documentation for the project.

```
docs/
├── GETTING_STARTED.md
│   ├── Installation steps
│   ├── Development server setup
│   ├── Project structure overview
│   ├── Build commands
│   └── Troubleshooting
│
├── DESIGN_SYSTEM.md
│   ├── Design philosophy
│   ├── Color palette
│   ├── Typography system
│   ├── Component specifications
│   └── Visual language
│
├── DEVELOPMENT.md
│   ├── Architecture overview
│   ├── 3-panel layout system
│   ├── Component tree
│   ├── Code examples
│   └── Development workflow
│
├── ERROR_RESOLUTION.md
│   ├── Fixed issues and solutions
│   ├── Known bugs
│   ├── Troubleshooting guide
│   └── Setup validation
│
├── ARCHITECTURE.md (NEW)
│   ├── High-level system design
│   ├── Data flow and state management
│   ├── Page routes
│   ├── Key features documentation
│   └── Performance considerations
│
├── COMPONENTS.md (NEW)
│   ├── Component overview table
│   ├── Detailed component documentation
│   ├── Component composition patterns
│   ├── Props and TypeScript
│   └── Best practices
│
├── STATE_MANAGEMENT.md (NEW)
│   ├── Zustand store guide
│   ├── State sections documentation
│   ├── Store creation and usage
│   ├── Data flow examples
│   └── Performance tips
│
├── STYLING_GUIDE.md (NEW)
│   ├── Tailwind CSS configuration
│   ├── Color palette system
│   ├── Typography guide
│   ├── Animation documentation
│   └── Component styling patterns
│
└── FILE_STRUCTURE.md (NEW)
    └── This file - project organization guide
```

---

### Root Configuration Files

```
.eslintrc.json
├── Purpose: ESLint configuration
├── Extends: Next.js recommended rules
└── Settings: Code quality rules

next.config.js
├── Purpose: Next.js configuration
├── Settings: Build optimizations, redirects
└── Plugins: Custom webpack loaders

tailwind.config.ts
├── Purpose: Tailwind CSS configuration
├── Contains: Custom colors, spacing, animations
└── Exports: Config object

tsconfig.json
├── Purpose: TypeScript configuration
├── Contains: Compiler options, path aliases
├── Aliases:
│   ├── @/* → ./*
│   ├── @/components/* → ./components/*
│   ├── @/app/* → ./app/*
│   ├── @/lib/* → ./lib/*
│   ├── @/store/* → ./store/*
│   ├── @/hooks/* → ./hooks/*
│   └── @/pages/* → ./pages/*
└── Remember: Restart TS server after changes

package.json
├── Purpose: Project metadata and dependencies
├── Scripts:
│   ├── dev - Development server
│   ├── build - Production build
│   ├── start - Run production build
│   └── lint - Run linter
├── Dependencies: React, Next, Zustand, etc.
└── DevDependencies: TypeScript, Tailwind, ESLint, etc.

postcss.config.js
├── Purpose: PostCSS configuration
├── Plugins: Tailwind CSS, Autoprefixer
└── For: CSS processing pipeline

README.md
├── Purpose: Project overview
├── Contains: Features, tech stack, setup guide
└── For: New developers

.gitignore
├── Purpose: Git ignore rules
├── Ignores: node_modules, .next, .env
└── Maintains: Clean repository

next-env.d.ts
├── Purpose: Next.js TypeScript definitions
├── Generated: Automatically by Next.js
└── Don't: Edit manually
```

---

## Path Aliases

Configure path aliases in `tsconfig.json` for easier imports:

```typescript
// Instead of:
import { cn } from '../../../lib/utils'
import { LeftPanel } from '../components/LeftPanel'

// Use:
import { cn } from '@/lib/utils'
import { LeftPanel } from '@/components/LeftPanel'
```

**Available Aliases**:
- `@/*` - Root directory
- `@/components/*` - Components folder
- `@/app/*` - App folder
- `@/lib/*` - Lib folder
- `@/store/*` - Store folder
- `@/hooks/*` - Custom hooks (future)
- `@/pages/*` - Pages (legacy, if used)

---

## Adding New Features

### New Component

```
1. Create file in components/ComponentName.tsx
2. Define TypeScript interface if needed
3. Add 'use client' directive
4. Export as named export
5. Document in COMPONENTS.md
```

### New Page Route

```
1. Create folder in app/route-name/
2. Create page.tsx inside folder
3. Add layout if needed
4. Configure in next.config.js if needed
5. Document in ARCHITECTURE.md
```

### New Utility Function

```
1. Add to lib/utils.ts
2. Export as named export
3. Document usage and examples
4. Add TypeScript types
```

### New State Slice

```
1. Define interfaces in appStore.ts
2. Add state section
3. Add actions
4. Export from store
5. Document in STATE_MANAGEMENT.md
```

---

## File Naming Conventions

- **Components**: PascalCase (e.g., `LeftPanel.tsx`)
- **Functions**: camelCase (e.g., `formatDate()`)
- **Types/Interfaces**: PascalCase (e.g., `Preference`, `Message`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)
- **Folders**: kebab-case or camelCase depending on context

---

## Import Organization

Maintain consistent import order:

```typescript
// 1. React and Next.js
import { useState, useRef } from 'react'
import Image from 'next/image'
import Link from 'next/link'

// 2. External libraries
import { cn } from 'clsx'

// 3. Internal imports
import { useAppStore } from '@/store/appStore'
import { formatDate } from '@/lib/utils'
import { LeftPanel } from '@/components/LeftPanel'

// 4. Type imports
import type { Itinerary } from '@/store/appStore'
```

---

## Module Dependencies Map

```
layout.tsx
  ├── globals.css
  └── RootLayout

page.tsx
  ├── LeftPanel
  ├── CenterPanel
  │   ├── Icons
  │   └── ItineraryCard
  └── RightPanel

trip/[id]/page.tsx
  └── BlogPostPage
      ├── Image
      ├── Link
      ├── Icons
      └── formatDate()

appStore.ts
  └── zustand (no dependencies)

utils.ts
  ├── clsx
  └── tailwind-merge

components/*
  └── May import from:
      ├── appStore
      ├── utils
      ├── Icons
      └── Other components (avoid circular)

lib/utils.ts
  ├── clsx
  └── tailwind-merge
```

---

## Best Practices

1. **Keep components small**: One responsibility per component
2. **Use path aliases**: Never use relative paths like `../../../`
3. **Organize by feature**: Group related files together
4. **Document public APIs**: Comment component props and exports
5. **Avoid circular dependencies**: Carefully plan imports
6. **Type all exports**: TypeScript interfaces for all data
7. **Pure functions in lib**: Keep utils side-effect free
8. **Keep store focused**: Don't bloat store with UI state
9. **Lazy load heavy components**: Use dynamic imports for large components
10. **Delete unused files**: Keep codebase tidy

---

## Future Enhancements

### Potential New Folders

- `/hooks` - Custom React hooks
- `/utils` - Additional utility categories
- `/constants` - Application constants
- `/types` - Shared TypeScript types
- `/services` - API service layer
- `/contexts` - React Context definitions (if needed)
- `/middleware` - Custom middleware functions

### Scale Considerations

As project grows, consider:
- Breaking components into smaller subfunctional folders
- Creating a components library
- Separating business logic from UI components
- Implementing proper service layer for API calls
- Setting up proper API client wrapper

