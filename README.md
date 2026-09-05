# Ayur-Lex-AI: Specialized Indian Patent Law & Ayurvedic IPR Engine

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF.svg)](https://vitejs.dev/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-DC2626.svg)](https://qdrant.tech/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, domain-grounded legal AI system designed for Indian Intellectual Property Rights (IPR), Patentability Assessments, and Regulatory Compliance in the Ayurvedic, phytopharmaceutical, and herbal biotechnology domains.

---

## Key Highlights

- **Strict Indian Statutory Grounding**: Zero generic textbook replies. Every query is statutorily contextualized with the **Indian Patents Act 1970** (§3(p) TKDL, §3(e) mere admixture, §3(d) therapeutic efficacy) and the **Biological Diversity Act 2002** (Form III NBA approval).
- **Multi-Agent Legal Chamber (Tribunal Debate)**: Simulates a real-time courtroom hearing over WebSockets between three specialized LLM agents:
  - **Applicant Attorney** (`Claude 3.5 Sonnet`): Advocates novelty, synergistic extraction, and technical bio-efficacy.
  - **Patent Examiner** (`GPT-4o`): Raises §3(p), §3(e), §3(d), and NBA clearance objections under CGPDTM guidelines.
  - **Presiding Arbiter** (`DeepSeek-R1`): Delivers binding legal determinations, claim amendments, and compliance roadmaps.
- **Adaptive Multi-Tier Query Routing**:
  - **Tier: Simple**: Instant statutory context-forcing prompt instruction; answers basic legal concepts strictly through the lens of Indian patent law.
  - **Tier: Standard**: Hybrid BM25 lexical + dense Qdrant vector retrieval, Cross-Encoder reranking, and citation engine linking official Gazettes, IPAB/High Court precedents, and Guidelines.
  - **Tier: Complex**: Full IRAC-structured legal opinions, statutory reasoner validation, and multi-agent tribunal debates.
- **High-Performance 2D Legal Chamber UI**: Interactive agent podiums with animated speaking states, live auto-scrolling debate transcripts, case intake presets, and real-time statutory risk telemetry heatmaps.
- **Unified Single-Origin Architecture**: Serves both the React SPA frontend and FastAPI backend under a single port (`http://localhost:8000/`) with zero CORS overhead and built-in client-side SPA routing.

---

## Architecture Overview

```mermaid
flowchart TB
    subgraph Client ["Client Layer (Browser)"]
        UI["React 18 + Vite SPA<br/>(TailwindCSS, Zustand, Lucide)"]
        Panel["Flat 2D Legal Chamber Panel<br/>(Podiums, Heatmaps, Transcripts)"]
    end

    subgraph Origin ["Unified Origin (http://localhost:8000)"]
        FastAPI["FastAPI Gateway<br/>(app.main:app)"]
        StaticSPA["Static SPA Mount<br/>(/frontend/dist)"]
        APIRoutes["REST API (/api/v1/*)"]
        WSRoutes["WebSocket (/api/v1/ws/debate)"]
    end

    subgraph Intelligence ["Statutory Intelligence & RAG Core"]
        Router["Adaptive Router<br/>(Simple / Standard / Complex)"]
        Security["Prompt Injection Guard<br/>& Input Sanitizer"]
        
        subgraph ReasoningEngine ["Legal Reasoning Layer"]
            StatutoryReasoner["Deterministic Statutory Reasoner<br/>(§3(p), §3(e), §3(d), BDA Form III)"]
            GeneralAI["General AI Reasoner<br/>(Ayur-Lex-AI Domain Persona)"]
        end

        subgraph MultiLLM ["Multi-Agent Legal Chamber"]
            Applicant["Applicant Attorney<br/>(Claude 3.5 Sonnet)"]
            Examiner["Patent Examiner<br/>(GPT-4o)"]
            Arbiter["Presiding Arbiter<br/>(DeepSeek-R1)"]
        end
    end

    subgraph Storage ["Persistence & Retrieval"]
        Qdrant[("Qdrant Vector DB<br/>(Dense Embeddings)")]
        BM25["BM25 Lexical Index"]
        Reranker["Cross-Encoder Reranker"]
        Postgres[("PostgreSQL 16<br/>(AsyncPG / SQLAlchemy 2.0)")]
        Redis[("Redis 7<br/>(Cache & Broker)")]
    end

    UI -->|"HTTP / WebSocket"| FastAPI
    FastAPI --> StaticSPA
    FastAPI --> APIRoutes
    FastAPI --> WSRoutes

    APIRoutes --> Security
    Security --> Router

    Router -->|"Tier: Simple"| GeneralAI
    Router -->|"Tier: Standard"| BM25 & Qdrant
    Router -->|"Tier: Complex"| StatutoryReasoner & MultiLLM

    BM25 & Qdrant --> Reranker
    Reranker --> StatutoryReasoner

    WSRoutes <-->|"Live Stream"| MultiLLM
    MultiLLM --> Postgres
    FastAPI --> Postgres
    FastAPI --> Redis
```

---

## Statutory Grounding Framework

Ayur-Lex-AI enforces statutory rigor at every layer of generation. Generic legal definitions are intercepted and framed under Indian statutes:

| Statute & Provision | Regulatory Rule | System Verification & Requirement |
| :--- | :--- | :--- |
| **Indian Patents Act 1970, §3(p)** | Inventions which in effect are traditional knowledge or an aggregation/duplication of known properties. | Cross-checked against **TKDL** (Traditional Knowledge Digital Library). Pure extracts or classical formulations are non-patentable. |
| **Indian Patents Act 1970, §3(e)** | Substances obtained by a mere admixture resulting only in aggregation of properties. | Requires quantitative synergism evidence (e.g., **Chou-Talalay Combination Index** $CI < 1.0$, isobologram analysis, or bioavailability enhancement via piperine/bio-enhancers). |
| **Indian Patents Act 1970, §3(d)** | Mere discovery of a new form of a known substance without enhanced efficacy. | Demands statistically significant proof of **enhanced therapeutic efficacy**, not merely altered pharmacokinetic or physical properties. |
| **Biological Diversity Act 2002, §6 & §19** | Mandatory prior approval for applying for IPR based on Indian biological resources. | Requires **Form III National Biodiversity Authority (NBA)** clearance prior to patent grant. Enforces benefit-sharing obligations. |
| **Drugs & Cosmetics Act 1940** | Regulation of Ayurvedic, Siddha, and Unani (ASU) drugs. | Distinguishes between **Classical formulations** (First Schedule authoritative texts) and **Patent & Proprietary (P&P)** medicines. |

---

## Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | Python 3.11+, FastAPI, Pydantic v2, Uvicorn |
| **Relational Database** | PostgreSQL 16, SQLAlchemy 2.0 (AsyncIO), Alembic migrations, AsyncPG |
| **Vector Store & Retrieval** | Qdrant (HNSW index), BM25 (rank-bm25), Cross-Encoder Reranker (`ms-marco-MiniLM-L-6-v2`) |
| **LLM Inference** | Ollama (Local: `llama3.1:8b`, `qwen2.5`, `deepseek-r1`), OpenAI (`gpt-4o`), Anthropic (`claude-3-5-sonnet`) |
| **Frontend Framework** | React 18, Vite 6, TypeScript 5.7, TailwindCSS 3.4 |
| **State & Networking** | Zustand 5, TanStack Query v5, Axios, Native WebSockets |
| **Icons & UI Styling** | Lucide React, clsx, tailwind-merge, custom cyberpunk & glassmorphic themes |
| **Streaming & Protocol** | ASGI WebSockets (`/api/v1/ws/debate`), Server-Sent Events (SSE) |
| **Containerization** | Docker, Docker Compose |

---

## Quick Start Guide

### Option 1: Unified Single-Origin Setup (Recommended)

Run both the frontend and backend under a single unified origin (`http://localhost:8000`):

#### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and `npm`
- PostgreSQL and Qdrant (running locally or via Docker)

#### 2. Build the Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```
*This outputs static production assets to `frontend/dist`.*

#### 3. Configure the Backend
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
```

#### 4. Run the Unified Server
```bash
uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000 --reload
```

#### 5. Access the Application
- **Unified Web Application**: [http://localhost:8000/](http://localhost:8000/)
- **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option 2: Full Docker Compose Deployment

Spin up all dependencies (PostgreSQL, Qdrant, Redis, Ollama, Backend, Frontend) with a single command:

```bash
# 1. Clone the repository
git clone https://github.com/NikhilBhaskarM/Ayur-Lex-AI.git
cd Ayur-Lex-AI

# 2. Configure environment variables
cp .env.example .env

# 3. Start all services
docker compose up -d
```

Services exposed:
- **Frontend SPA**: `http://localhost:3000`
- **Backend API & Docs**: `http://localhost:8000/docs`
- **Qdrant Vector DB Dashboard**: `http://localhost:6333/dashboard`

---

## Environment Configuration

Create a `.env` file in the project root:

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://ayurveda:ayurveda_secret@localhost:5432/ayurveda_ipr` |
| `DATABASE_URL_SYNC` | Synchronous PostgreSQL string (for Alembic migrations) | `postgresql://ayurveda:ayurveda_secret@localhost:5432/ayurveda_ipr` |
| `QDRANT_URL` | URL of the Qdrant vector database | `http://localhost:6333` |
| `REDIS_URL` | Redis connection URL | `redis://:ayurveda_redis_secret@localhost:6379/0` |
| `LLM_PROVIDER` | Active LLM provider (`ollama`, `openai`, `anthropic`) | `ollama` |
| `LLM_MODEL` | Primary reasoning model name | `llama3.1:8b` |
| `LLM_BASE_URL` | Base URL for OpenAI-compatible or local Ollama endpoints | `http://localhost:11434/v1` |
| `OPENAI_API_KEY` | OpenAI API key (required if `LLM_PROVIDER=openai`) | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional for Claude courtroom persona) | `sk-ant-...` |
| `JWT_SECRET` | Secret key for signing JWT authentication tokens | `your-secure-jwt-secret` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |

