# TripMind Frontend — Styling Guide & Tailwind System

## Tailwind CSS Configuration

TripMind uses **Tailwind CSS 3.4** with extensive custom extensions for a cohesive, premium design system.

**Config Location**: `tailwind.config.ts`

---

## Custom Color Palette

### Base Colors

| Color | Hex | Usage | Tailwind Class |
|-------|-----|-------|-----------------|
| Warm White | #fafaf8 | Main background, breathing room | `bg-warm-white` |
| Off-White | #f5f3f0 | Card backgrounds, secondary surfaces | `bg-off-white` |
| Cream | #fffbf7 | Subtle highlights, hover states | `bg-cream` |

### Text Colors

| Color | Hex | Usage | Tailwind Class |
|-------|-----|-------|-----------------|
| Text Primary | #1a1a2e | Main body text, headlines | `text-text-primary` |
| Text Secondary | #6b6b7f | Labels, secondary info | `text-text-secondary` |
| Text Muted | #9a9aaa | Disabled state, placeholders | `text-text-muted` |

### Accent Colors

| Color | Hex | Usage | Tailwind Class |
|-------|-----|-------|-----------------|
| Rich Teal ⭐ | #0d7377 | Primary accent, buttons, links | `text-teal` `bg-teal` |
| Teal Light | #14919b | Hover state for teal elements | `text-teal-light` `hover:bg-teal-light` |
| Teal Lighter | #3fb9cf | Subtle accents, backgrounds | `text-teal-lighter` |
| Ocean Blue | #084c61 | Alternative accent, dark highlights | `text-ocean` |

### Functional Colors

| Color | Hex | Usage | Tailwind Class |
|-------|-----|-------|-----------------|
| Success Green | #10b981 | "Completed" status badges | `text-success` `bg-success` |
| Warning Amber | #f59e0b | Alerts, pending states | `text-warning` `bg-warning` |
| Error Red | #ef4444 | Error states, destructive actions | `text-error` `bg-error` |
| Error Light | #fee2e2 | Error backgrounds | `bg-error-light` |

### Color Usage Rules

