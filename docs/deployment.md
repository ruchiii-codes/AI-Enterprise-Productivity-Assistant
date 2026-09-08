# WorkMind Deployment

This document covers the main steps required to deploy WorkMind to AWS.

---

## Deployment Architecture

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
      │
      ├── Gmail
      ├── Google Calendar
      ├── GitHub
      └── LLM / AI Services
```

---

## 1. Production Preparation

Before deploying:

- Make sure the project runs correctly locally.
- Confirm all backend dependencies are in `requirements.txt`.
- Confirm the frontend builds successfully.
- Keep secrets out of the source code.
- Make sure `.env` is not committed to Git.
- Keep `.env.example` updated.

Build the frontend:

```bash
cd frontend
npm install
npm run build
```

---

## 2. Backend Deployment

The FastAPI backend will be deployed using AWS Elastic Beanstalk.

The backend deployment must include:

```text
server/            # application code
alembic/           # migrations
alembic.ini
requirements.txt
Dockerfile
docker-entrypoint.sh
```

Configure the required production environment variables through AWS instead of storing them in the repository.

The deployed backend must be accessible through an HTTPS URL.

### Container

The image runs migrations before starting the server, so a deploy applies
schema changes automatically:

```bash
docker build -t workmind-backend .
docker run -p 8000:8000 --env-file .env -v workmind-data:/app/data workmind-backend
```

Notes:

- `/app/data` is a volume. Uploads, the ChromaDB vector store and the SQLite
  database live there; without the volume they are lost on every restart.
- The container runs as a non-root user and exposes `/health` for the
  load balancer.
- `WEB_CONCURRENCY` defaults to **1**. Multiple workers against one SQLite
  file produce "database is locked" errors. Raise it only after pointing
  `DATABASE_URL` at Postgres/RDS.

### Persistence

SQLite on a container filesystem is not suitable for production. For a real
deployment, provision RDS and set:

```text
DATABASE_URL=postgresql+psycopg://user:password@host:5432/workmind
```

Then run `alembic upgrade head` against it. No code changes are required —
the URL is the only thing that differs.

### Migrations

Never edit the schema by hand. To change it:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

An existing database that predates Alembic is brought under management with
`alembic stamp head`, which records the current revision without re-running
DDL.

---

## 3. Frontend Deployment

The React frontend will be deployed using AWS Amplify.

After the backend is deployed, update the frontend API configuration.

**Local:**

```text
http://localhost:8000
```

**Production:**

```text
https://<your-backend-domain>
```

Then deploy the frontend through AWS Amplify.

---

## 4. Environment Variables

WorkMind uses environment variables for application secrets and external services.

| Category | Examples |
|---|---|
| LLM | OpenRouter API key |
| Authentication | JWT secret |
| Email | SMTP configuration |
| Google | OAuth client ID and secret |
| GitHub | OAuth client ID and secret |
| Database | Database configuration |
| Frontend | Backend API URL |

Use `.env.example` as the reference.

Never commit the real `.env` file or other files containing secrets.

---

## 5. CORS Configuration

The backend must allow requests from the deployed frontend.

**Local:**

```text
http://localhost:5173
```

**Production:**

```text
https://<your-amplify-domain>
```

Update the backend CORS configuration before testing the live application.

---

## 6. OAuth Configuration

Gmail, Google Calendar, and GitHub integrations use OAuth.

Update the OAuth configuration with the production URLs:

- Google OAuth redirect URI
- Gmail OAuth redirect URI
- Google Calendar OAuth redirect URI
- GitHub OAuth callback URL

Remove or replace development `localhost` URLs where required.

---

## 7. Email Verification

The verification email must use the deployed frontend URL.

**Local:**

```text
http://localhost:5173/verify-email
```

**Production:**

```text
https://<your-frontend-domain>/verify-email
```

Make sure the backend generates the correct production verification link.

---

## 8. Production Checklist

Before making WorkMind public:

- [ ] Production JWT secret configured
- [ ] API keys stored securely
- [ ] OAuth secrets configured
- [ ] `.env` excluded from Git
- [ ] HTTPS enabled
- [ ] CORS configured
- [ ] OAuth redirect URLs updated
- [ ] Email verification URL updated
- [ ] Rate limiting enabled
- [ ] Protected APIs verified

---

## 9. Post-Deployment Testing

Test the live application for:

### Authentication

- Registration
- Email verification
- Login
- Logout

### Documents and RAG

- PDF upload
- Document questions
- Conversation memory

### Integrations

- Gmail
- Google Calendar
- GitHub

### Multi-Tool Workflows

- GitHub → Gmail
- GitHub → Calendar
- Calendar → Gmail
- Gmail → Calendar

Also verify that no production feature is still using a local `localhost` URL.

---

## Deployment Flow

```text
Production Preparation
        ↓
Backend → AWS Elastic Beanstalk
        ↓
Backend HTTPS URL
        ↓
Update Frontend API URL
        ↓
Frontend → AWS Amplify
        ↓
Configure CORS + OAuth
        ↓
Update Email Verification URL
        ↓
Live Testing
```