---

## API & WebSocket Endpoints

### Core REST Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status and database connectivity check. |
| `POST` | `/api/v1/auth/login` | Authenticate user and issue JWT bearer access token. |
| `POST` | `/api/v1/chat` | Send a legal query through the Adaptive RAG pipeline. |
| `POST` | `/api/v1/assessment` | Submit a formulation composition for a full statutory patentability audit. |
| `POST` | `/api/v1/citations/verify` | Validate statutory citations against official gazette indices. |

### Real-Time Legal Chamber WebSocket

- **WebSocket Route**: `ws://localhost:8000/api/v1/ws/debate` (or `ws://localhost:8000/ws/debate`)
- **Action**: Stream real-time multi-agent legal hearings.

#### Client Initiation Payload:
```json
{
  "action": "start_debate",
  "topic": "Patentability of a standardized Curcumin-Piperine nano-emulsion with enhanced bioavailability under Section 3(e) and 3(d)."
}
```

#### Streaming Message Event Schema:
```json
{
  "speaker": "examiner",
  "name": "Patent Examiner",
  "model": "GPT-4o",
  "text": "Objection raised under Section 3(e): The combination of Curcuma longa and Piper nigrum constitutes a mere admixture of known Ayurvedic herbs...",
  "statutory_risk": {
    "section_3p": 85.0,
    "section_3e": 72.5,
    "section_3d": 40.0,
    "bda_clearance": 95.0
  },
  "is_final": false
}
```

