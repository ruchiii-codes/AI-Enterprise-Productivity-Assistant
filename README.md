# WorkMind – AI Enterprise Productivity Assistant

WorkMind is an AI-powered productivity assistant that brings document intelligence, conversational memory, and productivity tools into one workspace.

It combines RAG, agent-based routing, and integrations with Gmail, Google Calendar, and GitHub to let users ask questions and perform tasks using natural language.

---

## Features

| Area | Capabilities |
|---|---|
| 📄 **Document AI & RAG** | PDF processing, semantic search, BM25, hybrid retrieval, reranking, context compression |
| 💬 **Memory** | Persistent conversations, follow-ups, conversation search, pinning |
| 🤖 **Agents** | Planner, retriever, summarization, tool orchestration |
| 📧 **Gmail** | Search, read, summarize, send emails |
| 📅 **Calendar** | View, search, create events, scheduling workflows |
| 🐙 **GitHub** | Repositories, issues, pull requests, repository details, activity |
| 🔌 **MCP** | MCP client/server and external tool integration |
| 🔐 **Security** | JWT authentication, bcrypt, email verification, protected APIs |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| LLM | OpenRouter |
| Embeddings | SentenceTransformers |
| Vector Database | ChromaDB |
| Search | Semantic Search + BM25 |
| Reranking | Cross-Encoder |
| Database | SQLite |
| Integrations | Gmail, Google Calendar, GitHub |
| Protocol | MCP |
| Deployment | AWS |

---

## Architecture

```text
                         ┌───────────────────┐
                         │   React Frontend  │
                         │      WorkMind     │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   FastAPI Backend │
                         └─────────┬─────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
        ┌───────────┐       ┌────────────┐      ┌──────────────┐
        │   Agents  │       │    RAG     │      │    Tools     │
        │  Planner  │       │ Semantic   │      │ Gmail        │
        │ Retriever │       │ + BM25     │      │ Calendar     │
        │ Summarize │       │ + Reranker │      │ GitHub       │
        └───────────┘       └─────┬──────┘      │ MCP          │
                                  │             └──────────────┘
                                  ▼
                            ┌──────────┐
                            │ ChromaDB │
                            └──────────┘
```

For the detailed architecture, see [Architecture Documentation](docs/architecture.md).

---

## Multi-Tool Workflows

WorkMind can combine multiple tools in a single request.

**GitHub → Gmail**

Find my recent GitHub activity and email me a summary.

**Calendar → Gmail**

Check my calendar for tomorrow and email me a summary.

**Gmail → Calendar**

Find my recent WorkMind emails and add a summary to my calendar.

---

## Project Structure

```text
AI-Enterprise-Productivity-Assistant/
├── frontend/                   # React frontend
├── server/                     # FastAPI backend
│   ├── main.py                 # App factory, middleware, router registration
│   ├── config.py               # Typed settings (pydantic-settings)
│   ├── api/                    # HTTP routers (thin)
│   ├── auth/                   # JWT, password hashing, dependencies
│   ├── db/                     # Engine, session, SQLAlchemy models
│   ├── schemas/                # Pydantic request/response models
│   ├── services/
│   │   ├── rag/                # Ingestion + retrieval pipeline
│   │   ├── agents/             # Planner, orchestrator, chat, summarization
│   │   ├── tools/              # Tool dispatch
│   │   ├── conversations/      # Conversation + message persistence
│   │   ├── integrations/       # Gmail, Calendar, GitHub
│   │   ├── mcp/                # MCP client + server
│   │   ├── multi_tool/         # Multi-tool selection and execution
│   │   ├── providers/          # LLM and email clients
│   │   └── evaluation/         # Retrieval and agent evaluation
│   └── utils/                  # Cache, rate limiter
├── alembic/                    # Database migrations
├── scripts/                    # Evaluation entry points
├── tests/                      # Tests
├── docs/                       # Technical documentation
├── Dockerfile
├── pyproject.toml
├── requirements.txt            # Direct dependencies
├── requirements-dev.txt        # Test + lint tooling
├── requirements.lock.txt       # Exact resolved environment
└── README.md
```

---

## Run Locally

### Backend

```bash
git clone https://github.com/ruchiii-codes/AI-Enterprise-Productivity-Assistant.git
cd AI-Enterprise-Productivity-Assistant

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements-dev.txt
copy .env.example .env

# Create/upgrade the database schema
alembic upgrade head

uvicorn server.main:app --reload
```

`OPENROUTER_API_KEY` and `JWT_SECRET_KEY` are required; the app fails at
startup with a clear message if either is missing.

### Tests

```bash
pytest
ruff check server tests
```

### Database migrations

Schema changes are managed by Alembic, never by editing tables by hand:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Add the required API keys, OAuth credentials, email configuration, and JWT settings to `.env`.

> Never commit the real `.env` file.

---

## Documentation

| Document | Description |
|---|---|
| [Architecture](docs/architecture.md) | RAG, agents, integrations, MCP, evaluation, and security |
| [Deployment](docs/deployment.md) | AWS deployment and production configuration |

---

## Deployment

WorkMind is designed for deployment on AWS.

```text
React Frontend
      │
      ▼
 AWS Amplify
      │
      ▼
FastAPI Backend
      │
      ▼
Elastic Beanstalk
```

See [Deployment Documentation](docs/deployment.md) for the deployment guide.
