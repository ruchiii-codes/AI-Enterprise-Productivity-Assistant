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


For the detailed architecture, See docs/deployment.md for the deployment guide.

## Multi-Tool Workflows

WorkMind can combine tools in a single request.

GitHub → Gmail
Find my recent GitHub activity and email me a summary.

Calendar → Gmail
Check my calendar for tomorrow and email me a summary.

Gmail → Calendar
Find my recent WorkMind emails and add a summary to my calendar.

## Project Structure

AI-Enterprise-Productivity-Assistant/
├── frontend/          # React frontend
├── server/            # FastAPI backend
├── tests/             # Tests
├── docs/              # Technical documentation
├── requirements.txt
└── README.md


## Run Locally

### Backend

git clone https://github.com/ruchiii-codes/AI-Enterprise-Productivity-Assistant.git
cd AI-Enterprise-Productivity-Assistant

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
copy .env.example .env

uvicorn server.main:app --reload

### Frontend

cd frontend
npm install
npm run dev

Add the required API keys, OAuth credentials, email configuration, and JWT settings to .env.
Never commit the real .env file.


## Documentation

| Document | Description |
|---|---|
| [Architecture](docs/architecture.md) | RAG, agents, integrations, MCP, evaluation, and security |
| [Deployment](docs/deployment.md) | AWS deployment and production configuration |


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

See docs/deployment.md for the deployment guide.