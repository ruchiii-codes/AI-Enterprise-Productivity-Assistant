#!/bin/sh
set -e

# Put the image's vector store in place on first boot. /app/data is a volume,
# so on a fresh one this directory is empty and the seed is copied in. An
# existing store is left alone, so documents uploaded in production survive a
# restart instead of being reverted to the image's snapshot.
#
# mkdir -p keeps this self-contained: the Dockerfile already creates the
# directory, but a bind-mounted /app/data would not necessarily have it.
mkdir -p /app/data/chroma_db

if [ -z "$(ls -A /app/data/chroma_db 2>/dev/null)" ]; then
    echo "Seeding vector store from image..."
    cp -r /app/seed/chroma_db/. /app/data/chroma_db/
else
    echo "Vector store already present; leaving it untouched."
fi

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
