#!/bin/sh
set -e

# Bring the database schema up to date before serving. On a fresh volume this
# creates every table; on an existing one it applies only new revisions.
echo "Applying database migrations..."
alembic upgrade head

# Defaults to a single worker because the default DATABASE_URL is SQLite, and
# concurrent writers to one SQLite file cause "database is locked" errors.
# Raise WEB_CONCURRENCY once DATABASE_URL points at Postgres/RDS.
echo "Starting server on port ${PORT:-8000} with ${WEB_CONCURRENCY:-1} worker(s)..."
exec uvicorn server.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-1}"
