from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from server.config import settings

DATABASE_URL = settings.DATABASE_URL

IS_SQLITE = DATABASE_URL.startswith("sqlite")

# check_same_thread is SQLite-only; connect_timeout is a libpq parameter and
# bounds how long a request (the /health probe most of all) can block waiting
# for an unreachable database.
connect_args = (
    {"check_same_thread": False}
    if IS_SQLITE
    else {"connect_timeout": settings.DB_CONNECT_TIMEOUT}
)

# Pooling options that only apply to a networked database. RDS -- and any
# proxy or NAT gateway in front of it -- closes idle connections, and a pooled
# connection that was closed server-side fails on its next use with "server
# closed the connection unexpectedly". pool_pre_ping tests a connection before
# handing it out and transparently replaces a dead one; pool_recycle retires
# connections before they get old enough to be dropped.
pool_args = (
    {}
    if IS_SQLITE
    else {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
    }
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    **pool_args,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
