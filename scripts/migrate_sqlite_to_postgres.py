"""Copy the SQLite database into a freshly migrated PostgreSQL database.

Dry run by default: it reads both databases, reports exactly what it would
copy, and changes nothing. Pass --execute to write.

    # 1. Create the schema in Postgres (never copied from SQLite -- see below)
    DATABASE_URL=postgresql+psycopg://user:pw@host:5432/workmind alembic upgrade head

    # 2. Inspect the plan
    python -m scripts.migrate_sqlite_to_postgres \\
        --target postgresql+psycopg://user:pw@host:5432/workmind

    # 3. Do it
    python -m scripts.migrate_sqlite_to_postgres \\
        --target postgresql+psycopg://user:pw@host:5432/workmind --execute

The schema is built by Alembic rather than copied, and that is deliberate:
the live SQLite file has drifted from the models (documents.created_at is
nullable and documents.conversation_id has lost its foreign key), while the
migrations describe the schema the models actually declare. Building fresh
and copying only rows leaves the drift behind instead of carrying it forward.

The target must be empty. This script does not merge, upsert or resume; if a
run fails partway, drop and recreate the target schema before retrying.
"""

import argparse
import sys
from typing import Optional

from sqlalchemy import create_engine, func, inspect, select, text
from sqlalchemy.orm import Session

from server.config import settings
from server.db import models  # noqa: F401  (registers the tables)
from server.db.base import Base

# Parents before children: every foreign key must already point at a row that
# exists by the time the referencing row is inserted.
TABLE_ORDER = [
    "users",
    "conversations",
    "messages",
    "documents",
    "gmail_connections",
    "calendar_connections",
    "github_connections",
]

# Copied verbatim; Alembic owns it and rewriting it would desynchronise the
# target from its own migration history.
EXCLUDED_TABLES = {"alembic_version"}

BATCH_SIZE = 500


def _fail(message: str) -> int:
    print(f"\nERROR: {message}")
    return 1


def check_table_order() -> Optional[str]:
    """Guard against a model being added without updating TABLE_ORDER."""
    known = set(TABLE_ORDER) | EXCLUDED_TABLES
    declared = set(Base.metadata.tables)

    missing = declared - known
    if missing:
        return (
            f"TABLE_ORDER does not cover {sorted(missing)}. Add them in "
            "foreign-key order before running this script."
        )

    unknown = set(TABLE_ORDER) - declared
    if unknown:
        return f"TABLE_ORDER lists tables that no longer exist: {sorted(unknown)}"

    return None


def row_counts(engine, tables) -> dict:
    counts = {}
    with engine.connect() as connection:
        for name in tables:
            table = Base.metadata.tables[name]
            counts[name] = connection.execute(
                select(func.count()).select_from(table)
            ).scalar_one()
    return counts


def copy_table(source_session: Session, target_session: Session, name: str) -> int:
    """Copy one table, preserving primary keys."""
    table = Base.metadata.tables[name]
    copied = 0

    rows = source_session.execute(select(table)).mappings()

    batch = []
    for row in rows:
        batch.append(dict(row))

        if len(batch) >= BATCH_SIZE:
            target_session.execute(table.insert(), batch)
            copied += len(batch)
            batch = []

    if batch:
        target_session.execute(table.insert(), batch)
        copied += len(batch)

    return copied


