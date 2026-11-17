# MerchantAI Backend

FastAPI backend powering the MerchantAI Agentic SMB Marketing & Onboarding Copilot.

## Architecture

- **FastAPI** — High-performance asynchronous web framework
- **SQLAlchemy 2.0** — Database ORM with SQLite (PostgreSQL-ready)
- **Pydantic v2** — Data validation and schema enforcement
- **Agent Orchestrator** — State machine coordinating validation, RAG, and AI provider layers
- **Modular AI Providers** — Plug-and-play support for Demo Mode (built-in, keyless), OpenAI, and Anthropic

## Getting Started

### 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

By default, `AI_PROVIDER=demo` runs completely offline with deterministic mock data without requiring any paid API keys.

To use live LLMs:
```env
AI_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```
or
```env
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
```

### 3. Run Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 4. Run Tests

```bash
python tests/test_api.py
```
