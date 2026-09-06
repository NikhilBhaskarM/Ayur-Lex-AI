# Ayurvedic IPR & Regulatory AI Assistant

An advanced Retrieval-Augmented Generation (RAG) system designed to provide accurate, cited, and trustworthy answers to Intellectual Property Rights (IPR) and regulatory questions in the Ayurvedic domain.

## Architecture Overview

The system consists of a FastAPI backend and a Next.js frontend, backed by a PostgreSQL database and a Qdrant vector database. The core logic relies on an advanced RAG pipeline that handles complex legal/regulatory queries by combining vector similarity search with authority-level filtering and source citations.

## Features

- **Specialized RAG Pipeline**: Domain-specific retrieval tailored for Ayurvedic IPR (Patents, Trademarks, GI, Traditional Knowledge).
- **Citation Engine**: Automatically extracts and links specific government regulations and legal texts to the LLM's answers.
- **Confidence Scoring**: Returns a confidence metric based on retrieval quality and source authority levels.
- **Security & Sanitization**: Built-in prompt injection detection and input/output sanitization.
- **Role-Based Access Control**: JWT authentication with user and admin roles.

## Technology Stack

| Component | Technology |
| --- | --- |
| Backend | Python 3.11+, FastAPI |
| Database (Relational) | PostgreSQL, SQLAlchemy 2.0 (Async), Alembic |
| Database (Vector) | Qdrant |
| LLM Provider | Ollama (Local) / OpenAI (Cloud) |
| Frontend | Next.js, React, TailwindCSS |
| Containerization | Docker, Docker Compose |

## Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)

## Quick Start (Docker)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag2
   ```

2. Copy the environment variables template:
   ```bash
   cp .env.example .env
   ```
   *(Update the `.env` file with any required keys).*

3. Start the application:
   ```bash
   docker compose up -d
   ```

4. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API Docs: `http://localhost:8000/api/docs`

## Local Development Setup (Without Docker)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:create_app --reload --factory
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `DATABASE_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://user:pass@db:5432/rag2` |
| `DATABASE_URL_SYNC` | Sync PostgreSQL string (for Alembic offline) | `postgresql://user:pass@db:5432/rag2` |
| `QDRANT_URL` | URL for Qdrant vector database | `http://localhost:6333` |
| `LLM_PROVIDER` | `ollama` or `openai` | `ollama` |
| `LLM_MODEL` | The model name to use | `llama3.1:8b` |
| `OPENAI_API_KEY` | Required if LLM_PROVIDER is openai | - |
| `JWT_SECRET` | Secret key for JWT signing | - |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |

## Database Setup (Alembic)

To create a new migration after modifying models:
```bash
cd backend
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

## Vector Database (Qdrant) & LLM Setup

- **Qdrant**: Runs automatically via Docker. If running locally, ensure Qdrant is available on the specified `QDRANT_URL`.
- **Local LLM (Ollama)**: 
  ```bash
  ollama pull llama3.1:8b
  ```

## Document Ingestion & Seed Data

Populate the database with initial sources and an admin user:
```bash
python scripts/seed_sources.py
python scripts/seed_admin.py
```
*Note: The default admin credentials are `admin@ayurveda-ipr.local` / `changeme123`.*

## Running Tests

Ensure you are in the `backend` directory and run:
```bash
pytest
```
Test suite uses `pytest-asyncio` for async tests and an in-memory SQLite database.

## Project Structure (Abbreviated)
```
f:\rag2\
├── backend/
│   ├── alembic/            # Database migrations
│   ├── app/                # Main application code
│   │   ├── api/            # API routers (v1)
│   │   ├── rag/            # RAG pipeline, citations, confidence
│   │   ├── security/       # Input sanitization, injection detection
│   │   └── models/         # SQLAlchemy models
│   ├── tests/              # Pytest suite
│   └── alembic.ini         # Alembic configuration
├── frontend/               # Next.js application
├── scripts/                # Utility scripts (seeding)
├── tests/
│   └── golden_questions/   # Evaluation dataset
└── README.md
```

## Security Considerations

- **Prompt Injection**: The system includes a sanitizer that checks user inputs for common prompt override patterns before sending them to the LLM.
- **Sanitization**: Outputs from the LLM are scanned to strip unwanted scripts, external images, or dangerous Markdown.
- **Authentication**: All endpoints (except health and auth) require JWT bearer tokens.

## Privacy Notice

User conversations and interactions are stored in the database for continuity. No sensitive Personal Identifiable Information (PII) beyond email addresses is collected. Do not enter confidential or proprietary formulation data into the chat.

## Limitations

- The system relies on its indexed vector database. If a specific niche regulation has not been ingested, the AI may not have knowledge of it.
- Hallucinations, while minimized through rigorous RAG practices, are still possible.

## Legal Disclaimer

**This AI Assistant provides legal information, not legal advice.** The information provided by the Ayurvedic IPR & Regulatory AI Assistant is for informational and educational purposes only and does not constitute formal legal counsel, patent filing guidance, or regulatory compliance guarantees. Always consult with a qualified patent attorney, IPR professional, or regulatory consultant before making business or legal decisions.

## License

[MIT License](LICENSE)