1. **Never use pure black** (#000000) — always use `text-primary`
2. **Text on teal background** = pure white (high contrast requirement)
3. **Teal hover state** = `#14919b` (teal-light)
4. **Disabled text** = reduce opacity by 50% or use `text-muted`
5. **Shadows** = always use `text-primary` with low opacity

---

## Typography System

### Font Stack

**UI Font (Default)**:
```css
'Inter', system-ui, sans-serif
```

**Font Weights**:
- 300: Light (sparingly for large headings)
- 400: Regular (body text)
- 500: Medium (UI labels, captions)
- 600: Semibold (subheadings, button text)
- 700: Bold (strong emphasis)

**Blog Font**:
```css
'Lora', serif
```

- Used for editorial content
- Adds warmth and elegance
- Serif adds antiquity feel

### Font Sizes (Custom)

| Size | CSS | Usage |
|------|-----|-------|
| `text-xs` | 12px / 16px | Labels, captions, small UI |
| `text-sm` | 14px / 20px | Body text, button labels |
| `text-base` | 16px / 24px | Default body, small headings |
| `text-lg` | 18px / 28px | Subheadings, prominent text |
| `text-xl` | 20px / 28px | Section headings |
| `text-2xl` | 24px / 32px | Page titles |
| `text-3xl` | 30px / 36px | Main headings |
| `text-4xl` | 36px / 44px | Hero headings |

### Font Usage

```tsx
// Headline (semibold, large)
<h1 className="text-3xl font-semibold">Tokyo Trip</h1>

// Body text (regular, medium)
<p className="text-base font-normal">Travel description...</p>

// Label (small, semibold)
<label className="text-xs font-semibold uppercase">Budget</label>

// Blog content (serif, large)
<article className="text-lg font-serif">Opening paragraph...</article>
```

---

## Spacing System

Consistent 4px base unit scaling:

```
1   = 4px
2   = 8px
3   = 12px
4   = 16px
5   = 20px
6   = 24px
8   = 32px
10  = 40px
12  = 48px
16  = 64px
20  = 80px
24  = 96px
```

### Usage

```tsx
// Padding
<div className="p-4">Content</div>          // 16px padding all sides
<div className="px-6 py-4">Content</div>    // 24px horizontal, 16px vertical

// Margin
<div className="mb-8">Content</div>         // 32px margin bottom
<div className="mt-2">Content</div>         // 8px margin top

// Gap
<div className="flex gap-4">Items</div>     // 16px gap between flex items
```

---

## Border Radius

Soft, rounded corners (no hard angles):

```
sm   = 8px      // Inputs, badges, small buttons
md   = 10px     // Cards, modals (recommended)
lg   = 12px     // Large cards, panels
xl   = 16px     // Hero sections, large containers
2xl  = 20px     // Rare, very large elements
full = 9999px   // Perfect circles, full-radius pills
```

### Usage

```tsx
// Card
<div className="rounded-lg bg-white">Card</div>

// Pill button
<button className="rounded-full px-4 py-2">Button</button>

// Input
<input className="rounded-md border border-gray-100" />

// Badge
<span className="rounded-md bg-teal px-2 py-1">Badge</span>
```

---

## Shadow System

5 levels of shadows (soft, premium feel):

```
xs   = 0 1px 2px 0 rgba(26, 26, 46, 0.05)
       Single pixel depth

sm   = 0 1px 3px 0 rgba(26, 26, 46, 0.1), 0 1px 2px 0 rgba(26, 26, 46, 0.06)
       Subtle depth, used for UI elements

md   = 0 4px 6px -1px rgba(26, 26, 46, 0.1), 0 2px 4px -1px rgba(26, 26, 46, 0.06)
       Standard elevation, used for cards

lg   = 0 10px 15px -3px rgba(26, 26, 46, 0.1), 0 4px 6px -2px rgba(26, 26, 46, 0.05)
       Prominent depth, for highlighted cards

xl   = 0 20px 25px -5px rgba(26, 26, 46, 0.1), 0 10px 10px -5px rgba(26, 26, 46, 0.04)
       Maximum depth, for modals and overlays
```

**Color Basis**: Always uses `text-primary` with opacity to maintain visual coherence.

### Usage

```tsx
// Card with subtle shadow
<div className="shadow-md rounded-lg">Card</div>

// Lifted button on hover
<button className="shadow-sm hover:shadow-md transition-shadow">Button</button>

// Modal with prominent shadow
<div className="shadow-xl rounded-lg">Modal</div>
```

---

## Animation & Keyframes

### Defined Animations

#### pulse-soft
```css
@keyframes pulse-soft {
  0%, 100% { opacity: 1 }
  50%      { opacity: 0.5 }
}
```
**Duration**: 2s infinite
**Usage**: Gentle pulsing indicator (e.g., "Updating as you chat...")

#### fade-in
```css
@keyframes fade-in {
  0%   { opacity: 0 }
  100% { opacity: 1 }
}
```
**Duration**: 0.3s ease-in-out
**Usage**: Element appears smoothly

#### slide-up
```css
@keyframes slide-up {
  0%   { transform: translateY(10px); opacity: 0 }
  100% { transform: translateY(0);    opacity: 1 }
}
```
**Duration**: 0.3s ease-out
**Usage**: Element slides up from bottom (messages, cards)

#### highlight
```css
@keyframes highlight {
  0%   { backgroundColor: rgba(13, 115, 119, 0) }
  50%  { backgroundColor: rgba(13, 115, 119, 0.1) }
  100% { backgroundColor: rgba(13, 115, 119, 0) }
}
```
**Duration**: 1s ease-in-out
**Usage**: Teal flash background (preference updates)

#### typing
```css
@keyframes typing {
  0%, 60%, 100% { opacity: 0.3 }
  30%           { opacity: 1 }
}
```
**Duration**: 0.6s infinite
**Usage**: Typing dots animation

### Animation Classes

```tsx
// Fade in element
<div className="animate-fade-in">Content</div>

// Slide up animation
<div className="animate-slide-up">Message</div>

// Pulse softly
<span className="animate-pulse-soft">Updating...</span>

// Highlight effect
<div className="animate-highlight">Updated preference</div>

// Typing dots
<div className="flex gap-1">
  <div className="animate-typing bg-teal w-2 h-2 rounded-full" />
  <div className="animate-typing bg-teal w-2 h-2 rounded-full" style={{ animationDelay: '0.1s' }} />
  <div className="animate-typing bg-teal w-2 h-2 rounded-full" style={{ animationDelay: '0.2s' }} />
</div>
```

---

## Global Styles

**Location**: `app/globals.css`

### HTML & Body

```css
html {
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  @apply bg-warm-white text-text-primary;
}
```

### Custom Utility Classes

#### .flex-center
```css
.flex-center {
  @apply flex items-center justify-center;
}
```
**Usage**: Center content flexbox

#### .transition-smooth
```css
.transition-smooth {
  @apply transition-all duration-300 ease-out;
}
```
**Usage**: Smooth transition for all properties

### Scrollbar Styling

```css
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgb(26, 26, 46, 0.2);  /* text-primary 20% */
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgb(26, 26, 46, 0.3);  /* text-primary 30% */
}
```

**Effect**: Thin, subtle scrollbars that match design system

### Message Animations

```css
.message-enter {
  animation: slide-up 0.3s ease-out;
}

.pref-update {
  animation: highlight 1s ease-in-out;
}
```

### Typing Dots

```css
.typing-dots {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #0d7377;  /* teal */
  animation: typing 0.6s ease-in-out infinite;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.1s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.2s;
}
```

---

## Component Styling Patterns

### Button Styling

```tsx
// Primary button (teal)
<button className="px-4 py-2 bg-teal text-white rounded-md font-semibold hover:bg-teal-light transition-colors">
  Send
</button>

// Secondary button (outline)
<button className="px-4 py-2 border border-gray-100 text-text-primary rounded-md hover:bg-off-white transition-colors">
  Cancel
</button>

// Pill button (full radius)
<button className="px-4 py-2 rounded-full bg-teal text-white hover:bg-teal-light">
  Action
</button>

// Icon button
<button className="p-2 hover:bg-off-white rounded-md text-text-secondary hover:text-text-primary transition-colors">
  <MicIcon size={24} />
</button>
```

### Card Styling

```tsx
// Standard card
<div className="bg-white rounded-lg shadow-md border border-gray-100 p-6">
  {/* Content */}
</div>

// Hover elevated card
<div className="bg-white rounded-lg shadow-sm hover:shadow-lg transition-shadow border border-gray-100 p-6">
  {/* Content */}
</div>

// Accent card
<div className="bg-off-white rounded-lg border border-teal/20 p-6">
  {/* Content */}
</div>
```

### Input Styling

```tsx
// Text input
<input
  type="text"
  placeholder="Type message..."
  className="w-full px-4 py-2 rounded-md border border-gray-100 bg-white text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-teal/20"
/>

// Label
<label className="text-xs font-semibold text-text-muted uppercase tracking-wide">
  Budget
</label>
```

### Badge Styling

```tsx
// Teal badge
<span className="px-3 py-1 rounded-full bg-teal bg-opacity-10 text-teal text-xs font-semibold">
  Completed
</span>

// Status badge
<span className="px-3 py-1 rounded-full bg-success bg-opacity-10 text-success text-xs font-semibold">
  Ongoing
</span>

// Warning badge
<span className="px-3 py-1 rounded-full bg-warning bg-opacity-10 text-warning text-xs font-semibold">
  Pending
</span>
```

---

## Responsive Design

### Breakpoints

```
sm   = 640px   (rarely used)
md   = 768px   (tablets)
lg   = 1024px  (desktops)
xl   = 1280px  (large desktops)
2xl  = 1536px  (ultra-wide)
```

### Usage

```tsx
// Show on desktop, hide on tablet
<div className="hidden lg:block">
  {/* Desktop only content */}
</div>

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive columns */}
</div>

// Responsive padding
<div className="p-4 md:p-6 lg:p-8">
  {/* Dynamic padding */}
</div>
```

### TripMind Responsive Strategy

1. **Primary Layout**: 1280px+ (full 3-panel layout)
2. **Tablet**: 768px-1279px (2-panel, side collapse)
3. **Mobile**: Below 768px (single panel, stacked)

---

## Design Tokens Export

For Design System documentation, reference these in your design tool:

```json
{
  "colors": {
    "warm-white": "#fafaf8",
    "off-white": "#f5f3f0",
    "cream": "#fffbf7",
    "teal": "#0d7377",
    "text-primary": "#1a1a2e"
  },
  "typography": {
    "fontFamily": {
      "ui": "Inter",
      "editorial": "Lora"
    }
  },
  "spacing": {
    "base": "4px"
  },
  "borderRadius": {
    "sm": "8px",
    "md": "10px",
    "lg": "12px"
  }
}
```

---

## Best Practices

1. ✅ Always use custom color tokens, never hardcode colors
2. ✅ Use `cn()` utility for class merging
3. ✅ Apply spacing consistently (4px base unit)
4. ✅ Use shadows for elevation hierarchy
5. ✅ Prefer `transition-smooth` class over custom transitions
6. ✅ Use animations sparingly for premium feel
7. ✅ Maintain high contrast ratios for accessibility (WCAG AAA)
8. ❌ Don't use pure black (#000000)
9. ❌ Don't create new colors outside the palette
10. ❌ Don't override Tailwind config without documentation

---

## Theming (Future Enhancement)

Implement dark mode:

```typescript
// tailwind.config.ts
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          // Dark mode color palette
        }
      }
    }
  }
}
```

```tsx
// Usage
<html className="dark">
  <body className="bg-warm-white dark:bg-slate-900">
    {/* Content */}
  </body>
</html>
```

---

## Accessibility Considerations

1. **Color Contrast**: All text meets WCAG AAA standards
2. **Focus States**: Visible focus rings on interactive elements
3. **Font Size**: Minimum 12px for readability
4. **Line Height**: Minimum 1.3 for body text
5. **Spacing**: Sufficient spacing for touch targets (min 44px)

