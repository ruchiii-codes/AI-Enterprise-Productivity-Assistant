"""The GitHub authorization URL must request only the scope we intend.

The scope is a constant in the URL builder, so nothing else would catch it
widening again: repo grants read and write on every private repository, while
the integration only reads public activity and opens issues.
"""

import uuid
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.auth.security import create_access_token
from server.config import settings
from server.db.base import Base, get_db
from server.db.models import User
from server.main import app


@pytest.fixture
def db_session(tmp_path):
    """An isolated database for one test."""
    engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def auth_header(db_session):
    """A token for a verified user, minted directly to avoid the login limit."""
    email = f"user-{uuid.uuid4().hex[:8]}@example.com"

    db_session.add(
        User(
            username=f"user{uuid.uuid4().hex[:8]}",
            email=email,
            hashed_password="not-used-here",
            is_verified=True,
        )
    )
    db_session.commit()

    return {"Authorization": f"Bearer {create_access_token({'sub': email})}"}


def test_github_start_requests_only_public_repo_scope(client, auth_header, monkeypatch):
    monkeypatch.setattr(settings, "GITHUB_CLIENT_ID", "test-client-id")

    response = client.get("/auth/github/start", headers=auth_header)

    assert response.status_code == 200

    params = parse_qs(urlparse(response.json()["authorization_url"]).query)

    assert params["scope"] == ["public_repo"]
    assert params["redirect_uri"] == [settings.GITHUB_REDIRECT_URI]
    assert params["client_id"] == ["test-client-id"]

    # The CSRF token the callback checks against.
    assert params["state"][0]
