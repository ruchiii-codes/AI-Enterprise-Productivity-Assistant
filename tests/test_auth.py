"""Authentication endpoint tests.

These run against a temporary SQLite database rather than the developer's
assistant.db, and the verification email is stubbed so nothing reaches SMTP.
"""

import uuid
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from server.auth.service import hash_reset_token
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

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session, monkeypatch):
    """A TestClient wired to the temporary database, with email stubbed."""
    sent = []
    reset_emails = []

    def fake_send(recipient_email, verification_token):
        sent.append((recipient_email, verification_token))

    def fake_send_reset(recipient_email, reset_token):
        reset_emails.append((recipient_email, reset_token))

    monkeypatch.setattr(
        "server.auth.service.send_verification_email",
        fake_send,
    )
    monkeypatch.setattr(
        "server.auth.service.send_password_reset_email",
        fake_send_reset,
    )

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    test_client = TestClient(app)
    test_client.sent_emails = sent
    test_client.reset_emails = reset_emails

    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


def unique_email():
    return f"user-{uuid.uuid4().hex[:8]}@example.com"


def register(client, *, username=None, email=None, password="secret123"):
    return client.post(
        "/auth/register",
        json={
            "username": username or f"user{uuid.uuid4().hex[:8]}",
            "email": email or unique_email(),
            "password": password,
        },
    )


# ---------------------------------------------------------------- register


def test_register_creates_an_unverified_user_and_sends_an_email(client, db_session):
    email = unique_email()

    response = register(client, email=email)

    assert response.status_code == 200

    body = response.json()
    assert body["email"] == email
    # The password must never come back in the response.
    assert "password" not in body
    assert "hashed_password" not in body

    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    assert user.is_verified is False
    assert user.verification_token is not None
    assert user.hashed_password != "secret123"

    assert client.sent_emails == [(email, user.verification_token)]


def test_register_rejects_a_duplicate_email(client):
    email = unique_email()

    assert register(client, email=email).status_code == 200

    response = register(client, email=email)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered."


def test_register_rejects_a_duplicate_username(client):
    username = f"user{uuid.uuid4().hex[:8]}"

    assert register(client, username=username).status_code == 200

    response = register(client, username=username)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists."


# ------------------------------------------------------------------- login


def test_login_is_refused_until_the_email_is_verified(client):
    email = unique_email()
    register(client, email=email)

    response = client.post(
        "/auth/login",
        data={"username": email, "password": "secret123"},
    )

    assert response.status_code == 403
    assert "verify" in response.json()["detail"].lower()


