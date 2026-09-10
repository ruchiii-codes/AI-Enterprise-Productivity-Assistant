FROM python:3.13-slim

# Python behaviour
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# The application's default DATABASE_URL resolves to /app/assistant.db, which
# is OUTSIDE the /app/data volume declared below -- so a container restart
# would silently recreate an empty schema and lose every user and
# conversation. Overriding it here puts the SQLite file on the volume.
#
# Production should override this again with a PostgreSQL URL; ENVIRONMENT
# =production refuses to start on SQLite for exactly that reason.
ENV DATABASE_URL=sqlite:////app/data/assistant.db

WORKDIR /app

# curl is used by HEALTHCHECK; build tooling is needed by some wheels.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencies first, so this layer caches across source changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code and everything needed to run migrations.
COPY server ./server
COPY alembic ./alembic
COPY alembic.ini .
COPY data/evaluation_questions.json data/agent_evaluation_questions.json ./data/
COPY docker-entrypoint.sh .

# The application writes to these; they are declared as volumes below so that
# uploads, the vector store and the SQLite database survive a container restart.
RUN mkdir -p /app/data/uploads /app/data/chroma_db \
    && chmod +x /app/docker-entrypoint.sh \
    && useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

VOLUME ["/app/data"]

EXPOSE 8000

# /health probes the database, and DB_CONNECT_TIMEOUT bounds that at 5s, so
# the client timeout must sit above it -- otherwise curl gives up first and a
# degraded instance never reports its own 503.
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]
