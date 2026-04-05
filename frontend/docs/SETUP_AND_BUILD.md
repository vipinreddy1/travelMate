# TripMind Frontend — Setup, Build & Deployment

## Environment Setup

### Prerequisites

- **Node.js**: 18.17+ (LTS recommended)
- **npm**: 9.0+ or **yarn**: 3.0+
- **Git**: For version control
- **Code Editor**: VS Code recommended

**Check installed versions**:
```bash
node --version    # Should be >= 18.17
npm --version     # Should be >= 9.0
git --version     # Should be installed
```

---

## Installation & Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/vipinreddy1/travelMate.git
cd travelMate/frontend
```

### 2. Install Dependencies

```bash
npm install
```

This installs all packages from `package.json`:
- Next.js 14.0.4
- React 18.2
- TypeScript 5.3
- Tailwind CSS 3.4
- Zustand 4.4
- ElevenLabs SDK
- TanStack Query 5.28
- And other utilities

**Installation time**: ~2-5 minutes depending on connection

**Troubleshooting**:
```bash
# If installation fails:
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# If issues persist:
npm install --legacy-peer-deps
```

### 3. Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
# Placeholder for future API URLs and API keys
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_ELEVENLABS_API_KEY=your_key_here
# NEXT_PUBLIC_AUTH0_DOMAIN=your_domain.auth0.com
# NEXT_PUBLIC_AUTH0_CLIENT_ID=your_client_id
```

**Note**: Current version uses mock data. Uncomment keys when integrating APIs.

### 4. Verify Installation

```bash
# Run linter to check for errors
npm run lint

# Should output: ✓ No ESLint errors found
```

---

## Development

### Start Development Server

```bash
npm run dev
```

**Output**:
```
  ▲ Next.js 14.0.4
  - ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

**Access Application**:
- Open browser to `http://localhost:3000`
- App hot-reloads on file saves
- See changes in real-time
- Errors display in terminal and browser

### Development Server Features

- **Hot Module Reloading (HMR)**: Changes reflect instantly
- **Fast Refresh**: Component state preserved during edits
- **Error Display**: Syntax errors shown in overlay
- **Source Maps**: Debugging with original source

### Stop Development Server

```bash
# Press Ctrl+C in terminal
^C
```

---

## Building for Production

### 1. Create Production Build

```bash
npm run build
```

**What happens**:
1. Compiles TypeScript to JavaScript
2. Optimizes Next.js production image
3. Generates static files
4. Runs ESLint checks
5. Creates `.next` folder with build output

**Output example**:
```
  ▲ Next.js 14.0.4

  Route (kind)                 Size     First Load JS
  ─────────────────────────────────────────────────────
  ○ /                         1.2 kB         82.5 kB
  ○ /trip/[id]                2.1 kB         84.6 kB
  
  ✓ Build successful
```

**Build time**: ~30-60 seconds

### 2. Start Production Server

```bash
npm start
```

**Access at**: `http://localhost:3000`

**Difference from `npm run dev`**:
- Optimized bundle
- No hot reloading
- Performance closer to production
- Serve pre-built assets

---

## Linting & Code Quality

### Run ESLint

```bash
npm run lint
```

**Checks for**:
- Code style violations
- Unused variables
- Type errors
- Import/export issues
- Next.js specific rules

**Fix automatically**:
```bash
npm run lint -- --fix
```

**Configuration**: `.eslintrc.json`

---

## Project Configuration

### Tailwind CSS Configuration

**File**: `tailwind.config.ts`

Defines:
- Custom colors
- Extended typography
- Animations
- Spacing system

```bash
# Regenerate CSS if needed
npm run build
```

### TypeScript Configuration

**File**: `tsconfig.json`

Key settings:
```json
{
  "compilerOptions": {
    "strict": true,           // Strict type checking
    "jsx": "preserve",        // For Next.js
    "moduleResolution": "bundler"  // For path aliases
  },
  "paths": {
    "@/*": ["./*"],
    "@/components/*": ["./components/*"]
    // ... more aliases
  }
}
```

