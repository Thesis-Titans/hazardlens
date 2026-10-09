# HazardLens Web

Frontend single-page application for HazardLens. Built with React 18, TypeScript, Vite, Tailwind CSS, TanStack Query, and MapLibre GL JS.

## Development Setup

```bash
# From repository root
cd web

# Install dependencies
npm ci

# Start local development server
npm run dev
```

## Verification Commands

Before opening a pull request or pushing changes, verify that the following checks pass:

```bash
# Linting
npm run lint

# TypeScript type checking
npx tsc --noEmit

# Production bundle build
npm run build
```
