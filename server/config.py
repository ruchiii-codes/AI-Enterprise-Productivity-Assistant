"""Application configuration.

All environment access happens here. Modules import ``settings`` rather than
calling ``os.getenv`` directly, so a missing or malformed value fails at
startup with a clear message instead of surfacing as ``None`` deep inside a
request.

Filesystem paths are resolved relative to the repository root rather than the
current working directory. Previously ``data/uploads``, ``data/chroma_db`` and
``./assistant.db`` were CWD-relative, so launching the app from any other
directory silently created an empty database and vector store.
"""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Repository root: server/config.py -> server/ -> repo root
BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # -----------------------------
    # Required
    # -----------------------------
    OPENROUTER_API_KEY: str
    JWT_SECRET_KEY: str

    # -----------------------------
    # Paths
    # -----------------------------
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    CHROMA_DIR: Path = BASE_DIR / "data" / "chroma_db"

    # -----------------------------
    # Database
    # -----------------------------
    DATABASE_URL: str = f"sqlite:///{(BASE_DIR / 'assistant.db').as_posix()}"

    # -----------------------------
    # Auth
    # -----------------------------
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # -----------------------------
    # GitHub
    # -----------------------------
    GITHUB_ACCESS_TOKEN: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/auth/github/callback"

    # -----------------------------
    # Google (Gmail + Calendar)
    # -----------------------------
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/gmail/callback"
    GOOGLE_CALENDAR_REDIRECT_URI: str = (
        "http://localhost:8000/auth/calendar/callback"
    )

    # -----------------------------
    # Frontend / CORS
    # -----------------------------
    FRONTEND_URL: str = "http://localhost:5173"

    # -----------------------------
    # Email / SMTP
    # -----------------------------
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    @property
    def cors_origins(self) -> list[str]:
        """Allowed CORS origins: local dev plus the configured frontend."""
        origins = ["http://localhost:5173"]

        if self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)

        return origins


settings = Settings()

# Directories the application writes to must exist before first use.
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DIR.mkdir(parents=True, exist_ok=True)
