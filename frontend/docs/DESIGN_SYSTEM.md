# TripMind — Design System & Visual Language

## Design Philosophy

TripMind's design reflects "your intelligent travel companion" — **trustworthy, calm, sophisticated**. 

Inspired by:
- **Airbnb**: Warm, human-centered, aspirational
- **Linear**: Clean, minimal, purposeful
- **Medium**: Editorial elegance with generous whitespace

**Anti-goals**: Not flashy, not corporate, not kitschy.

---

## Color Palette

### Primary Colors

```
Warm White (#fafaf8)
├─ Background for main UI
└─ Breathing room and warmth

Off-White (#f5f3f0)
├─ Card backgrounds
└─ Secondary surfaces

Cream (#fffbf7)
├─ Subtle highlights
└─ Hover states

Rich Teal (#0d7377) ⭐ PRIMARY ACCENT
├─ Buttons
├─ Links
├─ Icons
├─ Accent highlights
└─ Creates premium feel

Teal Light (#14919b)
├─ Hover state for buttons
└─ Secondary accent

Deep Ocean (#084c61)
├─ Alternative accent
├─ Logo background
└─ Dark highlights

Text Primary (#1a1a2e)
├─ Main body text
└─ Headlines

Text Secondary (#6b6b7f)
├─ Labels
└─ Secondary information

Text Muted (#9a9aaa)
├─ Disabled state
├─ Placeholder text
└─ Tertiary information
```

### Functional Colors

```
Success Green (#10b981)
└─ "Completed" status badge

Warning Amber (#f59e0b)
└─ Alerts, pending states

Error Red (#ef4444)
└─ Error states

Error Light (#fee2e2)
└─ Error backgrounds
```

### Color Usage Rules

