import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# GitHub Personal Access Token
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

# GitHub OAuth
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

GITHUB_REDIRECT_URI = os.getenv(
    "GITHUB_REDIRECT_URI",
    "http://localhost:8000/auth/github/callback",
)

# Gmail / Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI",
    "http://localhost:8000/auth/gmail/callback",
)

GOOGLE_CALENDAR_REDIRECT_URI = os.getenv(
    "GOOGLE_CALENDAR_REDIRECT_URI",
    "http://localhost:8000/auth/calendar/callback",
)

# Email / SMTP
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")