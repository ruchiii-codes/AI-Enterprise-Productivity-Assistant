# WorkMind Architecture

This document gives a high-level overview of how WorkMind is structured and how its main AI components work together.

---

## 1. System Architecture

WorkMind is built with a React frontend and a FastAPI backend. The backend handles authentication, conversations, RAG, AI routing, memory, and productivity integrations.

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
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌──────────┐       ┌─────────────┐      ┌────────────┐
    │   Auth   │       │  AI + RAG   │      │   Tools    │
    │ & Memory │       │             │      │            │
    └──────────┘       └──────┬──────┘      └─────┬──────┘
                              │                    │
                              ▼                    ├── Gmail
                         ┌──────────┐              ├── Calendar
                         │ ChromaDB │              ├── GitHub
                         └──────────┘              └── MCP

```

## Main Components

| Component | Purpose |
|---|---|
| React Frontend | Chat, conversations, documents, settings and user interface |
| FastAPI Backend | API layer and application logic |
| Authentication | Registration, login, JWT and email verification |
| Memory | Conversation history and persistence |
| RAG | Document retrieval and context generation |
| Tool Layer | Gmail, Calendar, GitHub and MCP operations |
| ChromaDB | Vector storage and semantic search |
| SQLite | User, conversation and application data |


```text
## 2. RAG Pipeline

WorkMind uses Retrieval-Augmented Generation to answer questions using uploaded documents.

PDF Upload
    ↓
Text Extraction
    ↓
Cleaning + Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
User Query
    ↓
Semantic Search + BM25
    ↓
Hybrid Retrieval
    ↓
Cross-Encoder Reranking
    ↓
Context Compression
    ↓
LLM
    ↓
Answer

```

```text
| Component | Purpose |
|---|---|
| Embeddings | Represent document chunks as vectors |
| Semantic Search | Find content with similar meaning |
| BM25 | Find relevant keyword matches |
| Hybrid Search | Combine semantic and keyword results |
| Reranker | Reorder results by relevance |
| Context Compression | Keep only useful retrieved information |

```

Additional retrieval techniques include query rewriting, multi-query retrieval, HyDE, and parent-child retrieval.

```text
## 3. Agentic AI & Orchestration

WorkMind uses a planner-based approach to decide how a request should be handled.


User Request
     ↓
   Planner
     ↓
 Route / Intent
     │
 ┌───┼────────────┐
 ▼   ▼            ▼
RAG Summary     Tool
                  ↓
             Orchestrator
                  ↓
          External Service
                  ↓
              Response
```

| Component | Purpose |
|---|---|
| Planner | Determines the required route and action |
| Retriever | Retrieves relevant document context |
| Summarizer | Creates concise summaries |
| Tool Dispatcher | Executes the selected tool |
| Orchestrator | Coordinates multi-step workflows |

WorkMind supports workflows where one tool's result is used by another tool.

Examples:

- GitHub → Gmail
- GitHub → Calendar
- Calendar → Gmail
- Gmail → Calendar

---

## 4. Productivity Integrations

### Gmail

WorkMind can:

- Search emails
- Read messages
- Summarize emails
- Send emails
- Use email results in workflows

### Google Calendar

WorkMind can:

- View upcoming events
- Search events
- View tomorrow's events
- Create events
- Use calendar results in workflows

### GitHub

WorkMind can:

- View the connected GitHub account
- List repositories
- View issues
- View pull requests
- Get repository details
- View recent activity

---

## 5. Model Context Protocol (MCP)

WorkMind includes MCP support for connecting AI workflows with external tools.

```text
WorkMind Agent
      ↓
   MCP Client
      ↓
   MCP Server
      ↓
 External Tools

MCP provides a standard interface for exposing tools and capabilities to the AI system.


## 6. Evaluation

The retrieval pipeline is evaluated by comparing different retrieval approaches.

```text
Semantic Retrieval
        ↓
Hybrid Retrieval
        ↓
Hybrid + Reranking

| Metric | What it measures |
|---|---|
| Precision@K | Relevance of retrieved results |
| Recall@K | Coverage of relevant results |
| MRR | Position of the first relevant result |
| Hit Rate | Whether a relevant result was retrieved |
| Failure Analysis | Common retrieval failure cases |

---

## 7. Security

WorkMind uses several layers of application security.

| Area | Implementation |
|---|---|
| Authentication | JWT-based authentication |
| Passwords | bcrypt hashing |
| Email | Email verification |
| APIs | Protected authenticated routes |
| User Isolation | User-specific data and integrations |
| Rate Limiting | Request rate control |
| Secrets | Environment variables |

OAuth is used for connected productivity services such as Gmail, Google Calendar, and GitHub.

Sensitive values such as API keys, OAuth secrets, email credentials, and JWT secrets should never be committed to the repository.