1. **Never use pure black** (#000000) — always use text-primary
2. **Text on teal background** = pure white (high contrast)
3. **Teal hover** = #14919b (teal-light)
4. **Disabled states** = reduce opacity by 50% or use text-muted
5. **Shadows** = always use text-primary with low opacity

---

## Typography

### Font Stack

```
UI (Default): 
"Inter", system-ui, sans-serif
├─ Geometric, clean, modern
├─ Weights: 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
└─ Perfect for UI and buttons

Blog Post Body:
"Lora", serif
├─ Warm, editorial, human
├─ Weights: 400 (regular), 500 (medium), 600 (semibold)
└─ Used only in blog post content, not UI
```

### Font Sizes & Line Heights

```
XS (12px / 16px line-height)
├─ Labels, badges, timestamps
└─ Small supporting text

SM (14px / 20px)
├─ Input labels, helper text
└─ Secondary information

Base (16px / 24px) ← DEFAULT
├─ Body text
├─ Chat messages
└─ Regular interactive elements

LG (18px / 28px)
├─ Blog post body text
└─ Large call-to-action

XL (20px / 28px)
├─ Section headers
└─ Card titles

2XL (24px / 32px)
├─ Preference labels
└─ Modal titles

3XL (30px / 36px)
├─ Page section headers
└─ Large emphasis

4XL (36px / 44px)
├─ Blog post hero heading
└─ Main page titles
```

### Font Weight Usage

```
300 (Light) — Rarely used, only for emphasis on large sizes
400 (Regular) — Body text, paragraphs
500 (Medium) — Label text, secondary headings
600 (Semibold) — Buttons, card titles, navigation
700 (Bold) — Page titles, hero headings
```

### Line Height Ratios

- **Compact** (1.33x) — Headlines, labels
- **Comfortable** (1.5x) — UI text
- **Generous** (1.75x) — Blog post body (editorial warmth)

---

## Spacing System

### Base Unit: 4px

```
1 = 4px   (xs)
2 = 8px   (sm)
3 = 12px  (md)
4 = 16px  (lg)
5 = 20px  (xl)
6 = 24px  (2xl)
8 = 32px  (3xl)
10 = 40px (4xl)
12 = 48px (5xl)
16 = 64px (6xl)
20 = 80px (7xl)
24 = 96px (8xl)
```

### Common Patterns

```
Padding in cards: 4 (16px)
Padding in buttons: 3-4 horizontal, 2-3 vertical
Gap between elements: 3-4
Margin between sections: 8-12
Gap between columns: 4-6
```

### Breathing Room

- Blog post max-width: 680px (generous margins)
- Panel widths: Left 220px, Right 280px
- Generous padding in modals and cards
- Whitespace is not wasted space — it's intentional

---

## Border Radius

### System

```
None       — 0px (very rare)
SM         — 8px (inputs, small cards)
MD         — 10px (most components) ⭐ DEFAULT
LG         — 12px (cards, panels)
XL         — 16px (large modals)
2XL        — 20px (extra large cards)
Full       — 9999px (pills, avatars)
```

### Usage Rules

1. **Buttons** → `rounded-full` for pill shape
2. **Card chips** → `rounded-full` for preferences
3. **Input fields** → `rounded-full` for chat input
4. **Panels** → `rounded-lg` (if not edge-to-edge)
5. **Images** → `rounded-lg` (slightly rounded)
6. **Message bubbles** → `rounded-lg`
7. **Accordions** → `rounded-md` for row levels

---

## Shadows

### Shadow Scale

```
None (Default)
├─ 0px (most elements)

XS (subtle background)
├─ 0 1px 2px 0 rgba(26, 26, 46, 0.05)
└─ Barely visible, for subtle depth

SM (cards, small depth)
├─ 0 1px 3px 0 rgba(26, 26, 46, 0.1)
├─ 0 1px 2px 0 rgba(26, 26, 46, 0.06)
└─ Used on messages, small cards

MD (medium elevation)
├─ 0 4px 6px -1px rgba(26, 26, 46, 0.1)
├─ 0 2px 4px -1px rgba(26, 26, 46, 0.06)
└─ Card hover, expanded panels

LG (strong elevation)
├─ 0 10px 15px -3px rgba(26, 26, 46, 0.1)
└─ Modals, prominent cards, itinerary

XL (maximum elevation)
├─ 0 20px 25px -5px rgba(26, 26, 46, 0.1)
└─ Hero overlays, max elevation

NONE (flat)
├─ Border-based depth instead
└─ Used for clarity in dark backgrounds
```

### Shadow Usage Rules

1. **Messages**: `shadow-sm` for subtle depth
2. **Cards**: `shadow-md` by default
3. **Hover state**: `shadow-lg`
4. **Itinerary**: `shadow-lg`
5. **Trip memory cards**: `shadow-md` default, `shadow-lg` on hover
6. **Use very light shadows** — this is not a skeuomorphic app

---

## Animations & Transitions

### Timing

```
Fast:      150ms (micro-interactions)
Normal:    300ms (standard) ⭐ DEFAULT
Slow:      500ms (complex transitions)
Very Slow: 1000ms+ (attention-grabbing)
```

### Easing Functions

```
Linear            — uniform pace
ease-in           — slow start, fast end
ease-out          — fast start, slow end ⭐ DEFAULT for exits
ease-in-out       — slow start & end (smooth)
cubic-bezier()    — custom curves
```

### Core Animations

#### 1. Message Entry (0.3s, ease-out)
```css
@keyframes slide-up {
  0% { transform: translateY(10px); opacity: 0 }
  100% { transform: translateY(0); opacity: 1 }
}
```
**Purpose**: Feel of messages floating up naturally

#### 2. Preference Update (1s, ease-in-out)
```css
@keyframes highlight {
  0% { background-color: rgba(13, 115, 119, 0) }
  50% { background-color: rgba(13, 115, 119, 0.1) }
  100% { background-color: rgba(13, 115, 119, 0) }
}
```
**Purpose**: Draw attention to live updates

#### 3. Typing Indicator (0.6s, infinite)
```css
@keyframes typing {
  0%, 60%, 100% { opacity: 0.3 }
  30% { opacity: 1 }
}
```
**Purpose**: Organic feel of agent thinking

#### 4. Fade In (0.3s, ease-in-out)
```css
@keyframes fade-in {
  0% { opacity: 0 }
  100% { opacity: 1 }
}
```
**Purpose**: Content appearing (modals, overlays)

#### 5. Pulse Soft (2s, infinite)
```css
@keyframes pulse-soft {
  0%, 100% { opacity: 1 }
  50% { opacity: 0.5 }
}
```
**Purpose**: Gentle "live" indicator (status dot)

#### 6. Rotate (0.3s, ease-out)
```css
transform: rotate(180deg)
```
**Purpose**: Chevron rotation on accordion toggle

---

## Interactive Elements

### Buttons

```
Base Style:
- Padding: 3-4px horizontal, 2-3px vertical
- Border radius: full
- Font weight: 600
- Font size: 14px
- Transition: 300ms ease-out
- No shadow by default

Variants:
- Primary (Teal) — filled, used for main CTAs
- Secondary (White) — outlined or ghost
- Tertiary (Gray) — minimal, for secondary actions
- Danger (Red) — for destructive actions

States:
- Default: Full color/opacity
- Hover: Darker shade (opacity increase or color change)
- Active: Same as hover + slight scale
- Disabled: 50% opacity, cursor not-allowed
- Loading: Spinner overlay
```

**Example**:
```tsx
<button className="px-6 py-3 bg-teal text-white rounded-full font-semibold text-sm hover:bg-teal-light transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
  Plan a trip
</button>
```

### Input Fields

```
Base Style:
- Background: warm-white or white
- Border: 1px solid gray-100
- Padding: 12px horizontal, 8px vertical
- Border radius: full
- Font: Inter, 14px
- Transition: 300ms ease-out

States:
- Default: Gray-100 border
- Focus: Teal border + soft shadow
- Hover: Gray-200 border
- Error: Red border + error-light background
- Disabled: Gray background, no pointer

Focus State:
- Border color: teal
- Box shadow: 0 0 0 3px rgba(13, 115, 119, 0.1)
```

### Cards

```
Base Style:
- Background: white
- Border: 1px solid gray-100
- Border radius: lg (12px)
- Padding: 16px-24px (depends on card type)
- Shadow: sm by default

Hover State (Interactive):
- Border color: teal/light
- Shadow: md
- Transform: translateY(-2px) if it lifts
- Transition: 300ms ease-out

Variant: No Border
- Subtle shadow increase on hover
- Border removed
- Softer feel
```

### Message Bubbles

```
User Message:
- Background: teal
- Text: white
- Border radius: lg with br-0 on bottom-right
- Padding: 12px 16px
- Max width: 80% or 400px
- Alignment: right

Agent Message:
- Background: white
- Text: text-primary
- Border: 1px solid gray-100
- Border radius: lg with bl-0 on bottom-left
- Padding: 12px 16px
- Max width: 80% or 500px (slightly wider)
- Alignment: left
- Shadow: sm

Typing Indicator:
- 3 animated dots
- Each dot: 8px, border-radius-full
- Background: teal
- Animation: staggered opacity
```

---

## Responsive Breakpoints

### Desktop (1280px+) — PRIMARY

All 3 panels visible:
```
[220px] [flex] [280px]
```

### Tablet (768px - 1279px) — FUTURE

Collapsible panels:
```
[hamburger] [main area] [drawer icon]
```

### Mobile (< 768px) — FUTURE

Full-width, stacked:
```
[preferences sheet]
[chat area]
[trip memory sheet]
```

---

## Component Specs

### Preference Chip

```
Grid layout with:
- Icon: 16px (emoji or SVG)
- Main label: 12px text-muted
- Value: 12px font-semibold text-primary
- Padding: 8px 12px
- Border radius: full
- Height: 32px
- Gap: 8px

Animation on update:
- Highlight class: 1s ease-in-out
- Border color: teal (temporary)
- Background flash: teal/10
```

### Message Component

```
Flex container with:
- Gap: 12px
- Alignment: items-center
- User message: flex-end
- Agent message: flex-start

Message bubble:
- Avatar: 32px, rounded-full (agent only)
- Content: rounded-lg, max-width constrained
- Timestamp: hidden (can add on hover)
```

### Itinerary Card

```
Layout:
- Hero image: 256px height, full width
- Details grid: 2 columns
- Each detail: white card, shadow-sm
- Days accordion: divide-y
- Footer: teal/5 background, CTA button

Expandable day:
- Header: 16px font, flex between
- Chevron: 18px, rotate on expand
- Content: 56px background, padded
- Activities: time flex-right, details flex-1

Image: Dynamic (destination-specific)
```

### Blog Post

```
Hero section:
- Image: full-width, min-height 384px
- Title: 48px bold, positioned bottom-left
- Gradient overlay: from transparent to black/50

Content:
- Max-width: 680px
- Padding: generous (24-48px each side)
- Font size: 18px (lg)
- Line height: generous (1.75x)
- Serif font for warmth

Day dividers:
- Horizontal line: teal/30, 1px
- Text: "Day 1 — Arrival", small caps, teal, 11px
- Centered between lines

Photo grid:
- 3 columns (desktop)
- Gap: 16px
- Images: rounded-lg, object-cover
- Hover: scale-105, shadow-lg
```

---

## Dark Mode (Future)

If implementing dark mode:

```
Warm White → Dark surface (#1a1a1f)
Off-White → Elevated (#2a2a31)
Cream → Accent surface (#3a3a41)
Text Primary → Off-white (#fafaf8)
Text Secondary → Gray-400 (#a0a0b0)
Teal → Teal-light (#3fb9cf)
```

---

## Accessibility

### Color Contrast

- Text on background: minimum 4.5:1 (WCAG AA)
- Text on teal: white for 12.8:1
- Disabled text: reduced but still readable

### Touch Targets

- Minimum 44px × 44px for buttons (mobile)
- 32px × 32px acceptable for desktop
- Sufficient gap between interactive elements

### Focus States

- Always visible (never `outline: none` without replacement)
- Focus color: teal
- Focus ring: 2px solid teal with 2px offset

### Motion

- Respect `prefers-reduced-motion` media query
- Animation: optional, not required to use app

---

## Icons

### Sets

```
Lucide React — for standard UI icons
Custom SVG — for TripMind-specific icons (compass, sparkle)
Emoji — for quick visual signals (budget 💰, vibe 🎯)
```

### Usage

```
UI Icons: 16-20px
Button icons: 18-20px
Large icons: 24px+
Navigation: 20px
Badge icons: 16px
Emoji: 18-24px
```

### Icon Colors

- Default: text-secondary or text-primary
- Active: teal
- Disabled: text-muted
- On teal: white

---

## Micro-interaction Rules

1. **Every action gets feedback** — hover, click, disable
2. **Animations are < 500ms** — fast feels responsive
3. **Easing matches motion** — out for exits, in-out for cycles
4. **Nothing moves alone** — changes trigger multiple signals
5. **Cascading animations are subtle** — stagger by 50-100ms max
6. **Z-index hierarchy matters** — overlays on top, backgrounds below

---

## QA Checklist

- [ ] All text meets WCAG AA contrast
- [ ] Hover states on all interactive elements
- [ ] Focus states visible on all focusable elements
- [ ] No layout shift on image load
- [ ] Animations respect prefers-reduced-motion
- [ ] Touch targets ≥ 44px on mobile
- [ ] Color not only indicator (always text/icon too)
- [ ] Responsive at all breakpoints
- [ ] No horizontal scroll except intentional
- [ ] Performance: animations 60fps
- [ ] Mobile font sizes readable without zoom

---

## Design Tokens (Exported from Tailwind)

See `tailwind.config.ts` for all values. Key exports:

```typescript
colors: { teal, ocean, warm-white, off-white, ... }
fontSize: { xs, sm, base, lg, xl, 2xl, 3xl, 4xl }
spacing: { 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24 }
borderRadius: { sm, md, lg, xl, 2xl, full }
shadows: { xs, sm, md, lg, xl }
animation: { fade-in, slide-up, highlight, typing, pulse-soft }
```