---

## Project Structure

```text
Ayur-Lex-AI/
├── backend/
│   ├── alembic/                       # Database migrations & versions
│   ├── app/
│   │   ├── api/                       # API router registrations
│   │   │   ├── v1/                    # v1 endpoints (chat, assessment, debate_stream)
│   │   │   │   ├── debate_stream.py   # Multi-LLM WebSocket streaming logic
│   │   │   │   ├── chat.py            # Chat & RAG endpoints
│   │   │   │   └── assessment.py      # IPR patentability assessment endpoints
│   │   ├── core/                      # Application config & database session
│   │   ├── models/                    # SQLAlchemy async ORM models
│   │   ├── rag/                       # Statutory intelligence & RAG pipeline
│   │   │   ├── adaptive_router.py     # Domain persona & query tier routing
│   │   │   ├── general_ai_reasoner.py # Direct statutory reasoning handlers
│   │   │   ├── statutory_reasoner.py  # Deterministic §3(p)/(e)/(d) & BDA rule engine
│   │   │   ├── retriever.py           # Hybrid Qdrant + BM25 retrieval
│   │   │   ├── reranker.py            # Cross-Encoder reranking
│   │   │   └── prompts/               # Statutory system & answer prompts
│   │   ├── security/                  # Prompt injection detection & sanitizers
│   │   └── services/                  # Business logic services
│   ├── tests/                         # Pytest test suite
│   ├── alembic.ini                    # Alembic configuration
│   └── requirements.txt               # Backend Python dependencies
├── frontend/
│   ├── public/                        # Static public assets
│   ├── src/
│   │   ├── components/                # Reusable UI components
│   │   │   ├── LegalChamberPanel.tsx  # Flat 2D Legal Chamber (Podiums, Heatmaps)
│   │   │   ├── ChatInterface.tsx      # Main legal conversation view
│   │   │   └── IPAssessment.tsx       # Formulation assessment view
│   │   ├── services/                  # API client & WebSocket handlers
│   │   ├── store/                     # Zustand state stores
│   │   ├── App.tsx                    # Root dashboard layout
│   │   └── main.tsx                   # Frontend entry point
│   ├── package.json                   # Frontend dependencies & build scripts
│   └── vite.config.ts                 # Vite configuration
├── docker-compose.yml                 # Multi-container orchestration
├── .env.example                       # Environment template
└── README.md                          # Project documentation
```

---

## Testing & Quality Assurance

Run the comprehensive test suite:

```bash
cd backend
pytest -v
```

To run end-to-end statutory validation checks:
```bash
python scratch/test_hard_constrained_chat.py
```

---

## Legal Disclaimer

> [!IMPORTANT]
> **Ayur-Lex-AI provides legal and regulatory information, NOT formal legal advice.**
> 
> The statutory evaluations, patentability assessments, and tribunal debate simulations generated by Ayur-Lex-AI are intended solely for academic, research, and preparatory patent intelligence purposes. They do not constitute formal legal counsel or guarantees of patent grant by the Indian Patent Office (CGPDTM) or the National Biodiversity Authority (NBA). Users should consult a registered Indian Patent Agent or IPR Advocate before filing patent specifications or biological resource access applications.

---

## License

This project is licensed under the [MIT License](LICENSE).
