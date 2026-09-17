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

import os
from pathlib import Path
from typing import Literal, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repository root: server/config.py -> server/ -> repo root
BASE_DIR = Path(__file__).resolve().parents[1]

# Secrets that ship in .env.example, test fixtures and tutorials. None of them
# may reach a production deployment.
PLACEHOLDER_SECRETS = {
    "your_jwt_secret_key",
    "test-jwt-secret-not-for-production",
    "change-me",
    "changeme",
    "secret",
}

MIN_SECRET_LENGTH = 32

LOCAL_HOSTS = ("localhost", "127.0.0.1")


def _is_local(url: str) -> bool:
    return any(host in url for host in LOCAL_HOSTS)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # -----------------------------
    # Environment
    # -----------------------------
    # Development defaults are permissive so the app runs out of the box.
    # Setting this to "production" turns on the checks in
    # _validate_production_settings below, which fail at startup rather than
    # letting a misconfigured deployment serve traffic.
    ENVIRONMENT: Literal["development", "production"] = "development"

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

    # Connection pool sizing, ignored on SQLite. The ceiling a deployment can
    # reach is (DB_POOL_SIZE + DB_MAX_OVERFLOW) x workers x instances, which
    # must stay under the database's max_connections.
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # Seconds to wait for a new database connection. libpq's default is around
    # two minutes, which is far longer than any request should wait: an
    # unreachable database would hold a worker thread for the whole timeout,
    # and with few workers the health check alone would starve the pool.
    DB_CONNECT_TIMEOUT: int = 5

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
    EMAIL_TIMEOUT: int = 10

    # -----------------------------
    # Observability (Langfuse)
    # -----------------------------
    # Tracing is off unless explicitly enabled, so local runs and the test
    # suite never ship data. Missing keys are safe either way: the SDK logs a
    # warning and installs a no-op tracer rather than raising.
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_BASE_URL: str = "https://cloud.langfuse.com"
    LANGFUSE_TRACING_ENABLED: bool = False

    # -----------------------------
    # Rate limiting
    # -----------------------------
    # Unset means slowapi keeps its in-memory store, which is per worker
    # process. That is fine for local development and tests, but it means the
    # configured limits are multiplied by the number of workers and instances.
    # Point this at Redis/ElastiCache for any deployment running more than one.
    REDIS_URL: Optional[str] = None

    # Number of proxies between the client and the app. Behind an ALB this is
    # 1: the socket peer is the load balancer, so the real client address has
    # to come from X-Forwarded-For. Leave at 0 when nothing proxies the app --
    # trusting the header without a proxy would let clients spoof their own
    # rate-limit key.
    TRUSTED_PROXY_COUNT: int = 0

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def oauth_redirect_uris(self) -> list[tuple[str, str, bool]]:
        """(setting name, value, provider is configured) for each OAuth callback.

        A redirect URI only matters when its provider has credentials: a
        deployment that does not use GitHub should not be forced to invent a
        GitHub callback URL.
        """
        github_configured = bool(self.GITHUB_CLIENT_ID and self.GITHUB_CLIENT_SECRET)
        google_configured = bool(self.GOOGLE_CLIENT_ID and self.GOOGLE_CLIENT_SECRET)

        return [
            ("GITHUB_REDIRECT_URI", self.GITHUB_REDIRECT_URI, github_configured),
            ("GOOGLE_REDIRECT_URI", self.GOOGLE_REDIRECT_URI, google_configured),
            (
                "GOOGLE_CALENDAR_REDIRECT_URI",
                self.GOOGLE_CALENDAR_REDIRECT_URI,
                google_configured,
            ),
        ]

    @property
    def cors_origins(self) -> list[str]:
        """Allowed CORS origins.

        Production allows only the configured frontend. Development also
        allows the Vite dev server.
        """
        if self.is_production:
            return [self.FRONTEND_URL]

        origins = ["http://localhost:5173"]

        if self.FRONTEND_URL not in origins:
            origins.append(self.FRONTEND_URL)

        return origins

    @property
    def email_configured(self) -> bool:
        return all(
            [
                self.EMAIL_HOST,
                self.EMAIL_USERNAME,
                self.EMAIL_PASSWORD,
            ]
        )

    @model_validator(mode="after")
    def _validate_production_settings(self) -> "Settings":
        """Refuse to start a production deployment that is misconfigured.

        Each of these is silent in development but damaging in production: a
        guessable token secret, a reset link pointing at localhost, a database
        that disappears with the container, or password reset that cannot send
        the email it promises the user.
        """
        if not self.is_production:
            return self

        problems = []

        if self.JWT_SECRET_KEY.strip().lower() in PLACEHOLDER_SECRETS:
            problems.append(
                "JWT_SECRET_KEY is a known placeholder value. Generate one "
                "with: python -c \"import secrets; print(secrets.token_urlsafe(48))\""
            )
        elif len(self.JWT_SECRET_KEY) < MIN_SECRET_LENGTH:
            problems.append(
                f"JWT_SECRET_KEY is {len(self.JWT_SECRET_KEY)} characters; "
                f"at least {MIN_SECRET_LENGTH} are required."
            )

        if _is_local(self.FRONTEND_URL):
            problems.append(
                f"FRONTEND_URL is {self.FRONTEND_URL!r}. It sets both the CORS "
                "origin and the links in verification and password-reset "
                "emails, so it must be the public frontend URL."
            )

        # Each of these defaults to localhost. Left unchanged, the OAuth
        # provider redirects the user's browser to a machine that is not the
        # server, so the integration fails after the user has already
        # consented -- and it fails at the callback, not at startup, which is
        # why it is worth catching here.
        for name, value, provider_configured in self.oauth_redirect_uris:
            if not provider_configured:
                continue

            if _is_local(value):
                problems.append(
                    f"{name} is {value!r}. Point it at the deployed backend and "
                    "register the same URL with the provider."
                )
            elif not value.startswith("https://"):
                problems.append(
                    f"{name} is {value!r}. OAuth callbacks must use https in "
                    "production; Google rejects plain http for web clients."
                )

        if self.DATABASE_URL.startswith("sqlite"):
            problems.append(
                "DATABASE_URL still points at SQLite. Use PostgreSQL in "
                "production: postgresql+psycopg://user:password@host:5432/dbname"
            )

        if not self.email_configured:
            problems.append(
                "EMAIL_HOST, EMAIL_USERNAME and EMAIL_PASSWORD must all be set: "
                "email verification and password reset cannot deliver without them."
            )

        if problems:
            raise ValueError(
                "Invalid production configuration (ENVIRONMENT=production):\n"
                + "\n".join(f"  - {problem}" for problem in problems)
            )

        return self


settings = Settings()

# Directories the application writes to must exist before first use.
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# The Langfuse SDK reads its configuration from os.environ directly, and
# pydantic-settings does not export .env values there -- a key present only in
# .env reaches `settings` but never os.environ. Without this bridge, tracing
# stays silently off in local development while appearing configured.
#
# setdefault rather than assignment: a real environment variable (Elastic
# Beanstalk sets real ones) must always win over the .env file.
for _name, _value in (
    ("LANGFUSE_PUBLIC_KEY", settings.LANGFUSE_PUBLIC_KEY),
    ("LANGFUSE_SECRET_KEY", settings.LANGFUSE_SECRET_KEY),
    ("LANGFUSE_BASE_URL", settings.LANGFUSE_BASE_URL),
    ("LANGFUSE_TRACING_ENABLED", str(settings.LANGFUSE_TRACING_ENABLED).lower()),
):
    if _value:
        os.environ.setdefault(_name, _value)
