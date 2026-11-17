# MerchantAI – Agentic Campaign Copilot

An AI-powered campaign planning system for small and medium businesses. MerchantAI guides merchants through onboarding, generates campaign strategies, ad copy, and creative briefs using an agentic workflow with RAG-enhanced knowledge retrieval.

## Problem Statement

Small business owners struggle with digital advertising — they lack the expertise to plan campaigns, write compelling ad copy, and produce creative briefs. MerchantAI automates this end-to-end workflow with AI agents that act as a marketing team, making professional campaign planning accessible to any merchant.

## Key Features

- **Guided Merchant Onboarding** — Multi-step form collecting business information with real-time validation
- **AI Campaign Planning** — Agent generates campaign strategy (objective, audience, budget allocation, duration) using RAG context from a marketing knowledge base
- **Ad Copy Generation** — Agent produces primary ad copy with two variations, each with headline, description, and CTA
- **Creative Brief Generation** — Agent creates visual content direction with scene direction, tone, imagery suggestions, and format recommendations
- **Campaign Readiness Validation** — Checks all components are present and flags issues before launch
- **Demo Mode** — Fully functional without API keys using deterministic mock responses
- **Modular AI Provider** — Swap between Demo, OpenAI, and Anthropic backends via a single environment variable

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| Backend | FastAPI, Python 3.11+ |
| Database | SQLite + SQLAlchemy ORM |
| AI Providers | Demo (built-in), OpenAI, Anthropic |
| RAG | Keyword-based retrieval from local Markdown knowledge base |

## Architecture

```
Frontend (Next.js + TypeScript + Tailwind CSS)
    ↓ REST API
Backend (FastAPI + Python)
    ↓
Agent Orchestrator (state-machine routing)
    ├── Validation Tool (onboarding & readiness checks)
    ├── RAG Service (knowledge retrieval)
    └── AI Provider (Demo / OpenAI / Anthropic)
    ↓
Database (SQLite + SQLAlchemy)
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/orchestrator.py    # Agent orchestrator (state machine)
│   │   ├── api/
│   │   │   ├── merchant.py           # Merchant CRUD + onboarding validation
│   │   │   └── campaign.py           # Campaign planning + generation endpoints
│   │   ├── models/                   # SQLAlchemy models
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── ai_provider.py        # AI provider abstraction + Demo/OpenAI/Anthropic
│   │   │   └── rag_service.py        # RAG knowledge retrieval
│   │   ├── tools/validation.py       # Validation tool for agents
│   │   ├── config.py                 # Settings from environment
│   │   ├── database.py               # DB engine + session
│   │   └── main.py                   # FastAPI app entry point
│   ├── data/knowledge_base/          # RAG source documents (Markdown)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/                      # Next.js App Router (layout, page)
│   │   ├── components/
│   │   │   ├── onboarding/           # Multi-step onboarding form
│   │   │   └── dashboard/            # Campaign dashboard
│   │   └── lib/
│   │       ├── api.ts                # API client
│   │       └── types.ts              # TypeScript interfaces
│   └── package.json
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### Backend

```bash
cd backend
cp .env.example .env        # defaults to demo mode — no API keys needed
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

Optionally create `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```
This defaults to `http://localhost:8000` if not set.

## Running the Application

### Start the backend (port 8000)

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start the frontend (port 3000)

```bash
cd frontend
npm run dev
```

Open **http://localhost:3000** in your browser.

## Usage

1. Click **Get Started** on the landing page
2. Fill in the 3-step onboarding form (business info, goals, optional details)
3. Click **Complete Onboarding** — the merchant is created and validated
4. On the dashboard, click **Generate All** to run the full agent workflow:
   - Campaign plan → Ad copy → Creative brief → Readiness check
5. Review all generated components on the dashboard

### API Testing

```bash
# Create merchant
curl -X POST http://localhost:8000/api/merchants/ \
  -H "Content-Type: application/json" \
  -d '{"business_name":"Test Boutique","business_type":"Fashion","location":"Mumbai","product_service":"Ethnic wear","target_customers":"Women 22-40","marketing_goal":"Sales","campaign_budget":15000,"preferred_platform":"Instagram"}'

# Validate onboarding
curl -X POST http://localhost:8000/api/merchants/1/validate-onboarding

# Plan campaign
curl -X POST http://localhost:8000/api/campaigns/plan \
  -H "Content-Type: application/json" \
  -d '{"merchant_id":1}'

# Generate ad copy (uses campaign ID returned above)
curl -X POST http://localhost:8000/api/campaigns/1/generate-ad-copy

# Generate creative brief
curl -X POST http://localhost:8000/api/campaigns/1/generate-creative-brief

# Check readiness
curl -X POST http://localhost:8000/api/campaigns/1/check-readiness
```

## Demo Mode vs Production

| | Demo Mode (default) | Production |
|---|---|---|
| Config | `AI_PROVIDER=demo` | `AI_PROVIDER=openai` or `anthropic` |
| API Keys | Not required | Required (`OPENAI_API_KEY` / `ANTHROPIC_API_KEY`) |
| Responses | Deterministic mock data | Real LLM-generated content |
| Cost | Free | Per-token API charges |

## Testing

The project runs in **demo mode** by default and has been manually tested end-to-end:

| Feature | Status |
|---------|--------|
| Backend startup + health check | ✅ Passing |
| Merchant creation (POST /api/merchants/) | ✅ Passing |
| Onboarding validation | ✅ Passing |
| Campaign planning (agent + RAG) | ✅ Passing |
| Ad copy generation | ✅ Passing |
| Creative brief generation | ✅ Passing |
| Campaign readiness check | ✅ Passing |
| Frontend build | ✅ Passing |
| Full UI flow (onboarding → dashboard → generate all) | ✅ Passing |

> **Note:** No automated test suite is included yet. All features are verified through manual API and UI testing.

## Limitations

- **RAG uses keyword matching** — a production system would use vector embeddings (e.g. ChromaDB)
- **No authentication** — the API is unauthenticated; suitable for demo/portfolio use only
- **SQLite only** — works for single-user demos; production would need PostgreSQL
- **No automated tests** — testing is manual
- **Demo responses are static** — the same mock output regardless of input specifics
- **Single campaign per merchant** — each "Generate All" creates a new campaign record


## Credits & Attribution

- **[FastAPI](https://fastapi.tiangolo.com/)** — Backend framework (MIT License)
- **[Next.js](https://nextjs.org/)** — Frontend framework (MIT License)
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM (MIT License)
- **[Tailwind CSS](https://tailwindcss.com/)** — Utility-first CSS (MIT License)
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation (MIT License)

## License

This is a portfolio/demonstration project. See individual dependency licenses above.

---

**Disclaimer:** This is a prototype for demonstration purposes. It does not integrate with actual advertising platforms or process real payments.
