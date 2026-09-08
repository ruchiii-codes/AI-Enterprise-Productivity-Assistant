import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from server.api.auth import router as auth_router
from server.api.calendar_auth import router as calendar_auth_router
from server.api.chat import router as chat_router
from server.api.conversation import router as conversation_router
from server.api.document import router as document_router
from server.api.github_auth import router as github_auth_router
from server.api.gmail_auth import router as gmail_auth_router
from server.api.message import router as message_router
from server.api.upload import router as upload_router
from server.config import settings

# Imported for its side effect: defining the ORM classes registers every table
# on Base.metadata. Alembic's autogenerate compares against it. Do not remove.
from server.db import models  # noqa: F401
from server.utils.rate_limiter import limiter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown.

    Schema creation is handled by Alembic (`alembic upgrade head`), not by
    create_all, so that schema changes are versioned and reviewable.
    """
    logger.info("Starting AI Enterprise Productivity Assistant")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="AI Enterprise Productivity Assistant",
    description="Backend API for the AI Enterprise Productivity Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# -----------------------------
# Rate limiting
# -----------------------------
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
app.add_middleware(SlowAPIMiddleware)


# -----------------------------
# Request logging
# -----------------------------
@app.middleware("http")
async def request_monitoring(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        logger.info(
            "HTTP %s %s - %s - %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "HTTP %s %s failed after %.3fs",
            request.method,
            request.url.path,
            duration,
        )

        raise


# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)

# -----------------------------
# Routers
# -----------------------------
app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(document_router)
app.include_router(github_auth_router)
app.include_router(gmail_auth_router)
app.include_router(calendar_auth_router)
app.include_router(chat_router)


# -----------------------------
# Service routes
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Enterprise Productivity Assistant 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }
