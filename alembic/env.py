"""Alembic environment.

The database URL and the target metadata both come from the application, so
migrations always run against the same configuration the app uses. The URL in
alembic.ini is deliberately left blank.
"""

import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context

# Make `server` importable when alembic is invoked from anywhere.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from server.config import settings  # noqa: E402

# Imported for its side effect: defining the ORM classes registers every table
# on Base.metadata, which autogenerate compares against. Do not remove.
from server.db import models  # noqa: E402,F401
from server.db.base import Base  # noqa: E402

config = context.config

# Inject the application's database URL rather than hardcoding one in the ini.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without a live DBAPI connection."""
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # SQLite cannot ALTER most columns in place; batch mode rewrites the
        # table instead. Harmless on other backends.
        render_as_batch=settings.DATABASE_URL.startswith("sqlite"),
    )

    with context.begin_transaction():
        context.run_migrations()


# Arbitrary but fixed: every instance must ask for the same lock for the lock
# to serialize them. Chosen to be unlikely to collide with another advisory
# lock in the same database.
MIGRATION_LOCK_ID = 4867211903


def _acquire_migration_lock(connection) -> None:
    """Serialize concurrent `alembic upgrade head` runs.

    The container entrypoint migrates on every start, so rolling out N
    instances launches N migrations at once. Without a lock they race: two
    processes can both see the same current revision and try to apply the same
    DDL, and the loser fails on an already-existing object -- taking the
    instance down on boot.

    pg_advisory_xact_lock blocks until the lock is free and releases on
    transaction end, so the second instance simply waits, then finds the
    schema already at head and applies nothing.

    SQLite has no equivalent and no concurrent deployment to protect, so it is
    skipped there.
    """
    if settings.DATABASE_URL.startswith("sqlite"):
        return

    from sqlalchemy import text

    connection.execute(
        text("SELECT pg_advisory_xact_lock(:lock_id)"),
        {"lock_id": MIGRATION_LOCK_ID},
    )


def run_migrations_online() -> None:
    """Run migrations against a live connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=settings.DATABASE_URL.startswith("sqlite"),
        )

        with context.begin_transaction():
            _acquire_migration_lock(connection)
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