def reset_sequences(target_session: Session, tables) -> list:
    """Point each identity sequence past the highest copied id.

    Rows are inserted with their original primary keys, which does not advance
    the sequence. Without this the next insert reuses id 1 and fails on a
    duplicate key. max(id) is the right basis, not the row count: deletions
    mean ids outrun the number of rows (conversations reaches 218 across 162
    rows in the current database).
    """
    notes = []

    for name in tables:
        table = Base.metadata.tables[name]

        if "id" not in table.columns:
            continue

        highest = target_session.execute(
            select(func.max(table.c.id))
        ).scalar()

        if highest is None:
            notes.append(f"   {name}: empty, sequence left at its default")
            continue

        target_session.execute(
            text(
                "SELECT setval("
                "  pg_get_serial_sequence(:table_name, 'id'), :next_value, false"
                ")"
            ),
            {"table_name": name, "next_value": highest + 1},
        )
        notes.append(f"   {name}: next id = {highest + 1}")

    return notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy SQLite data into a migrated PostgreSQL database.",
    )
    parser.add_argument(
        "--source",
        default=settings.DATABASE_URL,
        help="Source URL (default: the configured DATABASE_URL)",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target PostgreSQL URL, e.g. postgresql+psycopg://user:pw@host:5432/db",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually write. Without this the script only reports its plan.",
    )
    args = parser.parse_args()

    problem = check_table_order()
    if problem:
        return _fail(problem)

    if not args.source.startswith("sqlite"):
        return _fail(f"Source is not SQLite: {args.source}")

    if "postgresql" not in args.target:
        return _fail(f"Target is not PostgreSQL: {args.target}")

    mode = "EXECUTE" if args.execute else "DRY RUN"
    print(f"=== SQLite -> PostgreSQL [{mode}] ===\n")
    print(f"Source: {args.source}")
    print(f"Target: {args.target.split('@')[-1]}\n")

    source_engine = create_engine(args.source)
    target_engine = create_engine(args.target)

    # --- Target schema must exist and be empty -------------------------------
    try:
        target_tables = set(inspect(target_engine).get_table_names())
    except Exception as error:
        return _fail(f"Cannot reach the target database: {error}")

    expected = set(TABLE_ORDER)
    missing = expected - target_tables

    if missing:
        return _fail(
            f"Target is missing {sorted(missing)}. Run `alembic upgrade head` "
            "against the target first."
        )

    if "alembic_version" not in target_tables:
        return _fail(
            "Target has no alembic_version table. Its schema was not created "
            "by Alembic, so it may not match the models."
        )

    source_counts = row_counts(source_engine, TABLE_ORDER)
    target_counts = row_counts(target_engine, TABLE_ORDER)

    print("Rows to copy:")
    for name in TABLE_ORDER:
        print(f"   {name:<24} {source_counts[name]:>6}")
    print(f"   {'TOTAL':<24} {sum(source_counts.values()):>6}\n")

    occupied = {n: c for n, c in target_counts.items() if c}
    if occupied:
        return _fail(
            f"Target is not empty: {occupied}. This script does not merge; "
            "drop and recreate the schema, then re-run `alembic upgrade head`."
        )

    with source_engine.connect() as connection:
        source_revision = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar()

    with target_engine.connect() as connection:
        target_revision = connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar()

    print(f"Alembic revision   source: {source_revision}")
    print(f"Alembic revision   target: {target_revision}")

    if source_revision != target_revision:
        return _fail(
            "The two databases are at different migration revisions. Bring "
            "the target to the source's revision before copying."
        )

    if not args.execute:
        print(
            "\nDry run complete. Nothing was written.\n"
            "Re-run with --execute to copy."
        )
        return 0

    # --- Copy ----------------------------------------------------------------
    print("\nCopying...")
    copied_counts = {}

    with Session(source_engine) as source_session, Session(target_engine) as target_session:
        try:
            for name in TABLE_ORDER:
                copied = copy_table(source_session, target_session, name)
                copied_counts[name] = copied
                print(f"   {name:<24} {copied:>6}")

            print("\nResetting sequences...")
            for note in reset_sequences(target_session, TABLE_ORDER):
                print(note)

            target_session.commit()

        except Exception as error:
            target_session.rollback()
            return _fail(f"Copy failed and was rolled back: {error}")

    # --- Verify --------------------------------------------------------------
    print("\nVerifying...")
    final_counts = row_counts(target_engine, TABLE_ORDER)
    mismatches = [
        f"{name}: expected {source_counts[name]}, found {final_counts[name]}"
        for name in TABLE_ORDER
        if source_counts[name] != final_counts[name]
    ]

    if mismatches:
        return _fail("Row counts do not match:\n   " + "\n   ".join(mismatches))

    print(f"   all {len(TABLE_ORDER)} tables match ({sum(final_counts.values())} rows)")
    print(
        "\nDone. Point DATABASE_URL at the target and start the application.\n"
        "Keep the SQLite file until you have confirmed the app works against "
        "PostgreSQL."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
