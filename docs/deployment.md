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


## 1. Production Preparation

Before deploying:

Make sure the project runs correctly locally.
Confirm all backend dependencies are in requirements.txt.
Confirm the frontend builds successfully.
Keep secrets out of the source code.
Make sure .env is not committed to Git.
Keep .env.example updated.

Build the frontend:

cd frontend
npm install
npm run build


## 2. Backend Deployment

The FastAPI backend will be deployed using AWS Elastic Beanstalk.

The backend deployment should include:

server/
requirements.txt

Configure the required production environment variables through AWS instead of storing them in the repository.

The deployed backend must be accessible through an HTTPS URL.


## 3. Frontend Deployment

The React frontend will be deployed using AWS Amplify.

After the backend is deployed, update the frontend API configuration:

Local:
http://localhost:8000

Production:
https://<your-backend-domain>

Then deploy the frontend through AWS Amplify.      


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

Use .env.example as the reference.

Never commit the real .env file or other files containing secrets.


## 5. CORS Configuration

The backend must allow requests from the deployed frontend.

Local:

http://localhost:5173

Production:

https://<your-amplify-domain>

Update the backend CORS configuration before testing the live application.


## 6. OAuth Configuration

Gmail, Google Calendar, and GitHub integrations use OAuth.

Update the OAuth configuration with the production URLs:

- Google OAuth redirect URI
- Gmail OAuth redirect URI
- Google Calendar OAuth redirect URI
- GitHub OAuth callback URL

Remove or replace development localhost URLs where required.


## 7. Email Verification

The verification email must use the deployed frontend URL.

Local:

http://localhost:5173/verify-email

Production:

https://<your-frontend-domain>/verify-email

Make sure the backend generates the correct production verification link.


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

Also verify that no production feature is still using a local localhost URL. 


## Deployment Flow

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