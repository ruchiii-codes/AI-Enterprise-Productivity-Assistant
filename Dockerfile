FROM python:3.13-slim

# Python behaviour
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

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

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]
