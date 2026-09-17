import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langfuse import get_client
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

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
from server.db.base import engine
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
    logger.info(
        "Starting AI Enterprise Productivity Assistant (environment=%s)",
        settings.ENVIRONMENT,
    )
    yield

    # Langfuse batches traces on a background thread; a container that stops
    # without flushing loses whatever is still buffered.
    #
    # Guarded on the flag rather than called unconditionally: with tracing off
    # there is nothing buffered to lose, and merely asking for the client logs
    # "Authentication error: ... initialized without public_key", which reads
    # like a fault on every shutdown of a correctly configured deployment.
    if settings.LANGFUSE_TRACING_ENABLED:
        try:
            get_client().flush()
        except Exception:
            logger.warning("Langfuse flush on shutdown failed", exc_info=True)

    logger.info("Shutting down")


# The interactive docs publish every route, schema and validation rule. That is
# useful in development and is an inventory of the attack surface in
# production, so they are served only outside it.
docs_urls = (
    {"docs_url": None, "redoc_url": None, "openapi_url": None}
    if settings.is_production
    else {}
)

app = FastAPI(
    title="AI Enterprise Productivity Assistant",
    description="Backend API for the AI Enterprise Productivity Assistant",
    version="1.0.0",
    lifespan=lifespan,
    **docs_urls,
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
    """Liveness and readiness for the load balancer.

    The database is checked because an instance that cannot reach RDS cannot
    serve a single useful request. Reporting "running" on process liveness
    alone would keep the load balancer sending traffic to an instance that
    fails every one of them.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        database_ok = True

    except SQLAlchemyError:
        logger.exception("Health check failed: database unreachable")
        database_ok = False

    payload = {
        "status": "running" if database_ok else "degraded",
        "database": "ok" if database_ok else "unreachable",
    }

    if database_ok:
        return payload

    # 503 tells the load balancer to stop routing here until it recovers.
    return JSONResponse(status_code=503, content=payload)
