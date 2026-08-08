import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# GitHub Personal Access Token
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")