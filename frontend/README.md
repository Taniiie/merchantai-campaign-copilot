# MerchantAI Frontend

Next.js frontend application for the MerchantAI Agentic SMB Marketing & Onboarding Copilot.

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **UI Library**: React 19
- **Styling**: Tailwind CSS 4
- **Language**: TypeScript (strict mode)

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

Create `.env.local` if you need to point to a custom backend host (defaults to `http://localhost:8000`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

- `npm run dev` — Starts the development server with Turbopack
- `npm run build` — Builds the application for production
- `npm run start` — Runs the production server
- `npm run lint` — Runs ESLint code quality checks