### Next.js Configuration

**File**: `next.config.js`

Default settings work for most cases. May customize:
- Image optimization
- Redirect rules
- Rewrite rules
- Build optimization

---

## Testing (Setup Required)

### Future: Unit Tests

```bash
# Install Jest and React Testing Library
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch
```

### Future: E2E Tests

```bash
# Install Cypress
npm install --save-dev cypress

# Open Cypress dashboard
npx cypress open

# Run tests headless
npx cypress run
```

---

## Deployment

### Vercel (Recommended)

**Benefits**:
- Automatic builds on git push
- Zero-config deployment
- Environment variables management
- Preview deployments
- Analytics included

**Steps**:

1. **Connect Repository**
   - Go to https://vercel.com
   - Click "New Project"
   - Import GitHub repository

2. **Configure Project**
   - Framework: Next.js (auto-detected)
   - Root Directory: `frontend/`
   - Environment Variables: Add `.env.local` values

3. **Deploy**
   ```bash
   git push origin main
   # Vercel auto-builds and deploys
   ```

### Docker Deployment

**Dockerfile** (create in `frontend/` folder):

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --frozen-lockfile

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

**Build and run**:
```bash
docker build -t tripMind-frontend .
docker run -p 3000:3000 tripMind-frontend
```

### Manual Deployment to VPS

```bash
# 1. SSH into server
ssh user@server.com

# 2. Clone repository
git clone https://github.com/vipinreddy1/travelMate.git
cd travelMate/frontend

# 3. Install and build
npm install
npm run build

# 4. Start with PM2 (process manager)
npm install -g pm2
pm2 start "npm start" --name "tripMind-frontend"
pm2 startup
pm2 save
```

### Environment Variables for Deployment

Set environment variables on deployment platform:

```
NEXT_PUBLIC_API_URL=https://api.tripMind.com
NEXT_PUBLIC_ELEVENLABS_API_KEY=sk-xxx...
NEXT_PUBLIC_AUTH0_DOMAIN=tripMind.auth0.com
NEXT_PUBLIC_AUTH0_CLIENT_ID=xxx...
NEXTAUTH_SECRET=random-secret-key
DB_URL=postgresql://...
```

---

## Performance Optimization

### Current Optimizations

1. **Image Optimization**
   - Next.js `Image` component
   - Automatic responsive images
   - Lazy loading by default

2. **Code Splitting**
   - Route-based code splitting
   - Dynamic imports for heavy components

3. **CSS**
   - Tailwind PurgeCSS (removes unused styles)
   - Minimal CSS output

### Recommended Enhancements

```typescript
// Lazy load component
import dynamic from 'next/dynamic'

const BlogPostPage = dynamic(() => import('@/components/BlogPostPage'), {
  loading: () => <Skeleton />,
  ssr: false  // Disable server-side rendering if needed
})
```

### Bundle Analysis

```bash
# Analyze bundle size
npm install --save-dev @next/bundle-analyzer

# Update next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({})

# Run analysis
ANALYZE=true npm run build
```

---

## Debugging

### VS Code Debugging