def test_login_succeeds_after_verification(client, db_session):
    email = unique_email()
    register(client, email=email)

    user = db_session.query(User).filter(User.email == email).first()

    verify = client.get(f"/auth/verify-email?token={user.verification_token}")
    assert verify.status_code == 200

    db_session.refresh(user)
    assert user.is_verified is True
    # The token is single use.
    assert user.verification_token is None

    response = client.post(
        "/auth/login",
        data={"username": email, "password": "secret123"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_rejects_a_wrong_password(client, db_session):
    email = unique_email()
    register(client, email=email)

    user = db_session.query(User).filter(User.email == email).first()
    client.get(f"/auth/verify-email?token={user.verification_token}")

    response = client.post(
        "/auth/login",
        data={"username": email, "password": "not-the-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_login_rejects_an_unknown_email(client):
    response = client.post(
        "/auth/login",
        data={"username": unique_email(), "password": "secret123"},
    )

    # Same message as a wrong password, so the response does not reveal
    # whether the account exists.
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


# ------------------------------------------------------------ verify-email


def test_verify_email_rejects_an_unknown_token(client):
    response = client.get("/auth/verify-email?token=not-a-real-token")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid verification token."


def test_verify_email_rejects_an_expired_token(client, db_session):
    email = unique_email()
    register(client, email=email)

    user = db_session.query(User).filter(User.email == email).first()
    user.verification_token_expires = datetime.utcnow() - timedelta(hours=1)
    db_session.commit()

    response = client.get(f"/auth/verify-email?token={user.verification_token}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Verification token has expired."

    db_session.refresh(user)
    assert user.is_verified is False


def test_a_verification_token_cannot_be_reused(client, db_session):
    email = unique_email()
    register(client, email=email)

    user = db_session.query(User).filter(User.email == email).first()
    token = user.verification_token

    assert client.get(f"/auth/verify-email?token={token}").status_code == 200

    second = client.get(f"/auth/verify-email?token={token}")

    assert second.status_code == 400


# --------------------------------------------------------------------- me


def test_me_returns_the_signed_in_user(client, db_session):
    email = unique_email()
    register(client, email=email)

    user = db_session.query(User).filter(User.email == email).first()
    client.get(f"/auth/verify-email?token={user.verification_token}")

    token = client.post(
        "/auth/login",
        data={"username": email, "password": "secret123"},
    ).json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == email


def test_me_requires_a_valid_token(client):
    assert client.get("/auth/me").status_code in (401, 403)

    assert (
        client.get(
            "/auth/me",
            headers={"Authorization": "Bearer not-a-real-token"},
        ).status_code
        == 401
    )


# -------------------------------------------------------- password reset


def verified_user(client, db_session, password="secret123"):
    """Register and verify a user, returning their email."""
    email = unique_email()
    register(client, email=email, password=password)

    user = db_session.query(User).filter(User.email == email).first()
    client.get(f"/auth/verify-email?token={user.verification_token}")

    return email


def test_forgot_password_emails_a_token_and_stores_only_its_hash(
    client, db_session
):
    email = verified_user(client, db_session)

    response = client.post("/auth/forgot-password", json={"email": email})

    assert response.status_code == 200

    assert len(client.reset_emails) == 1
    recipient, token = client.reset_emails[0]
    assert recipient == email

    user = db_session.query(User).filter(User.email == email).first()

    # The raw token must never be at rest in the database.
    assert user.reset_token is not None
    assert user.reset_token != token
    assert user.reset_token == hash_reset_token(token)
    assert user.reset_token_expires > datetime.utcnow()


def test_forgot_password_looks_identical_for_an_unknown_address(client):
    known = client.post(
        "/auth/forgot-password", json={"email": unique_email()}
    )

    assert known.status_code == 200
    # No email is sent, and the response must not reveal that.
    assert client.reset_emails == []
    assert "if that email" in known.json()["message"].lower()


def test_reset_password_sets_the_new_password(client, db_session):
    email = verified_user(client, db_session)

    client.post("/auth/forgot-password", json={"email": email})
    _, token = client.reset_emails[0]

    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "a-brand-new-password"},
    )

    assert response.status_code == 200

    # The old password no longer works.
    assert (
        client.post(
            "/auth/login",
            data={"username": email, "password": "secret123"},
        ).status_code
        == 401
    )

    # The new one does.
    assert (
        client.post(
            "/auth/login",
            data={"username": email, "password": "a-brand-new-password"},
        ).status_code
        == 200
    )


def test_a_reset_token_cannot_be_reused(client, db_session):
    email = verified_user(client, db_session)

    client.post("/auth/forgot-password", json={"email": email})
    _, token = client.reset_emails[0]

    first = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "first-new-password"},
    )
    assert first.status_code == 200

    second = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "second-new-password"},
    )

    assert second.status_code == 400

    # The first reset stands.
    assert (
        client.post(
            "/auth/login",
            data={"username": email, "password": "first-new-password"},
        ).status_code
        == 200
    )


def test_reset_password_rejects_an_expired_token(client, db_session):
    email = verified_user(client, db_session)

    client.post("/auth/forgot-password", json={"email": email})
    _, token = client.reset_emails[0]

    user = db_session.query(User).filter(User.email == email).first()
    user.reset_token_expires = datetime.utcnow() - timedelta(minutes=1)
    db_session.commit()

    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "a-brand-new-password"},
    )

    assert response.status_code == 400
    assert "invalid or has expired" in response.json()["detail"]


def test_reset_password_rejects_an_unknown_token(client):
    response = client.post(
        "/auth/reset-password",
        json={"token": "not-a-real-token", "new_password": "long-enough-1"},
    )

    assert response.status_code == 400


def test_reset_password_enforces_a_minimum_length(client, db_session):
    email = verified_user(client, db_session)

    client.post("/auth/forgot-password", json={"email": email})
    _, token = client.reset_emails[0]

    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "short"},
    )

    # Rejected by the schema before any password is written.
    assert response.status_code == 422

    assert (
        client.post(
            "/auth/login",
            data={"username": email, "password": "secret123"},
        ).status_code
        == 200
    )


# ------------------------------------------------------------ rate limits


def test_login_is_rate_limited(client):
    email = unique_email()

    statuses = [
        client.post(
            "/auth/login",
            data={"username": email, "password": "whatever"},
        ).status_code
        for _ in range(12)
    ]

    # Unlimited password guessing was possible before this limit existed.
    assert 429 in statuses
    assert statuses.index(429) == 10


def test_forgot_password_is_rate_limited(client):
    statuses = [
        client.post(
            "/auth/forgot-password", json={"email": unique_email()}
        ).status_code
        for _ in range(7)
    ]

    # Stops the endpoint being used to send bulk mail.
    assert 429 in statuses
    assert statuses.index(429) == 5
