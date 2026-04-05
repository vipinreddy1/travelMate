# Getting Started with TripMind Frontend

## Installation

Before running the development server, you need to install all dependencies:

```bash
cd frontend
npm install
```

This will install all packages defined in `package.json`:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Zustand (state management)
- TanStack Query (server state)
- Lucide React (icons)
- And other utilities

## Development Server

Once dependencies are installed, run the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Build for Production

To create an optimized production build:

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                     # Next.js App Router
├── components/              # React components
├── store/                   # Zustand state management
├── lib/                     # Utilities
├── hooks/                   # Custom React hooks
├── globals.css              # Global styles
└── tailwind.config.ts       # Tailwind configuration
```

## Next Steps

1. Run `npm install` to install dependencies
2. Run `npm run dev` to start the development server
3. Open `http://localhost:3000` in your browser
4. Start editing the components in the `components/` folder

## Troubleshooting

### Module not found errors
- Make sure you've run `npm install`
- Delete `node_modules` and `.next` folders and run `npm install` again

### TypeScript errors
- VSCode may show errors until node_modules is installed
- These will disappear after `npm install`

### Port 3000 already in use
Run on a different port:
```bash
npm run dev -- -p 3001
```

## Documentation

- [DEVELOPMENT.md](./DEVELOPMENT.md) - Architecture and development guide
- [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) - Visual design and component specs
- [README.md](./README.md) - Project overview