**`.vscode/launch.json`**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/frontend/node_modules/.bin/next",
      "args": ["dev"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Browser DevTools

- **React Developer Tools**: Chrome Extension for component inspection
- **Network Tab**: Monitor API calls and performance
- **Console**: View errors and logs
- **Performance Tab**: Profile rendering performance

### Common Issues & Solutions

#### Issue: Module not found errors

```
Solution: npm install
          rm -rf node_modules .next
          npm install
```

#### Issue: TypeScript errors in VS Code

```
Solution: Restart TypeScript server
          Cmd+Shift+P → TypeScript: Restart TS Server
```

#### Issue: Port 3000 already in use

```bash
# Use different port
npm run dev -- -p 3001

# Or kill process using port 3000
lsof -i :3000
kill -9 <PID>
```

#### Issue: Tailwind classes not applying

```
Solution: Ensure content path is correct in tailwind.config.ts
          content: ['./app/**/*.{js,ts,jsx,tsx}',...]
          Restart dev server
```

---

## Workflow & Best Practices

### Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Make changes**
   ```bash
   npm run dev
   # Edit files, test in browser
   ```

3. **Check code quality**
   ```bash
   npm run lint -- --fix
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/feature-name
   ```

5. **Create Pull Request**
   - GitHub automatically builds and tests
   - Review changes
   - Merge to main when approved

### Pre-commit Checks

Recommended: Install Husky for automated checks

```bash
npm install husky --save-dev
npx husky install
npx husky add .husky/pre-commit "npm run lint"
```

---

## Scripts Reference

| Script | Purpose | When to Use |
|--------|---------|------------|
| `npm run dev` | Start dev server | Daily development |
| `npm run build` | Create production build | Before deployment |
| `npm start` | Run production server | Production testing |
| `npm run lint` | Check code quality | Before committing |
| `npm test` | Run unit tests | When available |

---

## Monitoring & Logging

### Build Logs

```bash
# View full build output
npm run build 2>&1 | tee build.log
```

### Runtime Logs

```bash
# Redirect logs to file
npm start > app.log 2>&1 &
```

### Error Tracking (Future)

Integration with Sentry:

```typescript
// sentry.config.ts
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
})
```

---

## Troubleshooting

### Build Fails with TypeScript Errors

```bash
# Check for errors
npm run lint

# Fix automatically
npm run lint -- --fix

# Rebuild
npm run build
```

### Performance Issues

```bash
# Analyze bundle
npm install --save-dev @next/bundle-analyzer
ANALYZE=true npm run build

# Check performance in production
npm start

# Use Lighthouse: DevTools → Lighthouse tab
```

### Strange Behavior After Update

```bash
# Clear cache and reinstall
rm -rf node_modules .next package-lock.json
npm install
npm run build
```

---

## Version Management

### Update Dependencies

```bash
# Check for updates
npm outdated

# Update all packages
npm update

# Update specific package
npm install package-name@latest

# Check for security vulnerabilities
npm audit

# Auto-fix vulnerabilities
npm audit fix
```

### Node Version

```bash
# Check current version
node --version

# Use nvm to switch versions
nvm use 18.17.0

# Install specific version
nvm install 18.17.0
```

---

## Security Best Practices

1. ✅ **Keep dependencies updated**
   ```bash
   npm audit fix
   ```

2. ✅ **Never commit sensitive data**
   - Use `.env.local` (in .gitignore)
   - Use secrets management for production

3. ✅ **Use secure headers**
   - Implemented via Next.js

4. ✅ **Validate environment variables**
   - Check .env variables at build time

5. ❌ **Don't expose API keys in client**
   - Keep sensitive keys server-side only

---

## CI/CD Pipeline (Recommended)

### GitHub Actions Example

**`.github/workflows/deploy.yml`**:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - run: npm install
      - run: npm run lint
      - run: npm run build
      
      - name: Deploy to Vercel
        uses: vercel/actions/deploy-production@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
```

---

## Maintenance

### Regular Maintenance Tasks

- **Weekly**: Review and fix ESLint warnings
- **Monthly**: Update dependencies (`npm update`)
- **Quarterly**: Audit security (`npm audit`)
- **Annually**: Review and update major versions

### Monitoring Checklist

- ✓ Build status on CI/CD
- ✓ Application performance metrics
- ✓ Error tracking and logging
- ✓ User analytics
- ✓ Uptime monitoring

---

## Support & Resources

- **Documentation**: `/docs` folder in repository
- **Next.js Docs**: https://nextjs.org/docs
- **React Docs**: https://react.dev
- **Tailwind Docs**: https://tailwindcss.com/docs
- **Zustand Docs**: https://github.com/pmndrs/zustand

